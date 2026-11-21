# Cambios

## v2026.11.21

- Estándar 2.0 de los kits (`docs/ESTANDAR-DE-KITS.md`): estructura por carpetas, `kit.yaml` validado por esquema,
  verificadores de solo lectura con salida legible por máquina, detecciones Sigma, Wazuh, KQL y SPL, indicadores en
  CSV y STIX 2.1, y huellas `SHA256SUMS`.
- Validación con `tools/kits.py validar`: esquema, huellas, sintaxis de los guiones, STIX, pySigma y yamllint. El flujo
  de GitHub Actions suma ShellCheck y PSScriptAnalyzer. Versiones empaquetadas con un zip por kit.
- VMware vCenter CVE-2026-123890 pasa a la versión 1.1.0: estructura nueva e indicadores en STIX 2.1.
- Ocho kits nuevos, todos en la versión 1.0.0 y con explotación confirmada por CISA (KEV):
  - Apache Roller CVE-2026-129448 y CVE-2026-82384: XML-RPC con ejecución remota sin clave.
  - Barracuda Email Security Gateway CVE-2026-116606 y CVE-2026-111560.
  - BeyondTrust Remote Support CVE-2026-102764: día cero de ARMORY CASTLE antes del salto a vCenter.
  - Check Point Gaia CVE-2026-123039: PHP2Shell en las pasarelas, puerta trasera TSGA y borrado en ESXi.
  - Cisco Expressway CVE-2026-76466: credencial fija en el clúster, puertos TCP 4371 y 4372.
  - GitLab CVE-2026-97229, con la revisión del Ruby propio en instalaciones desde el código fuente.
  - OpenSSH CVE-2026-123158 («SSHole») en Linux con musl y sin PAM, como Alpine.
  - PHP CVE-2026-109618 (PHP2Shell) y la tanda de correcciones de PHP del 19-11-2026.
- Los verificadores no ejecutan programas encontrados en carpetas que otro usuario pueda escribir. En Windows la
  versión de PHP se lee de los metadatos del archivo.

## v2026.11.20

- Primer kit: VMware vCenter CVE-2026-123890 (ARMORY CASTLE), versión 1.0.
