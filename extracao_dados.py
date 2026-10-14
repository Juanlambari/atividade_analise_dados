import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print("\nDados da Tabela:\n")
dados = pd.DataFrame(pd.read_excel("aula_3.xlsx"))
dados['Data_Venda'] = pd.DatetimeIndex(dados['Data_Venda'])

copia_df = dados.copy()
print(dados.info(),"\n") # não há nulos
# Verificar se há custo negativo no Custo_Unitário
for x in dados['Custo_Unitario']:
    if x < 0:
        print(x)

# Verificar se há custo negativo no Custo_Unitário
for x in dados['Preco_Vendido']:
    if x < 0:
        print(x)

# Verificar se há custo negativo no Custo_Unitário
for x in dados['Custo_Frete']:
    if x < 0:
        print(x)
# Caso tivesse numeros negativos desse jeito eu poderia ver qual o produto
custo_negativo = dados[dados['Custo_Unitario'] < 0][['Produto', 'Custo_Unitario']]
print("\nCusto Unitario negativos:\n ",custo_negativo)

fretes_zerados = dados[dados['Custo_Frete'] < 0][['Produto', 'Custo_Frete', 'Regiao_Cliente']]
print("\nCusto Frete negativos:\n ",fretes_zerados)

media_custo_unitario = dados.groupby('Produto').agg({
    'Custo_Unitario': 'mean',
    'Preco_Vendido': 'mean',
    'Custo_Frete': 'mean'
})
print("\nMedia do Custo Unitário:\n ",media_custo_unitario.round(2)) # não há discrepancia a não ser a media de custo frete do 'Monitor 144hz'

filtro = dados['Produto'] == 'Monitor 144hz'
max_min_do_monitor = dados.loc[filtro]

max_monitor = max_min_do_monitor.groupby('Produto')['Custo_Frete'].max()
print("\nMax do Monitor:\n ",max_monitor)

min_monitor = max_min_do_monitor.groupby('Produto')['Custo_Frete'].min()
print("\nMin do Monitor:\n ",min_monitor)

filtro = dados['Produto'] == 'Cabo USB-C'
max_min_do_cabo_C = dados.loc[filtro]
max_cabo_C = max_min_do_cabo_C.groupby('Produto')['Custo_Frete'].max()
print("\nMax do cabo_C:\n ",max_cabo_C)

min_cabo_C = max_min_do_cabo_C.groupby('Produto')['Custo_Frete'].min()
print("\nMin do cabo_C:\n ",min_cabo_C)

dados_teclado = dados.loc[dados['Produto'] == 'Teclado Mecânico', :]

# PARA CUSTO UNITARIO
dados['media_produto'] = dados.groupby('Produto')['Custo_Unitario'].transform('mean')
dados['std_produto'] = dados.groupby('Produto')['Custo_Unitario'].transform('std')

dados['limite_superior'] = dados['media_produto'] + (3 * dados['std_produto'])
dados['limite_inferior'] = dados['media_produto'] - (3 * dados['std_produto'])

# 3. Usa o .loc para encontrar quem fugiu do padrão do SEU PRÓPRIO grupo
outliers = dados.loc[(dados['Custo_Unitario'] > dados['limite_superior']) | (dados['Custo_Unitario'] < dados['limite_inferior'])]

# Mostra apenas as colunas principais para você analisar o que está errado
resultado_limpo = outliers[['Produto', 'Custo_Unitario', 'media_produto', 'std_produto']]
print("\nResultado Limpo com o Custo_Unitário:\n",resultado_limpo)

# PARA PRECO VENDIDO
dados['media_produto'] = dados.groupby('Produto')['Preco_Vendido'].transform('mean')
dados['std_produto'] = dados.groupby('Produto')['Preco_Vendido'].transform('std')

dados['limite_superior'] = dados['media_produto'] + (3 * dados['std_produto'])
dados['limite_inferior'] = dados['media_produto'] - (3 * dados['std_produto'])

# Usa o .loc para encontrar quem fugiu do padrão do SEU PRÓPRIO grupo
outliers = dados.loc[(dados['Preco_Vendido'] > dados['limite_superior']) | (dados['Preco_Vendido'] < dados['limite_inferior'])]

# Mostra apenas as colunas principais para você analisar o que está errado
resultado_limpo = outliers[['Produto', 'Preco_Vendido', 'media_produto', 'std_produto']]
print("\nResultado Limpo com o Preco_Vendido:\n",resultado_limpo)

# PARA CUSTO FRETE
dados['media_produto'] = dados.groupby('Produto')['Custo_Frete'].transform('mean')
dados['std_produto'] = dados.groupby('Produto')['Custo_Frete'].transform('std')

dados['limite_superior'] = dados['media_produto'] + (3 * dados['std_produto'])
dados['limite_inferior'] = dados['media_produto'] - (3 * dados['std_produto'])

# Usa o .loc para encontrar quem fugiu do padrão do SEU PRÓPRIO grupo
outliers = dados.loc[(dados['Custo_Frete'] > dados['limite_superior']) | (dados['Custo_Frete'] < dados['limite_inferior'])]

# Mostra apenas as colunas principais para você analisar o que está errado
resultado_limpo = outliers[['Produto', 'Custo_Frete', 'media_produto', 'std_produto']]
print("\nResultado Limpo com o Custo_Frete:\n",resultado_limpo)

# 2.
dados['Lucro_Real'] = dados['Preco_Vendido'] - dados['Custo_Frete'] - dados['Custo_Unitario']

