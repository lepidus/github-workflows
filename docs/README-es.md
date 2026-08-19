# github-workflows

[English](../README.md) | [Português Brasileiro](README-pt_BR.md) | **Español**

Workflows reutilizables de GitHub Actions para plugins de Lepidus.

## Workflows disponibles

### `generate-package.yml`

Valida el `version.xml`, genera un paquete `.tar.gz` y publica una release completa en inglés al crear una etiqueta. La descripción de la release contiene metadatos de compatibilidad, cambios generados automáticamente e instrucciones de instalación.

**Validaciones realizadas:**
- El campo `application` del `version.xml` corresponde al nombre del plugin
- El campo `release` corresponde exactamente a la etiqueta creada sin el prefijo `v`
- El campo `date` corresponde a la fecha actual

**Archivos excluidos del paquete:**
`.agents`, `.codex`, `.gitattributes`, `.github`, `.gitignore`, `.gitlab-ci.yml`, `.gitmodules`, `AGENTS.md`, `CLAUDE.md`, `tests`, `cypress`, `resources`, `package.json`, `package-lock.json`, `vite.config.js`, `i18nExtractKeys.vite.js`

#### Cómo usar

En el repositorio del plugin, cree `.github/workflows/generate-package.yml`:

```yaml
on:
  push:
    tags:
      - 'v*'

name: Create release and tar.gz package for it

jobs:
  create-release:
    uses: lepidus/github-workflows/.github/workflows/generate-package.yml@main
    with:
      plugin_name: nombreDeSuPlugin
      pkp_application: OJS
      compatible_versions: OJS 3.5.x
      release_branch: stable-3_5_0
    permissions:
      contents: write
```

#### Requisitos

- El repositorio debe tener un archivo `version.xml` en la raíz con los campos `application`, `release` y `date`
- Las etiquetas deben seguir el patrón `v*` (ej: `v1.0.0.0`)
- `plugin_name` es obligatorio y debe corresponder a `version/application`
- Las entradas de compatibilidad mantienen los metadatos correctos y son muy recomendables:
  - `pkp_application`: aplicación PKP compatible, como `OJS`, `OMP` u `OPS`
  - `compatible_versions`: versiones compatibles de la aplicación, como `OJS 3.5.x`
  - `release_branch`: rama desde la cual se preparó la release, como `stable-3_5_0`
- Los workflows existentes que solo envían `plugin_name` siguen siendo compatibles. Los valores de compatibilidad y la rama de la release ausentes se identifican en inglés como no especificados, en lugar de inferirse
- El workflow llamador debe conceder el permiso `contents: write` para que el workflow cree la release y suba el paquete
