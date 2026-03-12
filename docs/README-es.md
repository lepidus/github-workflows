# github-workflows

[English](/lepidus/github-workflows/blob/main/README.md) | [Português Brasileiro](/lepidus/github-workflows/blob/main/docs/README-pt_BR.md) | **Español**

Workflows reutilizables de GitHub Actions para plugins de Lepidus.

## Workflows disponibles

### `generate-package.yml`

Valida el `version.xml` y genera un paquete `.tar.gz` como asset de release al crear una etiqueta.

**Validaciones realizadas:**
- El campo `application` del `version.xml` corresponde al nombre del plugin
- El campo `release` corresponde a la etiqueta creada
- El campo `date` corresponde a la fecha actual

**Archivos excluidos del paquete:**
`tests`, `cypress`, `resources`, `CLAUDE.md`, `package.json`, `package-lock.json`, `vite.config.js`, `i18nExtractKeys.vite.js`

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
```

#### Requisitos

- El repositorio debe tener un archivo `version.xml` en la raíz con los campos `application`, `release` y `date`
- Las etiquetas deben seguir el patrón `v*` (ej: `v1.0.0.0`)
