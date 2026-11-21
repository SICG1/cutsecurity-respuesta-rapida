# Respuesta rápida Cut Security

[![Validar kits](https://github.com/SICG1/cutsecurity-respuesta-rapida/actions/workflows/validar.yml/badge.svg)](https://github.com/SICG1/cutsecurity-respuesta-rapida/actions/workflows/validar.yml)
![STIX 2.1](https://img.shields.io/badge/indicadores-STIX%202.1-5B2D8E)
![Sigma](https://img.shields.io/badge/detecciones-Sigma%20%C2%B7%20Wazuh%20%C2%B7%20KQL%20%C2%B7%20SPL-1B2240)

Kits listos para revisar sus equipos cuando una vulnerabilidad empieza a explotarse.

Cada vez que aparece una vulnerabilidad grave, cada equipo de seguridad repite el mismo trabajo. Lee los informes,
extrae los indicadores, escribe las búsquedas y adapta las reglas a su SIEM. Este repositorio entrega ese trabajo hecho.
Cut Security prepara cada kit desde las fuentes primarias y lo publica junto a la alerta en su comunidad:
https://cutsecurity.cl/comunidad

## Kits disponibles

<!-- indice:inicio -->
| Kit | CVE | Severidad | KEV | Versión |
|---|---|---|---|---|
| [VMware vCenter Server](kits/vmware-vcenter-cve-2026-123890/) | CVE-2026-123890 | Crítica | 2026-11-20 | 1.1.0 |
<!-- indice:fin -->

## Qué trae cada kit

| Pieza | Formato | Para qué |
|---|---|---|
| Guía | `README.md` | Prioridad, versiones corregidas, pasos, qué hacer si hay indicadores y plazos de la Ley 21.663. |
| Metadatos | `kit.yaml` | CVE, CVSS, EPSS, KEV, versiones y fuentes, legibles por máquina. |
| Verificadores | Bash, PowerShell 5.1/7, Python 3.10+ | Revisan un equipo en una pasada. Solo leen. |
| Detecciones | Sigma, Wazuh, KQL, SPL | Reglas para su SIEM, solo cuando las fuentes dan base. |
| Indicadores | CSV y STIX 2.1 | Para cortafuegos, filtros, SIEM y plataformas de inteligencia (MISP, OpenCTI). |
| Huellas | `SHA256SUMS` | Comprueban que nadie alteró un archivo. |

## Cómo usar un kit con seguridad

1. Descargue el zip del kit desde «Releases» y compare su huella con el `SHA256SUMS` de la versión.
2. Descomprímalo y compruebe cada archivo: `sha256sum -c SHA256SUMS`.
3. Lea cada guion antes de ejecutarlo. Los verificadores solo leen: no modifican, no borran y no envían datos.
4. Cada hallazgo sale como una línea `cutsec-kit <cve> hallazgo=<tipo> detalle=<texto>`, lista para su SIEM.
   Código de salida: 0 sin indicadores, 2 con indicadores, 1 no se pudo revisar.
5. Revise la sección «Límites del kit» de cada guía.

## Cómo se arma un kit

Todos los kits siguen el [estándar de los kits](docs/ESTANDAR-DE-KITS.md). Sus reglas centrales:

- Nada inventado: cada versión, ruta, indicador o regla sale de una fuente que se leyó. Manda el fabricante.
- Solo lectura: ningún verificador cambia, borra, instala o envía algo.
- Prueba declarada: cada kit dice qué se probó y cómo, en su guía y en su `kit.yaml`.

Cada cambio pasa por una validación automática: esquema de los metadatos, huellas, ShellCheck, PSScriptAnalyzer,
reglas Sigma con pySigma y YAML. Para validar en su equipo:

```bash
pip install pyyaml jsonschema
python tools/kits.py validar
```

## Alcance

Un resultado limpio no prueba que un equipo esté sano: los atacantes borran rastros y cambian nombres de archivo.
Los kits se entregan tal cual, sin garantía. Cada organización decide y aplica los cambios en sus propios equipos.

## Errores y mejoras

¿Encontró un error, un falso positivo o una fuente nueva? Abra un issue. Para reportar una vulnerabilidad en este
repositorio, siga [SECURITY.md](SECURITY.md).
