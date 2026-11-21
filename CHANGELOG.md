# Cambios

## v2026.11.21

- Estándar 2.0 de los kits (`docs/ESTANDAR-DE-KITS.md`): estructura por carpetas, `kit.yaml` validado por esquema,
  verificadores de solo lectura con salida legible por máquina, detecciones Sigma, Wazuh, KQL y SPL, indicadores en
  CSV y STIX 2.1, y huellas `SHA256SUMS`.
- Validación automática en cada cambio (GitHub Actions): esquema, huellas, ShellCheck, PSScriptAnalyzer, pySigma y
  yamllint. Versiones empaquetadas con un zip por kit.
- VMware vCenter CVE-2026-123890 pasa a la versión 1.1.0: estructura nueva e indicadores en STIX 2.1.

## v2026.11.20

- Primer kit: VMware vCenter CVE-2026-123890 (ARMORY CASTLE), versión 1.0.
