# Interface web — Conciliador de Vendas (SEVENT)

Interface web para rodar o pipeline sem terminal: o usuário anexa os **três
relatórios do mês** num único campo, o sistema **reconhece cada um pelo conteúdo**,
concilia e devolve as **planilhas prontas** para importação, com tela de conferência.

Feita para rodar **on-premise** (na máquina/rede do cliente) — os arquivos são
processados localmente e não saem do ambiente.

## Rodar

Na raiz do projeto:

```bash
pip install -r requirements.txt
python webapp/app.py
```

Abra **http://localhost:5000** no navegador.

## Como usar

1. Arraste os 3 relatórios do mês (Adquirente/cartões, Marketplace/delivery e PDV)
   para o campo único — em qualquer ordem.
2. Informe o mês de referência (ex.: `jun2026`).
3. Clique em **Processar**.
4. Confira os totais por forma de pagamento e as divergências; baixe as planilhas
   (individual ou `.zip`).

O reconhecimento é por **conteúdo** (colunas), não pelo nome do arquivo — pode
renomear os exports à vontade.

## Stack

- **Flask** (servidor) + **openpyxl** (planilhas)
- Front-end estático (HTML/CSS/JS) na identidade SEVENT
- Reutiliza o núcleo [`src/gerar_planilhas.py`](../src/gerar_planilhas.py)

## Notas

- Processamento **efêmero**: cada execução usa uma pasta temporária; nada é
  persistido além da sessão de download.
- A etapa **"Confirmar e importar"** (criar os lançamentos direto no sistema
  financeiro via API) é a **Fase 3** do roadmap — na interface aparece como "em breve".
- Para produção on-premise, servir atrás de um WSGI (ex.: `waitress`/`gunicorn`) e,
  se desejado, dentro do container Docker (Fase 2).
