"""Delega una tarea a un modelo gratis y devuelve solo un resumen corto.

Uso:
  python delegar.py tarea.md [--archivos a.py b.py] [--worker opencode|codex|agy|auto] [--modelo opencode/xxx]

- Copia los archivos a una carpeta aislada (resultados/<id>/); el original no se toca.
- Rechaza archivos con pinta de secretos (.env, claves) y contenido con claves.
- Cadena de respaldo: si un worker falla o da 429, pasa al siguiente (config.json -> "cadena").
- Todo queda en registro.jsonl. Imprime: id, worker, segundos, ruta de salida, archivos cambiados.
"""
import argparse, datetime, difflib, json, os, pathlib, re, shutil, subprocess, sys, threading, time, uuid

AQUI = pathlib.Path(__file__).parent
DS = "opencode:opencode/deepseek-v4.1-flash-free"
CFG = {"cadena": [DS], "timeout": 300, "tope_diario": 150,
       # perfil -> orden de workers; el primero que responda gana, el resto es respaldo
       "perfiles": {"re": [DS, "codex:"],        # ingenieria inversa / analisis de fallas (solo alcance autorizado)
                    "codigo": ["codex:", DS],    # implementar con spec clara
                    "ui": ["agy:", "codex:"]}}   # probar UI en navegador, lectura larga
if (AQUI / "config.json").exists():
    CFG.update(json.loads((AQUI / "config.json").read_text(encoding="utf-8")))

# Aislamiento (verificado 2026-11-19): OpenCode sube por las carpetas buscando skills/reglas y lee
# ~/.claude/CLAUDE.md. Sin esto el modelo ve el nombre del usuario y 100+ skills. Hace falta TODO:
# home limpio + carpeta de trabajo fuera de C:\Users\<usuario>.
BASE = pathlib.Path(CFG.get("base_trabajo", r"C:\ocwork"))
_H = str((AQUI / "_home").resolve())
ENV_AISLADO = {**os.environ, "USERPROFILE": _H, "HOME": _H, "XDG_CONFIG_HOME": _H + r"\.config",
               "XDG_DATA_HOME": _H + r"\.local\share", "XDG_CACHE_HOME": _H + r"\.cache",
               "OPENCODE_DISABLE_CLAUDE_CODE": "1"}

PROHIBIDOS = re.compile(r"(^|[\\/])(\.env.*|.*\.(pem|key|pfx|p12)|id_rsa.*|credentials.*|.*secret.*)$", re.I)
CLAVES = re.compile(r"(sk-[A-Za-z0-9_-]{20,}|AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----|ghp_[A-Za-z0-9]{30,})")
ANSI = re.compile(r"\x1b\[[0-9;?]*[A-Za-z]")
LIMITE = re.compile(r"429|rate.?limit|usage limit|quota|upstream request failed|too many", re.I)


EDITAR = False
BASE_ACTUAL = pathlib.Path(".")  # carpeta de trabajo de la tarea en curso (la fija main)
TEXTO = {".md", ".txt", ".py", ".js", ".ts", ".tsx", ".json", ".html", ".css", ".csv", ".yml", ".yaml", ".sh"}


def exe(worker):
    # agy se instala en AppData\Local\agy\bin y el instalador no lo agrega al PATH
    p = shutil.which(worker)
    if p is None and worker == "agy":
        c = pathlib.Path(os.environ.get("LOCALAPPDATA", "")) / "agy" / "bin" / "agy.exe"
        p = str(c) if c.exists() else None
    return p


def copiar_skill(nombre, work):
    home = pathlib.Path(os.path.expanduser("~"))
    for base in (home / ".claude" / "skills", home / ".agents" / "skills", AQUI.parent.parent / ".claude" / "skills"):
        s = base / nombre
        if (s / "SKILL.md").is_file():
            break
    else:
        abortar(f"no existe la skill {nombre}")
    dst = work / "skills" / nombre
    peso = sum(f.stat().st_size for f in s.rglob("*") if f.is_file())
    if peso <= 3_000_000:
        shutil.copytree(s, dst)
    else:  # shortcut: skill con assets pesados, va solo SKILL.md; subir el tope si hace falta
        dst.mkdir(parents=True)
        shutil.copy(s / "SKILL.md", dst)
    if CLAVES.search((dst / "SKILL.md").read_text(encoding="utf-8", errors="ignore")):
        abortar(f"la skill {nombre} contiene algo que parece una clave")
    return f"skills/{nombre}/SKILL.md"


