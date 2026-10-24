"""Análise acadêmica de vendas fictícias, recuperada do relatório original."""

from pathlib import Path
import sqlite3

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


PASTA = Path(__file__).resolve().parent
DADOS = [
    ('2023-01-01', 'Produto A', 'Eletrônicos', 1500.00),
    ('2023-01-05', 'Produto B', 'Roupas', 350.00),
    ('2023-02-10', 'Produto C', 'Eletrônicos', 1200.00),
    ('2023-03-15', 'Produto D', 'Livros', 200.00),
    ('2023-03-20', 'Produto E', 'Eletrônicos', 800.00),
    ('2023-04-02', 'Produto F', 'Roupas', 400.00),
    ('2023-05-05', 'Produto G', 'Livros', 150.00),
    ('2023-06-10', 'Produto H', 'Eletrônicos', 1000.00),
    ('2023-07-20', 'Produto I', 'Roupas', 600.00),
    ('2023-08-25', 'Produto J', 'Eletrônicos', 700.00),
    ('2023-09-30', 'Produto K', 'Livros', 300.00),
    ('2023-10-05', 'Produto L', 'Roupas', 450.00),
    ('2023-11-15', 'Produto M', 'Eletrônicos', 900.00),
    ('2023-12-20', 'Produto N', 'Livros', 250.00),
]


def main():
    saida = PASTA / 'resultados'
    saida.mkdir(exist_ok=True)
    # A base em memória evita duplicar as vendas ao executar novamente.
    with sqlite3.connect(':memory:') as conexao:
        conexao.execute('''CREATE TABLE vendas1 (
            id_venda INTEGER PRIMARY KEY AUTOINCREMENT,
            data_venda DATE, produto TEXT, categoria TEXT, valor_venda REAL
        )''')
        conexao.executemany(
            'INSERT INTO vendas1 (data_venda, produto, categoria, valor_venda) '
            'VALUES (?, ?, ?, ?)', DADOS
        )
        df = pd.read_sql_query('SELECT * FROM vendas1', conexao)

    df['data_venda'] = pd.to_datetime(df['data_venda'])
    print('Informações:')
    df.info()
    print('\nResumo estatístico:')
    print(df.describe())
    print('\nValores nulos:')
    print(df.isnull().sum())

    vendas_categoria = df.groupby('categoria')['valor_venda'].sum()
    df['mes'] = df['data_venda'].dt.month
    vendas_mes = df.groupby('mes')['valor_venda'].sum()
    print('\nVendas por categoria:')
    print(vendas_categoria)
    print('\nVendas por mês:')
    print(vendas_mes)
    print(f'\nTotal: R$ {df["valor_venda"].sum():.2f}')

    df.to_csv(saida / 'vendas.csv', index=False, encoding='utf-8')
    vendas_categoria.to_csv(saida / 'vendas_por_categoria.csv')
    vendas_mes.to_csv(saida / 'vendas_por_mes.csv')

    sns.set_theme(style='whitegrid')
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=vendas_categoria.index, y=vendas_categoria.values, ax=ax)
    ax.set(title='Vendas por categoria', xlabel='Categoria', ylabel='Total de vendas (R$)')
    fig.tight_layout()
    fig.savefig(saida / 'vendas_por_categoria.png', dpi=150)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(9, 5))
    sns.lineplot(x=vendas_mes.index, y=vendas_mes.values, marker='o', ax=ax)
    ax.set(title='Vendas ao longo dos meses de 2023', xlabel='Mês', ylabel='Total de vendas (R$)')
    ax.set_xticks(range(1, 13))
    fig.tight_layout()
    fig.savefig(saida / 'vendas_por_mes.png', dpi=150)
    plt.close(fig)
    print(f'Resultados salvos em: {saida}')


if __name__ == '__main__':
    main()
