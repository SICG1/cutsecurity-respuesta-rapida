#!/usr/bin/env python3
"""Herramienta del repositorio: valida los kits, regenera el índice del README y empaqueta cada kit.

    python tools/kits.py validar          # esquema de kit.yaml, archivos obligatorios, huellas, sintaxis
    python tools/kits.py indice           # reescribe la tabla de kits del README entre sus marcas
    python tools/kits.py empaquetar dist  # un zip por kit y SHA256SUMS de los zip, para la versión

Requiere Python 3.10+ y, para validar, PyYAML y jsonschema (pip install pyyaml jsonschema).
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import zipfile
from dataclasses import dataclass
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
KITS = RAIZ / "kits"
OBLIGATORIOS = ("README.md", "kit.yaml", "SHA256SUMS")
MARCA_INICIO = "<!-- indice:inicio -->"
MARCA_FIN = "<!-- indice:fin -->"
SEVERIDAD = {"critica": "Crítica", "alta": "Alta", "media": "Media"}


@dataclass(frozen=True)
class Kit:
    carpeta: Path
    meta: dict

    @property
    def id(self) -> str:
        return self.meta["id"]


def leer_kits() -> list[Kit]:
    import yaml  # noqa: PLC0415 (solo hace falta aquí)

    kits = []
    for carpeta in sorted(p for p in KITS.iterdir() if p.is_dir()):
        archivo = carpeta / "kit.yaml"
        # Una carpeta sin kit.yaml es un kit en preparación: se informa, no rompe la validación de los demás.
        meta = yaml.safe_load(archivo.read_text(encoding="utf-8")) if archivo.is_file() else {"id": None}
        kits.append(Kit(carpeta, meta))
    return kits


def sha256(ruta: Path) -> str:
    return hashlib.sha256(ruta.read_bytes()).hexdigest()


def errores_de(kit: Kit, esquema: dict) -> list[str]:
    import jsonschema  # noqa: PLC0415

    errores: list[str] = []
    nombre = kit.carpeta.name
    if kit.meta.get("id") is None:
        return [f"{nombre}: falta kit.yaml (kit en preparación)"]
    for archivo in OBLIGATORIOS:
        if not (kit.carpeta / archivo).is_file():
            errores.append(f"{nombre}: falta {archivo}")
    if not any((kit.carpeta / "verificar").glob("*")):
        errores.append(f"{nombre}: falta al menos un guion en verificar/")
    meta = json.loads(json.dumps(kit.meta, default=str))  # fechas de YAML -> texto
    for e in jsonschema.Draft202012Validator(esquema).iter_errors(meta):
        errores.append(f"{nombre}: kit.yaml {'/'.join(map(str, e.path)) or '(raíz)'}: {e.message}")
    if kit.meta.get("id") != nombre:
        errores.append(f"{nombre}: el id de kit.yaml ({kit.meta.get('id')}) no coincide con la carpeta")
    # Huellas: cada archivo del kit (salvo SHA256SUMS) aparece y coincide.
    sumas = kit.carpeta / "SHA256SUMS"
    if sumas.is_file():
        declaradas = {}
        for linea in sumas.read_text(encoding="utf-8").splitlines():
            if linea.strip():
                huella, ruta = linea.split(maxsplit=1)
                declaradas[ruta.lstrip("*").removeprefix("./")] = huella
        reales = {
            p.relative_to(kit.carpeta).as_posix(): sha256(p)
            for p in kit.carpeta.rglob("*")
            if p.is_file() and p.name != "SHA256SUMS" and "__pycache__" not in p.parts
        }
        for ruta, huella in reales.items():
            if declaradas.get(ruta) != huella:
                errores.append(f"{nombre}: la huella de {ruta} no coincide o falta en SHA256SUMS")
        for ruta in declaradas.keys() - reales.keys():
            errores.append(f"{nombre}: SHA256SUMS nombra {ruta}, que no existe")
    # Sintaxis de los guiones.
    for guion in kit.carpeta.rglob("*.sh"):
        # Ruta relativa y cwd en la raíz: así funciona con el bash de Linux y con el de WSL en Windows.
        relativa = guion.relative_to(RAIZ).as_posix()
        if subprocess.run(["bash", "-n", relativa], capture_output=True, cwd=RAIZ).returncode != 0:
            errores.append(f"{nombre}: error de sintaxis en {guion.name}")
    for guion in kit.carpeta.rglob("*.py"):
        # compile() en memoria: py_compile dejaría __pycache__ dentro del kit y rompería sus huellas.
        try:
            compile(guion.read_text(encoding="utf-8"), str(guion), "exec")
        except SyntaxError:
            errores.append(f"{nombre}: error de sintaxis en {guion.name}")
    for stix in kit.carpeta.rglob("*.stix.json"):
        datos = json.loads(stix.read_text(encoding="utf-8"))
        if datos.get("type") != "bundle" or not all("spec_version" in o for o in datos.get("objects", [])):
            errores.append(f"{nombre}: {stix.name} no es un paquete STIX 2.1 válido")
    return errores


def validar() -> int:
    esquema = json.loads((RAIZ / "schema" / "kit.schema.json").read_text(encoding="utf-8"))
    kits = leer_kits()
    errores = [e for k in kits for e in errores_de(k, esquema)]
    for e in errores:
        print(f"::error::{e}")
    print(f"{len(kits)} kits revisados, {len(errores)} errores")
    return 1 if errores else 0


def indice() -> int:
    filas = ["| Kit | CVE | Severidad | KEV | Versión |", "|---|---|---|---|---|"]
    for k in sorted(leer_kits(), key=lambda k: str(k.meta.get("publicado")), reverse=True):
        m = k.meta
        kev = (m.get("kev") or {}).get("agregada", "—")
        cves = ", ".join(m["cves"])
        filas.append(
            f"| [{m['producto']}](kits/{k.id}/) | {cves} | {SEVERIDAD.get(m['severidad'], m['severidad'])} "
            f"| {kev} | {m['version']} |"
        )
    readme = RAIZ / "README.md"
    texto = readme.read_text(encoding="utf-8")
    inicio, fin = texto.index(MARCA_INICIO) + len(MARCA_INICIO), texto.index(MARCA_FIN)
    readme.write_text(texto[:inicio] + "\n" + "\n".join(filas) + "\n" + texto[fin:], encoding="utf-8", newline="\n")  # LF también en Windows: sha256sum -c no lee CRLF
    print(f"índice con {len(filas) - 2} kits")
    return 0


def empaquetar(destino: str) -> int:
    salida = RAIZ / destino
    salida.mkdir(parents=True, exist_ok=True)
    lineas = []
    for k in leer_kits():
        zip_ruta = salida / f"{k.id}-v{k.meta['version']}.zip"
        with zipfile.ZipFile(zip_ruta, "w", zipfile.ZIP_DEFLATED) as z:
            for p in sorted(k.carpeta.rglob("*")):
                if p.is_file():
                    z.write(p, f"{k.id}/{p.relative_to(k.carpeta).as_posix()}")
        lineas.append(f"{sha256(zip_ruta)}  {zip_ruta.name}")
    (salida / "SHA256SUMS").write_text("\n".join(lineas) + "\n", encoding="utf-8", newline="\n")  # LF también en Windows: sha256sum -c no lee CRLF
    print("\n".join(lineas))
    return 0


if __name__ == "__main__":
    orden = sys.argv[1] if len(sys.argv) > 1 else ""
    if orden == "validar":
        sys.exit(validar())
    if orden == "indice":
        sys.exit(indice())
    if orden == "empaquetar" and len(sys.argv) > 2:
        sys.exit(empaquetar(sys.argv[2]))
    sys.exit(__doc__)