def ejecutar(cmd, cwd, timeout, entrada=None):
    """Corre el worker y lo corta al toque si en su stderr aparece un limite de cuota.
    OpenCode, ante 'Free usage limit reached', reintenta en vez de fallar y colgaba hasta el timeout."""
    # OpenCode resuelve rutas relativas con la variable PWD heredada (la pone Git Bash), no con el cwd real
    env = {**ENV_AISLADO, "PWD": str(cwd), "INIT_CWD": str(cwd)}
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE if entrada else subprocess.DEVNULL, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="replace", cwd=cwd, env=env)
    if entrada:  # por stdin porque el shim de Windows corta los argumentos en el primer salto de linea
        try:
            p.stdin.write(entrada)
            p.stdin.close()
        except OSError:
            pass
    buf = {"out": [], "err": []}
    limite = threading.Event()

    def leer(pipe, k):
        for linea in pipe:
            buf[k].append(linea)
            if k == "err" and LIMITE.search(linea):  # solo stderr: la respuesta puede nombrar "quota" legitimamente
                limite.set()

    hilos = [threading.Thread(target=leer, args=(p.stdout, "out"), daemon=True),
             threading.Thread(target=leer, args=(p.stderr, "err"), daemon=True)]
    for h in hilos:
        h.start()
    t0, motivo = time.time(), ""
    while p.poll() is None:
        if limite.is_set():
            motivo = "LIMITE"
        elif time.time() - t0 > timeout:
            motivo = "TIMEOUT"
        if motivo:
            # en Windows kill() solo mata el shim; /T mata todo el arbol
            subprocess.run(["taskkill", "/F", "/T", "/PID", str(p.pid)], capture_output=True)
            break
        time.sleep(0.3)
    p.wait()
    for h in hilos:
        h.join(timeout=3)
    return ANSI.sub("", "".join(buf["out"])), ANSI.sub("", "".join(buf["err"])), p.returncode, motivo


def estado():
    """Por worker: instalado, llamadas de hoy (ok/fallo) y el ultimo intento. Lee registro.jsonl."""
    reg = AQUI / "registro.jsonl"
    filas = [json.loads(l) for l in reg.read_text(encoding="utf-8").splitlines() if l.strip()] if reg.exists() else []
    hoy = datetime.date.today().isoformat()
    for w in ("opencode", "codex", "agy"):
        mias = [r for r in filas if r["worker"] == w]
        h = [r for r in mias if r["ts"].startswith(hoy)]
        linea = f"{w:9s} {'instalado' if exe(w) else 'NO instalado':12s} hoy: {sum(r['ok'] for r in h)} ok / {sum(not r['ok'] for r in h)} fallo"
        if mias:
            u = mias[-1]
            linea += f" | ultimo {u['ts'][5:16]} " + ("ok" if u["ok"] else "FALLO: " + u["err"].strip().replace("\n", " ")[-110:])
        print(linea)
    print(f"tope diario por worker: {CFG['tope_diario']} | timeout: {CFG['timeout']}s | perfiles: " +
          ", ".join(f"{k}={'>'.join(x.split(':')[0] for x in v)}" for k, v in CFG["perfiles"].items()))


def abortar(msg):
    sys.exit(f"RECHAZADO: {msg}")


def comando(worker, modelo, prompt_file):
    # shortcut: codex/agy sin verificar flags hasta instalarlos; ajustar aca si cambian
    msg = "Cumpli la tarea del archivo adjunto. Responde solo lo que pide."
    if worker == "opencode":
        # --auto solo con --editar: aun asi edita la copia aislada, nunca el original
        extra = ["--auto"] if EDITAR else []
        # --print-logs: sin esto el error de cuota no sale por stderr y no se puede detectar
        return [shutil.which("opencode") or "opencode", "run", msg, "-m", modelo, "-f", prompt_file,
                "--print-logs", "--log-level", "ERROR"] + extra
    if worker == "codex":
        # Verificado 2026-11-21 (v0.171): sin --approve-for-me Codex no puede leer archivos en Windows
        # ("rejected: blocked by policy", con cualquier sandbox/home). Con --approve-for-me las aprobaciones
        # pasan por revision automatica en workspace-write: lee y puede editar SOLO la copia aislada.
        return [shutil.which("codex") or "codex", "exec", "--skip-git-repo-check", "--ephemeral",
                "--ignore-user-config", "--ignore-rules", "--approve-for-me", "-o", "ultimo.txt",
                f"Lee {prompt_file} y cumpli la tarea. Responde solo lo que pide."]
    if worker == "agy":
        # verificado 2026-11-20 (v1.5.13): reusa el login de la app; no lee CLAUDE.md ni las skills del usuario
        return [exe("agy"), "-p", f"Lee {prompt_file} y cumpli la tarea. Responde solo lo que pide.",
                "--print-timeout", f"{CFG['timeout']}s", "--disable-slash-commands",
                "--model", modelo or "gemini-3.8-flash-medium"] + (["--mode", "accept-edits"] if EDITAR else [])
    abortar(f"worker desconocido: {worker}")


