#!/usr/bin/env python3
"""
sincronizar.py — Mantiene iguales los archivos compartidos, valida y empaqueta.

Algunas piezas existen en varias skills para que cada una funcione sola (por ejemplo
si alguien sube solo una skill a Claude). La copia "maestra" es la de la izquierda:

  adaptador/references/ficha-marca.md   -> carrusel-tryhard, creador-de-guiones, guion-broll, historias, calendario-contenido
  carrusel-tryhard/scripts/{efectos,fuentes,render}.py -> historias/scripts/

Uso (desde la raíz del repo):
  python herramientas/sincronizar.py            copia las maestras, valida y arma dist/*.zip
  python herramientas/sincronizar.py --revisar  solo revisa que todo esté igual (para antes de un commit)

Regla: edita SIEMPRE la maestra y corre este script. Si editas una copia, el script la pisa.
"""
import filecmp
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SKILLS = RAIZ / "plugins" / "phoenix-os" / "skills"
DIST = RAIZ / "dist"

COPIAS = {
    SKILLS / "adaptador/references/ficha-marca.md": [
        SKILLS / f"{s}/references/ficha-marca.md"
        for s in ("carrusel-tryhard", "creador-de-guiones", "guion-broll", "historias", "calendario-contenido")
    ],
}
for nombre in ("efectos.py", "fuentes.py", "render.py"):
    COPIAS[SKILLS / "carrusel-tryhard/scripts" / nombre] = [SKILLS / "historias/scripts" / nombre]

IGNORAR = {"__pycache__", ".DS_Store"}


def revisar():
    malas = [c for m, cs in COPIAS.items() for c in cs if not c.exists() or not filecmp.cmp(m, c, shallow=False)]
    for c in malas:
        print(f"  DISTINTA o FALTA: {c.relative_to(RAIZ)}")
    return not malas


def copiar():
    for maestra, copias in COPIAS.items():
        for c in copias:
            c.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(maestra, c)
    print("Copias sincronizadas.")


def validar():
    ok = True
    validador = Path("/mnt/skills/examples/skill-creator/scripts/quick_validate.py")
    for d in sorted(p for p in SKILLS.iterdir() if p.is_dir()):
        if validador.exists():
            r = subprocess.run([sys.executable, str(validador), str(d)], capture_output=True, text=True)
            estado = r.stdout.strip() or r.stderr.strip()
            ok &= r.returncode == 0
        else:
            estado = "SKILL.md presente" if (d / "SKILL.md").exists() else "FALTA SKILL.md"
            ok &= (d / "SKILL.md").exists()
        print(f"  {d.name:22s} {estado}")
    return ok


def empaquetar():
    DIST.mkdir(exist_ok=True)
    for d in sorted(p for p in SKILLS.iterdir() if p.is_dir()):
        destino = DIST / f"{d.name}.zip"
        with zipfile.ZipFile(destino, "w", zipfile.ZIP_DEFLATED) as z:
            for f in sorted(d.rglob("*")):
                if f.is_file() and not (IGNORAR & set(f.parts)):
                    z.write(f, f"{d.name}/{f.relative_to(d)}")
        print(f"  dist/{destino.name}  ({destino.stat().st_size / 1024:.0f} KB)")


def main():
    if "--revisar" in sys.argv:
        bien = revisar()
        print("Todo igual." if bien else "Hay copias desactualizadas: corre python herramientas/sincronizar.py")
        sys.exit(0 if bien else 1)
    copiar()
    print("Validando skills:")
    if not validar():
        sys.exit("Hay skills inválidas; no se empaqueta.")
    print("Empaquetando:")
    empaquetar()


if __name__ == "__main__":
    main()
