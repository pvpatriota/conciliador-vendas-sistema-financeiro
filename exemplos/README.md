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

Uma subpasta `SAIDA_ContaAzul/` é criada dentro da pasta do mês, com:

```
conta_azul_debito_<sufixo>.xlsx
conta_azul_credito_<sufixo>.xlsx
conta_azul_pix_<sufixo>.xlsx
conta_azul_dinheiro_<sufixo>.xlsx
conta_azul_hanzo_<sufixo>.xlsx
conta_azul_ifood_<sufixo>.xlsx
DIVERGENCIAS_ifood_sem_nfce_<sufixo>.xlsx
```

## Execução

```bash
python ../src/gerar_contaazul.py ./2026-05 mai2026
```
