# github-workflows

[English](../README.md) | **Português Brasileiro** | [Español](README-es.md)

Workflows reutilizáveis do GitHub Actions para plugins da Lepidus.

## Workflows disponíveis

### `generate-package.yml`

Valida o `version.xml`, gera um pacote `.tar.gz` e publica uma release completa em inglês ao criar uma tag. A descrição da release contém metadados de compatibilidade, alterações geradas automaticamente e instruções de instalação.

**Validações realizadas:**
- O campo `application` do `version.xml` corresponde ao nome do plugin
- O campo `release` corresponde exatamente à tag criada sem o prefixo `v`
- O campo `date` corresponde à data atual

**Arquivos excluídos do pacote:**
`.agents`, `.codex`, `.gitattributes`, `.github`, `.gitignore`, `.gitlab-ci.yml`, `.gitmodules`, `AGENTS.md`, `CLAUDE.md`, `tests`, `cypress`, `resources`, `package.json`, `package-lock.json`, `vite.config.js`, `i18nExtractKeys.vite.js`

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
      pkp_application: OJS
      compatible_versions: OJS 3.5.x
      release_branch: stable-3_5_0
    permissions:
      contents: write
```

#### Pré-requisitos

- O repositório deve ter um arquivo `version.xml` na raiz com os campos `application`, `release` e `date`
- As tags devem seguir o padrão `v*` (ex: `v1.0.0.0`)
- `plugin_name` é obrigatório e deve corresponder a `version/application`
- As entradas de compatibilidade mantêm os metadados corretos e são fortemente recomendadas:
  - `pkp_application`: aplicação PKP compatível, como `OJS`, `OMP` ou `OPS`
  - `compatible_versions`: versões compatíveis da aplicação, como `OJS 3.5.x`
  - `release_branch`: ramo a partir do qual a release foi preparada, como `stable-3_5_0`
- Chamadores existentes que informam apenas `plugin_name` permanecem compatíveis. Valores de compatibilidade e o ramo da release ausentes são identificados em inglês como não informados, em vez de serem inferidos
- O chamador deve conceder a permissão `contents: write` para que o workflow crie a release e envie o pacote
