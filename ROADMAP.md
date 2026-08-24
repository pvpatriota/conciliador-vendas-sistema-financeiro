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
