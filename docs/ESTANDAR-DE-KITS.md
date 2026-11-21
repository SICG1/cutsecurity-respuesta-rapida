# Estándar de los kits de respuesta rápida

Versión 2.0 · 21-11-2026 · Cut Security

Este documento fija cómo se arma cada kit. Un kit que no cumple este estándar no se publica.

## 1. Para quién y para qué

El lector es un equipo de seguridad o de TI de una empresa en Chile, con criterio técnico y poco tiempo. Un kit le
permite responder en una sola pasada a una vulnerabilidad que se está explotando: saber si está expuesto, buscar
señales de compromiso, aplicar la corrección y dejar evidencia.

## 2. Qué vulnerabilidades entran

1. Explotación confirmada: está en el catálogo KEV de CISA, o el fabricante o un equipo de respuesta nacional confirman
   ataques reales.
2. Producto de uso común en empresas o en el Estado.
3. Hay algo concreto que verificar o detectar: versión, archivo, ruta, puerto, registro o comportamiento.

## 3. Estructura de carpetas

```
kits/<producto>-<cve>/            minúsculas, sin tildes, palabras unidas por guiones
├── README.md                     la guía del kit (sección 5)
├── kit.yaml                      metadatos (sección 4), validados por schema/kit.schema.json
├── verificar/                    guiones de solo lectura
│   ├── verificar.sh              Bash: set -Eeuo pipefail, sin dependencias fuera de coreutils
│   ├── verificar.ps1             PowerShell 7+ y Windows PowerShell 5.1, solo ASCII
│   └── verificar.py              Python 3.10+ con tipos, solo biblioteca estándar
├── detecciones/                  solo lo que las fuentes respaldan
│   ├── sigma/*.yml               Sigma con id UUID, status: experimental, level, falsepositives
│   ├── wazuh/*.xml               reglas con id en el rango 119000-119999
│   ├── kql/*.kql                 Microsoft Sentinel / Defender
│   └── spl/*.spl                 Splunk
├── indicadores/
│   ├── indicadores.csv           prioridad,tipo,indicador,accion,descripcion,fuente
│   └── indicadores.stix.json     paquete STIX 2.1 (solo si hay indicadores de compromiso publicados)
└── SHA256SUMS                    huella de cada archivo del kit (formato de sha256sum)
```

No todos los archivos son obligatorios: los obligatorios son `README.md`, `kit.yaml`, `SHA256SUMS` y al menos un
guion en `verificar/`. Un formato de detección sin base en las fuentes no se incluye: mejor ausente que inventado.

## 4. kit.yaml

```yaml
id: php-cve-2026-109618
titulo: Kit de respuesta para PHP2Shell (CVE-2026-109618 y CVE-2026-109619)
version: 1.0.0
publicado: 2026-11-21
cves: [CVE-2026-109618, CVE-2026-109619]
producto: PHP
fabricante: PHP Group
severidad: critica            # critica | alta | media
cvss: {puntaje: 9.8, vector: "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H", fuente: NVD}
epss: {probabilidad: 0.99999, percentil: 0.99999, fecha: 2026-11-20}
kev: {agregada: 2026-10-26, plazo_federal: 2026-10-29, ransomware: false}
versiones_afectadas: ["..."]
versiones_corregidas: ["..."]
mitigacion_temporal: "texto o null si el fabricante no da ninguna"
pruebas:                      # lo que de verdad se probó; nunca más de lo hecho
  verificador: "simulado | real | no probado"
  detecciones: "sintaxis validada | probadas en SIEM | no probadas"
fuentes:
  - {titulo: "...", url: "https://...", tipo: fabricante|cert|investigador|cisa|medio, consultada: 2026-11-21}
```

## 5. README.md del kit (la guía)

En español de Chile, frases de menos de 25 palabras, sujeto y verbo de acción. Secciones, en este orden:

1. **Título** («Kit de respuesta para <producto> (<CVE>)»), versión y fecha.
2. **Prioridad**: urgente, alta o media, con las razones en una lista (KEV, EPSS, CVSS, quién la explota).
3. **Datos clave**: tabla con CVE, producto, tipo, CVSS con vector, EPSS, KEV, explotación, parche.
4. **Versiones afectadas y corregidas**: tabla, tal como las publica el fabricante.
5. **Qué trae el kit**: tabla archivo → para qué → dónde se usa.
6. **Cómo usarlo, paso a paso**: comprobar huellas, leer los guiones, verificar versión, buscar indicadores, cargar
   detecciones, parchar.
7. **Si hay indicadores**: aislar sin apagar, conservar evidencia, rotar credenciales, revisar persistencia.
8. **Ley 21.663**: solo para las instituciones obligadas por su artículo 4°: alerta temprana en 3 horas, actualización
   en 72 horas (24 si es operador de importancia vital y se afectan sus servicios esenciales), informe final en 15 días
   corridos desde la alerta temprana.
9. **Límites del kit**: qué no se probó y qué no detecta. Un resultado limpio no prueba que el equipo esté sano.
10. **Fuentes**: primero las primarias (fabricante, investigador, CISA, CERT), con fecha de consulta.

## 6. Reglas que no se negocian

1. **Nada inventado.** Cada versión, ruta, indicador, puerto o regla sale de una fuente que se leyó. Si un dato no está
   en las fuentes, no va. Si dos fuentes se contradicen, manda el fabricante y se dice.
2. **Solo lectura.** Los verificadores no cambian, no borran, no instalan y no envían nada. Lo declaran al inicio.
3. **Salida legible por máquina.** Cada hallazgo es una línea `cutsec-kit <cve> hallazgo=<tipo> detalle=<texto>`.
   Código de salida: 0 sin indicadores, 2 con indicadores, 1 no se pudo revisar.
4. **Direcciones desarmadas en el texto** (`hxxps`, `[.]`), no en el CSV ni en STIX, que son para importar.
5. **Sin datos de clientes**, sin nombres de personas, sin claves.
6. **Prueba lo que publicas.** `bash -n`, `shellcheck`, el analizador de PowerShell y `python -m py_compile` sin
   errores. Si un verificador se probó en un entorno simulado, se dice así en el README y en `kit.yaml`.
7. **Huellas al final**: `sha256sum` de todos los archivos del kit (salvo `SHA256SUMS`) en `SHA256SUMS`.
