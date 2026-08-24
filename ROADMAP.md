# Roadmap

## Fase 1 — Pipeline por arquivos ✅ (concluída)

- [x] Leitura das três fontes com detecção dinâmica de layout
- [x] Filtro de vendas efetivadas
- [x] Normalização para modelo único
- [x] Conciliação marketplace × PDV por valor
- [x] Conversão para o modelo de importação do sistema financeiro (6 formas)
- [x] Planilha de divergências
- [x] Validação em 3 meses reais + verificação de integridade

## Fase 2 — Empacotamento em Docker (on-premise)

- [ ] Imagem Docker com o pipeline e agendamento interno
- [ ] Execução na VM/rede do cliente (apenas chamadas de saída)
- [ ] Pasta de entrada monitorada + pasta de saída
- [ ] Logs e idempotência (não reprocessar o mesmo período)

Objetivo: os dados financeiros permanecem no ambiente do cliente; nenhuma porta de
entrada exposta.

Plano detalhado em [docs/DEPLOY_DOCKER.md](docs/DEPLOY_DOCKER.md).

## Fase 2b — Interface web (upload → processa → download)

Uma alternativa/complemento à execução por linha de comando: uma página onde o
usuário **anexa os relatórios do mês**, o pipeline processa no servidor e devolve as
**planilhas prontas** (e a de divergências) para download — sem o usuário tocar em
terminal.

- [ ] Front-end simples de upload (arrastar/soltar os 3 relatórios)
- [ ] Back-end que roda o pipeline e devolve os arquivos (download individual ou .zip)
- [ ] Validação de entrada (arquivos corretos, mês reconhecido) e mensagens de erro
- [ ] Sem persistência de dados sensíveis (processa e descarta; nada fica no servidor)
- [ ] Reaproveita o mesmo núcleo `src/gerar_planilhas.py`

Objetivo: facilitar a interação para usuários não técnicos. Decisões em aberto:
stack (ex.: Flask/FastAPI + HTML simples), onde hospedar (on-premise vs. nuvem) e
política de retenção — a definir no planejamento desta fase.

## Fase 3 — Integração com a API do sistema financeiro

- [ ] Autenticação OAuth 2.0
- [ ] Criação de lançamentos (contas a receber) via API
- [ ] Ajuste de datas/taxas via `PATCH` de parcela
- [ ] Sincronização por *polling* (a API não tem webhook)

## Fase 4 — Agente de conciliação

- [ ] Agente de navegador (headless) para a **baixa/conciliação** que a API não
      expõe
- [ ] Fluxo com aprovação humana para ações irreversíveis
- [ ] Preenchimento da *Data de Pagamento* no momento da conciliação

## Fase 5 — Conferência ao vivo (fontes via API)

- [ ] Consumir marketplace e adquirente por API (em vez de exports manuais)
- [ ] Relatórios de conciliação recorrentes e alertas de divergência
