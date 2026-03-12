# github-workflows

[English](../README.md) | **Português Brasileiro** | [Español](README-es.md)

Workflows reutilizáveis do GitHub Actions para plugins da Lepidus.

## Workflows disponíveis

### `generate-package.yml`

Valida o `version.xml` e gera um pacote `.tar.gz` como asset de release ao criar uma tag.

**Validações realizadas:**
- O campo `application` do `version.xml` corresponde ao nome do plugin
- O campo `release` corresponde à tag criada
- O campo `date` corresponde à data atual

**Arquivos excluídos do pacote:**
`tests`, `cypress`, `resources`, `CLAUDE.md`, `package.json`, `package-lock.json`, `vite.config.js`, `i18nExtractKeys.vite.js`

#### Como usar

No repositório do plugin, crie `.github/workflows/generate-package.yml`:

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
      plugin_name: nomeDoseuPlugin
```

#### Pré-requisitos

- O repositório deve ter um arquivo `version.xml` na raiz com os campos `application`, `release` e `date`
- As tags devem seguir o padrão `v*` (ex: `v1.0.0.0`)
