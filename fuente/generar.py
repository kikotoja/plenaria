#!/usr/bin/env python3
"""Genera la web de los asistentes (un único HTML) a partir de datos/*.json y plantilla.html.

Uso:
  python3 generar.py salida.html --completo   documento entero, para GitHub Pages
  python3 generar.py salida.html              solo el contenido, para publicarlo como Artifact
"""
import json, pathlib, re, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import laminas  # noqa: E402

AQUI = pathlib.Path(__file__).resolve().parent
DATOS = AQUI / "datos"
ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
COMPLETO = "--completo" in sys.argv
SALIDA = pathlib.Path(ARGS[0]) if ARGS else AQUI / "index.html"

# Perfil de LinkedIn de Kiko para el botón; vacío, el botón no aparece
LINKEDIN = "https://www.linkedin.com/in/kikotoja"

# ID de medición de Google Analytics (Kiko, 23-10); vacío, la web sale sin etiqueta. Solo en la versión --completo
GTAG = "G-13G1XNBXBY"

ORDEN = ["vih", "cardio", "geafen", "gedefo", "gteii", "neuropsiquiatria", "neumo"]


def norm(t):
    t = (t or "").lower()
    for a, b in zip("áéíóúü", "aeiouu"):
        t = t.replace(a, b)
    return t


def main():
    areas = []
    for nombre in ORDEN:
        p = DATOS / f"{nombre}.json"
        if p.exists():
            areas.append(json.loads(p.read_text(encoding="utf-8")))
    # Enlaza cada noticia de última hora con su fármaco cuando el texto lo nombra al principio
    for a in areas:
        for u in a.get("ultima_hora") or []:
            cab = norm(u.get("texto", ""))[:80]
            for f in a.get("farmacos") or []:
                nombres = [norm(x).strip() for x in re.split(r"[/+]", f.get("dci", ""))]
                if cab.startswith(norm(f.get("dci", ""))) or (nombres and cab.startswith(nombres[0])):
                    u["farmaco"] = f["id"]
                    break
    datos = json.dumps(areas, ensure_ascii=False).replace("</", "<\\/")
    lams = json.dumps(laminas.todas(), ensure_ascii=False).replace("</", "<\\/")
    mont = (DATOS / "montanas.json").read_text(encoding="utf-8") if (DATOS / "montanas.json").exists() else "[]"
    mont = json.dumps(json.loads(mont), ensure_ascii=False).replace("</", "<\\/")
    salida = (AQUI / "plantilla.html").read_text(encoding="utf-8").replace("{{DATOS}}", datos).replace("{{LAMINAS}}", lams).replace("{{MONTANAS}}", mont).replace("{{LINKEDIN}}", LINKEDIN.replace("'", ""))
    if COMPLETO:
        cabeza, cuerpo = salida.split("<!-- cuerpo -->", 1)
        etiqueta = (f'<!-- Google tag (gtag.js) -->\n<script async src="https://www.googletagmanager.com/gtag/js?id={GTAG}"></script>\n'
                    "<script>\n  window.dataLayer = window.dataLayer || [];\n  function gtag(){dataLayer.push(arguments);}\n"
                    f"  gtag('js', new Date());\n  gtag('config', '{GTAG}');\n</script>\n") if GTAG else ""
        salida = ('<!doctype html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n' + etiqueta +
                  '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
                  '<meta name="robots" content="noindex">\n'
                  + cabeza.replace("<style>", "<style>\nhtml { padding-top: env(safe-area-inset-top, 0px); padding-bottom: env(safe-area-inset-bottom, 0px); }\nbody { margin: 0; }\n[hidden] { display: none !important; }", 1)
                  + "</head>\n<body>\n" + cuerpo + "\n</body>\n</html>\n")
    SALIDA.write_text(salida, encoding="utf-8")
    n = sum(len(a.get("farmacos") or []) for a in areas)
    print(f"{SALIDA} · {len(areas)} áreas · {n} fármacos")


if __name__ == "__main__":
    main()
