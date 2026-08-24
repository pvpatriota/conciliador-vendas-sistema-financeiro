# Exemplos e formato de entrada

Esta pasta descreve os **arquivos de entrada** esperados pelo pipeline. Nenhum dado
real é distribuído — apenas a estrutura.

## Entrada: pasta do mês

Coloque numa pasta os três relatórios do mês. O pipeline reconhece por padrão de
nome:

| Fonte | Padrão de nome | Aba usada |
|---|---|---|
| Adquirente (cartões) | `Vendas_*cielo*detalhe*.xlsx` | primeira |
| Marketplace (delivery) | `relatorios.ifood*.xlsx` | primeira |
| PDV / caixa | `Relatorio_Geral_Vendas*.xlsx` | `Relatorio` |

## Colunas esperadas (resumo)

**Adquirente** — cabeçalho não está na primeira linha (há um bloco institucional
antes); o pipeline localiza a linha que contém `Data da venda`. Colunas usadas:
`Data da venda`, `Forma de pagamento`, `Bandeira`, `Valor bruto`, `Taxa/tarifa`,
`Status da venda`, `Data prevista do pagamento`, `NSU/DOC`.

**Marketplace** — cabeçalho na primeira linha. Colunas usadas (por prefixo):
`ID CURTO DO PEDIDO`, `ID COMPLETO DO PEDIDO`, `DATA E HORA DO PEDIDO`,
`STATUS FINAL DO PEDIDO`, `VALOR DOS ITENS`, `TOTAL PAGO...`, `VALOR LIQUIDO`,
`FORMA DE PAGAMENTO`.

**PDV** — aba `Relatorio`, cabeçalho na primeira linha. Colunas usadas:
`Data de Negocio`, `Status da Venda`, `Cupom Fiscal`, `Pedido`, `Venda Bruta`,
`Forma de pagamento`, `Valor Pagamento`.

## Saída

<!--
São geradas planilhas prontas para serem importadas no sistema financeiro
(uma por forma de pagamento) e uma planilha de divergências para conferência.
Ficam em uma subpasta criada dentro da pasta do mês.
-->

## Execução

```bash
python ../src/gerar_planilhas.py ./2026-05 mai2026
```
