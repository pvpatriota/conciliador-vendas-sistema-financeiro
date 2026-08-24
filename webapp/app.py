#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Interface web do Conciliador de Vendas (SEVENT).

O usuario anexa os 3 relatorios do mes num unico campo; o sistema reconhece cada
um pelo conteudo, roda o pipeline (src/gerar_planilhas.py) e devolve as planilhas
prontas para importacao, com uma tela de conferencia.

Rodar (on-premise):
    pip install -r requirements.txt
    python webapp/app.py
    # abre em http://localhost:5000
"""
import os
import sys
import uuid
import zipfile
import tempfile
import warnings

import openpyxl
from flask import (Flask, render_template, request, redirect, url_for,
                   send_from_directory, send_file, abort)
from werkzeug.utils import secure_filename

warnings.filterwarnings('ignore')

# Importa o nucleo do pipeline (src/gerar_planilhas.py)
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, 'src'))
from gerar_planilhas import gerar, norm  # noqa: E402

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 40 * 1024 * 1024  # 40 MB por upload

RUNS = os.path.join(tempfile.gettempdir(), 'conciliador_runs')
os.makedirs(RUNS, exist_ok=True)

# Nome canonico por tipo (bate com os padroes do pipeline)
CANONICO = {
    'adquirente': 'Vendas_cielo_detalhe.xlsx',
    'marketplace': 'relatorios.ifood.xlsx',
    'pdv': 'Relatorio_Geral_Vendas.xlsx',
}
ROTULO = {'adquirente': 'Adquirente', 'marketplace': 'Marketplace', 'pdv': 'PDV'}

CORES = {'Debito': '#5B9BFF', 'Credito': '#A98BFF', 'PIX': '#41cf93',
         'Dinheiro': '#7ED957', 'Hanzo': '#FF7AB6', 'iFood': '#f5b301'}


# --------------------------------------------------------------------------- #
# Reconhecimento do tipo de relatorio pelo conteudo (nao pelo nome do arquivo)
# --------------------------------------------------------------------------- #
def detectar_tipo(path):
    # Nao usar read_only: alguns exports (ex.: adquirente) declaram a dimensao
    # errada e o modo read_only devolve a planilha vazia.
    try:
        wb = openpyxl.load_workbook(path, data_only=True)
    except Exception:
        return None
    rotulos = set()
    for ws in wb.worksheets:
        for i, row in enumerate(ws.iter_rows(values_only=True)):
            if i >= 15:
                break
            for c in row:
                if c not in (None, ''):
                    rotulos.add(norm(c))
    wb.close()
    if 'data da venda' in rotulos and 'nsu/doc' in rotulos:
        return 'adquirente'
    if 'id curto do pedido' in rotulos or 'status final do pedido' in rotulos:
        return 'marketplace'
    if 'data de negocio' in rotulos and 'cupom fiscal' in rotulos:
        return 'pdv'
    return None


# --------------------------------------------------------------------------- #
# Filtros de formatacao (pt-BR)
# --------------------------------------------------------------------------- #
@app.template_filter('brl')
def brl(v):
    s = '{:,.2f}'.format(float(v or 0))
    s = s.replace(',', '#').replace('.', ',').replace('#', '.')
    return 'R$ ' + s


@app.template_filter('milhar')
def milhar(v):
    return '{:,}'.format(int(v or 0)).replace(',', '.')


# --------------------------------------------------------------------------- #
# Rotas
# --------------------------------------------------------------------------- #
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/processar', methods=['POST'])
def processar():
    enviados = request.files.getlist('relatorios')
    sufixo = secure_filename((request.form.get('sufixo') or 'saida').strip()) or 'saida'
    enviados = [f for f in enviados if f and f.filename]

    if not enviados:
        return render_template('index.html', erro='Nenhum arquivo foi enviado.',
                               sufixo=sufixo)

    token = uuid.uuid4().hex
    base = os.path.join(RUNS, token)
    entrada = os.path.join(base, 'entrada')
    os.makedirs(entrada, exist_ok=True)

    reconhecidos = {}
    nao_reconhecidos = []
    for f in enviados:
        tmp = os.path.join(base, 'tmp_' + secure_filename(f.filename))
        f.save(tmp)
        tipo = detectar_tipo(tmp)
        if tipo and tipo not in reconhecidos:
            os.replace(tmp, os.path.join(entrada, CANONICO[tipo]))
            reconhecidos[tipo] = f.filename
        else:
            nao_reconhecidos.append(f.filename)
            os.remove(tmp)

    faltando = [ROTULO[t] for t in ('adquirente', 'marketplace', 'pdv')
                if t not in reconhecidos]
    if faltando:
        msg = ('Faltou reconhecer: ' + ', '.join(faltando) + '. '
               'Envie os três relatórios (Adquirente, Marketplace e PDV) em formato .xlsx.')
        return render_template('index.html', erro=msg, sufixo=sufixo)

    # Roda o pipeline
    resumo = gerar(entrada, sufixo)

    # Empacota tudo num .zip
    saida = resumo['saida']
    zip_path = os.path.join(base, 'planilhas.zip')
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
        for nome in os.listdir(saida):
            z.write(os.path.join(saida, nome), nome)

    return render_template('resultado.html', resumo=resumo, sufixo=sufixo,
                           token=token, cores=CORES)


@app.route('/baixar/<token>/<path:arquivo>')
def baixar(token, arquivo):
    if not all(c in '0123456789abcdef' for c in token):
        abort(404)
    base = os.path.join(RUNS, token)
    if arquivo == 'planilhas.zip':
        caminho = os.path.join(base, 'planilhas.zip')
        if not os.path.isfile(caminho):
            abort(404)
        return send_file(caminho, as_attachment=True,
                         download_name='planilhas_conta_azul.zip')
    saida = os.path.join(base, 'entrada', 'SAIDA_Financeiro')
    return send_from_directory(saida, secure_filename(arquivo), as_attachment=True)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', '5000'))
    # Auto-reload em desenvolvimento: reinicia sozinho quando o codigo/templates
    # mudam (inclusive apos um `git pull`). Desative com RELOAD=0.
    reload = os.environ.get('RELOAD', '1') != '0'
    app.config['TEMPLATES_AUTO_RELOAD'] = reload
    print('Conciliador SEVENT  ->  http://localhost:%d   (auto-reload: %s)'
          % (port, 'ligado' if reload else 'desligado'))
    # use_reloader recarrega o codigo; sem debugger exposto (dados financeiros).
    app.run(host='0.0.0.0', port=port, use_reloader=reload)