print("\nLucros Reais",dados.round(2)) # Lucros reais
# 2.1
categoria_mais_vende = dados.groupby('Categoria').agg({
    'Custo_Unitario': 'sum',
    'Preco_Vendido': 'sum'
})
print("\nCategoria que mais vende por VOLUME:\n",categoria_mais_vende) # Monitor

# 2.2
tabela_estado_lucros = pd.pivot_table(
    dados,
    index='Regiao_Cliente',
    values='Lucro_Real',
    aggfunc=['sum', 'mean']
)
tabela_estado_lucros.columns = ['Lucro_Real_Total', 'Lucro_Real_Medio']

print("\nTabela com Lucro Real e Médio:\n",tabela_estado_lucros.round(2))

# 2.3
"""
TENTATIVAS FALHAS

filtro_preco = dados['Preco_Vendido'] > 150
coluna_interesse = ['Produto', 'Preco_Vendido']
df_filtrado = dados.loc[filtro_preco, coluna_interesse]

numeros = dados[dados['Quantidade'] == 1]
print(numeros)

TENTATIVAS FALHAS
"""
# uma ajudinha com IA né, básica.
# 1. Defina as categorias que você quer buscar
categorias_desejadas = ['Acessórios', 'Monitores', 'Periféricos']

# 2. Filtra o DataFrame trazendo todas as categorias de uma vez só
filtro = dados[dados['Categoria'].isin(categorias_desejadas)]

# 3. Pega a coluna 'Produto' e remove os duplicados com o método .unique()
produtos_unicos = filtro['Produto'].unique()

# 4. Transforma em uma Series limpa do Pandas
series_lista = pd.Series(produtos_unicos)

# uma ajudinha com IA né, básica.
colunass = ['Produto']                                              # seto a coluna que eu quero.
df_lista = pd.DataFrame(series_lista, columns=colunass)             # faço um DF com a coluna com produtos sem duplicados.


contagem_original = dados['Produto'].value_counts()                 # pega a contagem que os produtos apareceram.

df_lista['Quantidade'] = df_lista['Produto'].map(contagem_original) # coloca em uma coluna quantidade.
print("\nLista com quantidade:\n",df_lista)

#df_ordenado = df_lista.sort_values(by='Quantidade', ascending=False)  Lógica errada
#print(df_ordenado)

df_lista['Lucro_Financeiro'] = dados['Lucro_Real'] # Coloco na lista que o Lucro_Financeiro é o Lucro_Real do meu df com dados brutos.
                                                   # Assim o pandas faz a conta automaticamente por Região.

df_ordenado = df_lista.sort_values(by='Lucro_Financeiro', ascending=False) # Faz a ordenação dos lucros do melhor para pior.
print("\nItens ordenados por lucro:\n ",df_ordenado) # 1º Monitor 144hz, 2º Cabo USB-C, 3º Mouse Gamer RGB -> melhores
                                                     # 1º Teclado Mecânico, Mousepad Gigante, Cabo HDMI 2m -> Piores obs: todos negativos
# Tudo teste
tablea_produto = dados.pivot_table(
    index='Produto',
    values='Custo_Frete',
    aggfunc=['max','min','std']
)
print("\nTabelinha:\n",tablea_produto.round(2))
# tablea_produto.to_excel("tabela_produtos.xlsx") EXCEL

filtro_frete = (dados['Produto'] == 'Monitor 144hz') & (dados['Custo_Frete'] > 100)

filtro_categoria = (dados['Categoria'] == 'Monitores') & (dados['Custo_Frete'] > 100)

frete = dados.loc[filtro_frete, ['Produto', 'Custo_Frete']]
frete_categoria = dados.loc[filtro_categoria, ['Categoria', 'Custo_Frete']]
print("\nTabela com os registros dos monitores:\n",frete_categoria) # identico ao do produto obvio
agrupado = dados.pivot_table(
    index='Categoria',
    values='Custo_Frete',
    aggfunc=['sum', 'mean']
)
print("\nPivot_Table das Categorias:\n ",agrupado.round(2))  # Pivot table para uma tabela com a soma e a media da categoria monitores
# agrupado.to_excel("Categorias_CustoFrete.xlsx") EXCEL
# Tudo teste

#2.4
percentual = dados.groupby('Regiao_Cliente').agg({ # Agrupar Regiao_Cliente para mostrar o Custo_Frete de cada Regiao
    'Custo_Frete': 'sum',
}) 
custo_total_frete = percentual['Custo_Frete'].sum() # Guardo o Custo_Frete total, para poder fazer a porcentagem de cada regiao
print("\nCusto total do Frete",custo_total_frete) 
#custo_total_frete = pd.DataFrame(custo_total_frete)

percentual = pd.DataFrame(percentual) # transformo a variavel agrupada em um DataFrame

ultimato = (percentual['Custo_Frete'] / custo_total_frete) * 100 # Faço a conta da porcentagem (chama ultimato pois não aguentava mais pensar em nomes de variáveis).
print("\nDataFrame com todos os Percentuais",ultimato.round(2))
ultimato = pd.DataFrame(ultimato)
ultimato.columns.values[0] = 'Percentual %'                                  # Seto o nome da Coluna como Percentual.
ultimato_ordenado = ultimato.sort_values(by='Percentual %', ascending=False) # ordeno novamente por pura visualização e legibilidade.
print("\nPercentual ordenado das regiões:\n ",ultimato_ordenado.round(2))
# O norte comanda os percentuais de lucro com aproximadamente 10% a mais que o segundo melhor colocado na lista
"""print(percentual.round(2))
coluna_interesse = ['Regiao_Cliente', 'Percentual']"""