def usos_hoy(worker):
    reg = AQUI / "registro.jsonl"
    if not reg.exists():
        return 0
    hoy = datetime.date.today().isoformat()
    n = 0
    for l in reg.read_text(encoding="utf-8").splitlines():
        r = json.loads(l)
        if r["ts"].startswith(hoy) and r["worker"] == worker:
            n += 1
    return n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tarea", nargs="?")
    ap.add_argument("--estado", action="store_true", help="muestra que workers hay y como vienen hoy")
    ap.add_argument("--archivos", nargs="*", default=[])
    ap.add_argument("--worker", default="auto")
    ap.add_argument("--modelo", default=None)
    ap.add_argument("--skill", nargs="*", default=[], help="nombres de skills de ~/.claude/skills a pasarle al worker")
    ap.add_argument("--perfil", choices=list(CFG["perfiles"]), default=None, help="re | codigo | ui")
    ap.add_argument("--editar", action="store_true", help="deja que el worker edite la copia")
    a = ap.parse_args()
    if a.estado:
        return estado()
    if not a.tarea:
        ap.error("falta la tarea (o usa --estado)")
    global EDITAR
    EDITAR = a.editar

    tarea = pathlib.Path(a.tarea)
    if not tarea.is_file():
        abortar(f"no existe {tarea}")
    entradas = [tarea] + [pathlib.Path(x) for x in a.archivos]
    for p in entradas:
        if not p.is_file():
            abortar(f"no existe {p}")
        if PROHIBIDOS.search(str(p)):
            abortar(f"{p} parece un archivo de secretos")
        if CLAVES.search(p.read_text(encoding="utf-8", errors="ignore")):
            abortar(f"{p} contiene algo que parece una clave")

    id_ = datetime.datetime.now().strftime("%Y%m%d-%H%M%S-") + uuid.uuid4().hex[:4]
    work = BASE / id_
    work.mkdir(parents=True)
    global BASE_ACTUAL
    BASE_ACTUAL = work
    destino = AQUI / "resultados" / id_
    originales = {}
    for p in entradas:
        shutil.copy(p, work / p.name)
        originales[p.name] = (work / p.name).read_text(encoding="utf-8", errors="ignore")
    prompt_file = tarea.name
    if a.skill:
        # se copia SOLO la skill elegida para esta tarea (no todo ~/.claude): menos tokens, menos datos expuestos
        refs = [copiar_skill(s, work) for s in a.skill]
        extra = ("\n\nSkills a seguir: antes de empezar lee y aplica " + ", ".join(refs) +
                 " (las rutas relativas dentro de cada skill salen de su propia carpeta).\n")
        with open(work / prompt_file, "a", encoding="utf-8") as f:
            f.write(extra)
        originales[prompt_file] += extra

    if a.perfil:
        cadena = CFG["perfiles"][a.perfil]
    else:
        cadena = CFG["cadena"] if a.worker == "auto" else [f"{a.worker}:{a.modelo or ''}"]
    ultimo_error = ""
    for paso in cadena:
        worker, _, modelo = paso.partition(":")
        if exe(worker) is None:
            ultimo_error = f"{worker} no esta instalado"
            continue
        if usos_hoy(worker) >= CFG["tope_diario"]:
            ultimo_error = f"{worker}: tope diario alcanzado"
            continue
        t0 = time.time()
        try:
            cmd = comando(worker, modelo, prompt_file)
            cmd, entrada = cmd if isinstance(cmd, tuple) else (cmd, None)
            out, err, rc, motivo = ejecutar(cmd, work, CFG["timeout"], entrada)
            if worker == "codex" and (work / "ultimo.txt").exists():
                out = (work / "ultimo.txt").read_text(encoding="utf-8", errors="replace")
            ok = bool(out.strip()) and rc == 0 and not motivo and not LIMITE.search(err + out[:300])
            if motivo:
                err = motivo + " " + err
        except OSError as e:
            out, err, ok = "", str(e), False
        seg = round(time.time() - t0, 1)
        with open(AQUI / "registro.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps({"ts": datetime.datetime.now().isoformat(timespec="seconds"), "worker": worker,
                                "modelo": modelo, "ok": ok, "seg": seg, "err": err[-200:]}, ensure_ascii=False) + "\n")
        if ok:
            (work / "salida.md").write_text(out, encoding="utf-8")
            cambiados = []
            for n, orig in originales.items():
                nuevo = (work / n).read_text(encoding="utf-8", errors="ignore")
                if nuevo != orig:
                    cambiados.append(n)
                    d = difflib.unified_diff(orig.splitlines(), nuevo.splitlines(), n, n + " (nuevo)", lineterm="")
                    (work / f"{n}.diff").write_text("\n".join(d), encoding="utf-8")
            shutil.copytree(work, destino)
            print(f"id={id_} worker={worker}:{modelo} seg={seg}")
            print(f"salida: {destino / 'salida.md'}")
            print("cambiados:", ", ".join(cambiados) or "ninguno (ver salida.md)")
            print("--- primeras lineas ---")
            print("\n".join(out.strip().splitlines()[:15]))
            return
        ultimo_error = f"{worker}:{modelo} fallo ({err[-120:].strip() or 'sin salida'})"
        print("respaldo ->", ultimo_error, file=sys.stderr)
    abortar(f"ningun worker respondio. Ultimo: {ultimo_error}")


if __name__ == "__main__":
    main()
