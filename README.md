# Respuesta rápida Cut Security

Kits listos para revisar sus equipos cuando una vulnerabilidad empieza a explotarse.

Cada vez que aparece una vulnerabilidad grave, cada equipo de seguridad repite el mismo trabajo. Lee los informes,
extrae los indicadores, escribe las búsquedas y adapta las reglas a su SIEM. Este repositorio entrega ese trabajo hecho.
Cut Security prepara cada kit desde las fuentes primarias y lo publica junto a la alerta en su comunidad:
https://cutsecurity.cl/comunidad

## Qué trae cada kit

- Un verificador de solo lectura para ejecutar en los equipos expuestos.
- Los indicadores de compromiso en CSV, para importar, y en Excel, para revisar.
- Reglas de detección en formato Sigma y para Wazuh.
- Una guía en español con la prioridad, los pasos y qué hacer si aparecen indicadores.
- Los plazos para reportar al CSIRT Nacional según la Ley 21.663.
- La huella SHA-256 de cada archivo.

## Kits disponibles

| Publicado | Producto | Vulnerabilidad | Descarga |
|---|---|---|---|
| 20-11-2026 | [VMware vCenter](Kit%20de%20respuesta%20VMware%20vCenter%20CVE-2026-123890/) | CVE-2026-123890, explotada por el grupo ARMORY CASTLE | [Versión 1.0](https://github.com/SICG1/cutsecurity-respuesta-rapida/releases/tag/vcenter-cve-2026-123890-v1.0) |

## Cómo usar un kit con seguridad

1. Descargue el zip desde «Releases». Compare su huella SHA-256 con la que publica la versión.
2. Descomprímalo y compruebe cada archivo con `sha256sum -c "Huellas SHA-256.txt"`.
3. Lea cada guion antes de ejecutarlo. Los verificadores solo leen: no modifican, no borran y no envían datos.
4. Revise la sección «Límites del kit» de la guía.

## Alcance

Un resultado limpio no prueba que un equipo esté sano: los atacantes borran rastros y cambian nombres de archivo.
Los kits se entregan tal cual, sin garantía. Cada organización decide y aplica los cambios en sus propios equipos.

## Errores y mejoras

¿Encontró un error o un falso positivo? Abra un issue en este repositorio o comente la alerta en la comunidad.
