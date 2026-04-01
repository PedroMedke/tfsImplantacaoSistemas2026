# Automação

O projeto inclui scripts para build, deploy, rollback, backup e limpeza de recursos.

- `./scripts/build.sh`: valida o ambiente e constrói imagens Docker.
- `./scripts/deploy.sh`: cria backup, executa healthchecks e sobe containers com zero downtime.
- `./scripts/rollback.sh`: restaura configurações e banco a partir de um backup.
- `./scripts/backup.sh`: copia arquivos de configuração e chamadores de dump do banco.
- `./scripts/cleanup.sh`: remove containers e imagens não utilizados.
