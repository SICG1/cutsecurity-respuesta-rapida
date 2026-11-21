# Cómo contribuir

1. Lea el [estándar de los kits](docs/ESTANDAR-DE-KITS.md). Un kit que no lo cumple no se publica.
2. Cree la carpeta `kits/<producto>-<cve>/` con `README.md`, `kit.yaml`, al menos un guion en `verificar/` y
   `SHA256SUMS`.
3. Pruebe los verificadores en un entorno simulado y anote el resultado real en la guía y en `kit.yaml`.
4. Genere las huellas:
   ```bash
   cd kits/<id> && find . -type f ! -name SHA256SUMS | sed 's|^\./||' | sort | xargs sha256sum > SHA256SUMS
   ```
5. Valide y regenere el índice:
   ```bash
   python tools/kits.py validar
   python tools/kits.py indice
   ```
6. Abra un pull request con las fuentes primarias que leyó.

Cada versión del repositorio se publica con una etiqueta `vAAAA.MM.DD`. El flujo `publicar.yml` empaqueta un zip por
kit y adjunta sus huellas.
