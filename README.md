# Kits de respuesta de Cut Security

Cada kit responde a una vulnerabilidad que se está explotando. Trae lo necesario para revisar los equipos en una sola
pasada: un verificador de solo lectura, los indicadores de compromiso, reglas de detección y una guía en español.

Los kits se publican junto a la alerta correspondiente en la comunidad de Cut Security: https://cutsecurity.cl/comunidad

## Kits publicados

| Fecha | Kit | Vulnerabilidad | Descarga |
|---|---|---|---|
| 20-11-2026 | [VMware vCenter](Kit%20de%20respuesta%20VMware%20vCenter%20CVE-2026-123890/) | CVE-2026-123890, explotada por ARMORY CASTLE | [Versión 1.0](https://github.com/SICG1/kits-de-respuesta/releases/tag/vcenter-cve-2026-123890-v1.0) |

## Antes de usar un kit

1. Descargue el zip desde la sección «Releases» y compare su huella SHA-256 con la que publica la versión.
2. Dentro del kit, compruebe cada archivo: `sha256sum -c "Huellas SHA-256.txt"`.
3. Lea cada guion antes de ejecutarlo. Los verificadores solo leen: no cambian, no borran y no envían datos.
4. Lea la sección «Límites del kit» de la guía. Un resultado limpio no prueba que un equipo esté sano.

## Uso

Los kits se entregan tal cual, sin garantía. Cada organización decide y aplica los cambios en sus equipos.
Las fuentes de cada indicador se citan en la guía y en la planilla de indicadores.
