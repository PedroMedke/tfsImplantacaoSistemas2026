# Healthchecks

O sistema usa configuração YAML para executar healthchecks de diferentes tipos:
- HTTP
- Database
- TCP

Os healthchecks são definidos em `config/healthchecks.yml` e suportam intervalos, timeout e retries.

O monitor de saúde registra métricas em banco de dados e envia alertas quando há falhas.
