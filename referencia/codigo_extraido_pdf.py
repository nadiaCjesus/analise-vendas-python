# ==============================
# IMPORTAÇÃO DAS BIBLIOTECAS
# ==============================
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ==============================
# PASSO 1 - BANCO DE DADOS
# ==============================
conexao = sqlite3.connect('dados_vendas.db')
cursor = conexao.cursor()

# Criar tabela
cursor.execute('''
CREATE TABLE IF NOT EXISTS vendas1 (
id_venda INTEGER PRIMARY KEY AUTOINCREMENT,
data_venda DATE,
produto TEXT,
categoria TEXT,
valor_venda REAL
)
''')

# Inserir dados
cursor.execute('''
INSERT INTO vendas1 (data_venda, produto, categoria, valor_venda) VALUES
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
('2023-12-20', 'Produto N', 'Livros', 250.00);
''')

conexao.commit()

# ==============================
# PASSO 2 - CARREGAR PARA PANDAS
# ==============================
df = pd.read_sql_query("SELECT * FROM vendas1", conexao)

# Converter data
df['data_venda'] = pd.to_datetime(df['data_venda'])

# ==============================
# EXPLORAÇÃO DOS DADOS
# ==============================
print("Informações:")
print(df.info())

print("\nResumo estatístico:")
print(df.describe())

print("\nValores nulos:")
print(df.isnull().sum())

# ==============================
# PASSO 3 - ANÁLISE
# ==============================

# Total de vendas por categoria
vendas_categoria = df.groupby('categoria')['valor_venda'].sum()

# Vendas por mês
df['mes'] = df['data_venda'].dt.month
vendas_mes = df.groupby('mes')['valor_venda'].sum()

print("\nVendas por categoria:")
print(vendas_categoria)

print("\nVendas por mês:")
print(vendas_mes)

# ==============================
# PASSO 4 - VISUALIZAÇÃO
# ==============================

# Gráfico de barras - categoria
plt.figure()
sns.barplot(x=vendas_categoria.index, y=vendas_categoria.values)
plt.title("Vendas por Categoria")
plt.xlabel("Categoria")
plt.ylabel("Total de Vendas")
plt.show()

# Gráfico de linha - vendas mensais
plt.figure()
sns.lineplot(x=vendas_mes.index, y=vendas_mes.values)
plt.title("Vendas ao longo dos meses")
plt.xlabel("Mês")
plt.ylabel("Total de Vendas")
plt.show()
