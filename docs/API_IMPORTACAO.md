# Importação direta via API (Fase 3) — design

Como o botão **"Confirmar e importar"** vai criar os lançamentos direto no sistema
financeiro, sem importação manual de planilha. Baseado no schema oficial da API
Financeiro (v1). Ver [ROADMAP.md](../ROADMAP.md) e [APIS.md](APIS.md).

## Autenticação (OAuth 2.0)

- Fluxo *Authorization Code*.
- Autorização: `https://auth.contaazul.com/oauth2/authorize`
- Token: `https://auth.contaazul.com/oauth2/token`
- Header nas chamadas: `Authorization: Bearer <access_token>`
- Cada **empresa** autoriza uma vez; guardar `refresh_token` para renovar.

## Endpoint de criação

`POST /v1/financeiro/eventos-financeiros/contas-a-receber` (base `https://api-v2.contaazul.com`)

### Corpo (campos obrigatórios marcados com \*)

```
* data_competencia   string  (data)
* valor              number
* observacao         string
* descricao          string
* contato            string  (ID do cliente/contato)      <-- exige lookup
* conta_financeira   string  (ID da conta financeira)     <-- exige lookup
  rateio             array   (categoria + centro de custo)
* condicao_pagamento { parcelas: [ ... ] }
```

### Parcela (dentro de `condicao_pagamento.parcelas`)

```
* descricao          string
* data_vencimento    string (data)
* nota               string
* conta_financeira   string (ID)
* detalhe_valor      ComposicaoValor { *valor_bruto, valor_liquido, taxa, desconto, juros, multa }
  metodo_pagamento   enum (DINHEIRO | CARTAO_CREDITO | CARTAO_DEBITO |
                            PIX_PAGAMENTO_INSTANTANEO | OUTRO | ...)
```

## De-para: planilha → payload

| Coluna da planilha | Campo na API |
|---|---|
| Data de Competência | `data_competencia` |
| Valor | `valor` e `parcelas[0].detalhe_valor.valor_bruto` |
| Descrição | `descricao` e `parcelas[0].descricao` |
| Data de Vencimento | `parcelas[0].data_vencimento` |
| (taxa, extraída da descrição) | `parcelas[0].detalhe_valor.taxa` |
| Categoria (Visa/PIX/Dinheiro/…) | `rateio[0].id_categoria` **(resolver nome → id)** |
| forma de pagamento | `parcelas[0].metodo_pagamento` |
| — | `contato` **(cliente padrão)** |
| — | `conta_financeira` **(conta que recebe)** |

Datas provavelmente em `aaaa-mm-dd` (converter do `dd/mm/aaaa` das planilhas —
confirmar no primeiro POST real). NSU **não** existe no corpo de criação; segue na
`descricao`/`nota` (como já fazemos) ou via `PATCH` de parcela depois, se preciso.

### metodo_pagamento por forma

| Forma | enum |
|---|---|
| Débito | `CARTAO_DEBITO` |
| Crédito | `CARTAO_CREDITO` |
| PIX | `PIX_PAGAMENTO_INSTANTANEO` |
| Dinheiro | `DINHEIRO` |
| iFood / Hanzo | `OUTRO` |

## Exemplo de payload (uma venda de débito)

```json
{
  "data_competencia": "2026-05-01",
  "valor": 173.59,
  "descricao": "Taxa/Tarifa: R$ -1.74 | NSU: 138799",
  "observacao": "Importado via Conciliador SEVENT",
  "contato": "<id-do-cliente-padrao>",
  "conta_financeira": "<id-da-conta>",
  "rateio": [{ "id_categoria": "<id-categoria-Visa>", "valor": 173.59 }],
  "condicao_pagamento": {
    "parcelas": [{
      "descricao": "Taxa/Tarifa: R$ -1.74 | NSU: 138799",
      "data_vencimento": "2026-05-04",
      "nota": "",
      "conta_financeira": "<id-da-conta>",
      "detalhe_valor": { "valor_bruto": 173.59, "taxa": 1.74 },
      "metodo_pagamento": "CARTAO_DEBITO"
    }]
  }
}
```

## Configuração única (obtida por GET, uma vez por empresa)

Estes IDs a API exige mas as planilhas não têm — resolvemos uma vez e guardamos:

1. **`conta_financeira`** — `GET /v1/conta-financeira` → escolher a conta que recebe
   (ex.: a conta da adquirente/banco). Um ID.
2. **`contato` (cliente padrão)** — a criação exige um cliente. Definir um contato
   padrão (ex.: "Consumidor" ou o nome do canal) e usar o ID dele em todos os
   lançamentos. (API de contatos/pessoas.)
3. **De-para de categorias** — `GET /v1/categorias` → mapear cada `Categoria` da
   planilha (Visa, Mastercard, Elo, PIX, Dinheiro, Hanzo Prod, Ifood) para o
   `id_categoria` correspondente. Guardar o de-para.

## Rate limit e idempotência

- **Rate limit** ~50 req/min, 10/s → enviar em lotes com *throttling* (~1 req a cada
  1,2 s) e *backoff* em 429.
- **Idempotência** — evitar duplicar se o usuário clicar "importar" duas vezes:
  registrar (por empresa + mês + forma) o que já foi enviado e bloquear reenvio;
  idealmente uma chave por lançamento (NSU/pedido + data + valor).

## Limite conhecido

Criar lançamento ✅. **Baixa/conciliação** (marcar como recebido) **não** tem
endpoint de criação — continua como Fase 4 (agente). "Importar" aqui = criar as
contas a receber, prontas para conciliar.

## O que depende de Paulo (envolve login/credenciais)

1. Criar o app no **Portal de Desenvolvedores** do Conta Azul → `client_id` /
   `client_secret` + URL de redirecionamento (callback).
2. Autorizar a empresa (fluxo OAuth) na primeira execução.
3. Escolher a **conta financeira** que recebe e o **cliente padrão**.
