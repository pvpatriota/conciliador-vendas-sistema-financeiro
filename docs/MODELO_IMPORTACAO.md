# Modelo de importação (sistema financeiro)

O sistema financeiro importa lançamentos a partir de uma planilha com duas abas:
**`Orientações`** (texto fixo de instruções) e **`Dados`** (os lançamentos).

## Colunas da aba `Dados`

| Coluna | Preenchimento |
|---|---|
| Data de Competência | Data da venda |
| Data de Vencimento | Depende da forma de pagamento (ver tabela) |
| Data de Pagamento | **Sempre em branco** — preenchida no momento da conciliação |
| Valor | Valor bruto da venda |
| Categoria | Depende da forma de pagamento |
| Descrição | Depende da forma de pagamento |
| Cliente/Fornecedor | (vazio) |
| CNPJ/CPF Cliente/Fornecedor | (vazio) |
| Centro de Custo | (vazio) |
| Observações | (vazio) |

> **Regra global:** a *Data de Pagamento* fica **sempre em branco**, mesmo quando a
> data já passou e o valor já foi recebido. Esse campo só é preenchido quando a
> conciliação é efetivada no sistema financeiro.

## Regras por forma de pagamento

| Forma | Fonte | Competência | Vencimento | Categoria | Descrição |
|---|---|---|---|---|---|
| **Débito** | Adquirente | Data da venda | Data prevista de pagamento do adquirente | Bandeira (`Visa`, `Mastercard`, `Elo`…) | `Taxa/Tarifa: R$ x \| NSU: y` |
| **Crédito** | Adquirente | Data da venda | Data prevista de pagamento do adquirente | Bandeira | `Taxa/Tarifa: R$ x \| NSU: y` |
| **iFood** | Marketplace + PDV | Data do pedido | = Competência | `Ifood` | `NFCe: <PDV> \| ID iFood: <id>` |
| **PIX** | PDV | Data de negócio | = Competência | `PIX - PIX` | `NFCe: n \| Pedido: n` |
| **Dinheiro** | PDV | Data de negócio | = Competência | `Dinheiro` | `Pedido: n \| NFCe: n` |
| **Hanzo** | PDV | Data de negócio | D+31 | `Hanzo Prod` | `NFCe: n \| Pedido: n` |

**Valor por fonte:** Débito/Crédito → valor bruto do adquirente; iFood → valor dos
itens; PIX/Dinheiro/Hanzo → valor do pagamento no PDV.

## Racional das regras

- **Categoria = bandeira** (débito/crédito): mantém a categoria enxuta — só a
  bandeira do cartão, sem prefixos como "Débito Visa".
- **Vencimento pelo adquirente:** o adquirente informa a *data prevista de
  pagamento* de cada transação; usá-la evita recalcular `D+1`/`D+31` e trata
  automaticamente fins de semana e feriados.
- **Rótulos padronizados** (`PIX - PIX`, `Hanzo Prod`): pedidos pela operação
  financeira para facilitar a leitura no sistema.
- **`Cupom` → `NFCe`** na descrição: é o mesmo número (o cupom fiscal é a NFC-e),
  mas o texto `NFCe` deixa mais claro para quem confere.
- **NFC-e sempre do PDV:** no delivery, a nota pode ser emitida pelo marketplace;
  a NFC-e confiável vem do PDV.

## Filtro de vendas efetivadas

Só entram vendas realmente concluídas:

- **PDV:** `Status da Venda == "Pago"` (exclui `Cancelado`).
- **Adquirente:** `Status da venda == "Aprovada"`.
- **Marketplace:** `Status final do pedido == "CONCLUIDO"`.
- Qualquer linha com **valor ≤ 0** é descartada.

Esse filtro foi validado após identificar vendas canceladas do PDV que, sem ele,
entravam como lançamentos de R$ 0 (e, em alguns casos, com valor > 0 indevido).
