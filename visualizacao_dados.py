from extracao_dados import dados, tabela_estado_lucros, categoria_mais_vende, df_ordenado, ultimato_ordenado
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 3. Visualização de dados
# Lucro real entre as regiões
tabela_estado_lucros.head()
plt.figure(figsize=(10, 6))
ultimato_ordenado['Percentual %'].plot(kind='barh', color='coral')

plt.title('Percentual do Custo de Frete por região')
plt.xlabel('%')
plt.ylabel('Região')
plt.show()

lucro_total = dados['Lucro_Real'].sum()
print(df_ordenado)



# IAzinha né.
plt.figure(figsize=(8, 6))
plt.scatter(
    x=df_ordenado['Quantidade'], # Eixo X: Quanto o produto faturou
    y=df_ordenado['Lucro_Financeiro'],  # Eixo Y: Quanto o produto deu de lucro real
    color='blue',
    alpha=0.7,
    edgecolors='black',
    s=100 # Tamanho das bolinhas
)
plt.title('Relação entre Volume de Vendas e o Lucro', fontsize=14, fontweight='bold')
plt.xlabel('Volume de Vendas', fontsize=12)
plt.ylabel('Lucro (R$)', fontsize=12)

# 4. Adiciona linhas de grade no fundo
plt.grid(True, linestyle='--', alpha=0.5)

# 5. Exibe o gráfico na tela
plt.tight_layout()
plt.show()

top_3 = df_ordenado.nlargest(3, 'Lucro_Financeiro') # pega os 3 maiores numeros
bottom_3 = df_ordenado.nsmallest(3, 'Lucro_Financeiro') # pega os 3 menores numeros

tabela_resumo = pd.concat([top_3, bottom_3]).drop_duplicates().reset_index(drop=True) # concatena as variaveis, remove duplicadas e tira reseta os index para ter ordem.


# --- FUNÇÃO DE FORMATAÇÃO CONDICIONAL ---
def aplicar_cores_lucro(valor):
    """Aplica verde para lucros (positivos) e vermelho para prejuízos (negativos)"""
    if valor > 0:
        return 'background-color: #d4edda; color: #155724; font-weight: bold;'  # Verde suave
    elif valor < 0:
        return 'background-color: #f8d7da; color: #721c24; font-weight: bold;'  # Vermelho suave
    else:
        return ''
def formatacao(valor):
    return f'{valor:.2f}'
# 4. Aplicando a estilização na coluna 'Lucro_Real'
tabela_estilizada = (
    tabela_resumo.style
    # Passa o dicionário formatando a coluna desejada para 2 casas decimais
    .format({'Lucro_Financeiro': '{:.2f}'})
    # Passa a função de cores apenas no subset correto
    .map(aplicar_cores_lucro, subset=['Lucro_Financeiro'])
)

# Passando o nome do arquivo dentro do parâmetro 'buf'
tabela_estilizada.to_html(buf='tabela_resumo.html', index=False)

print("Agora sim! Arquivo 'tabela_resumo.html' gerado com sucesso.")
# IAzinha né.
dados_limpos = dados.copy()
dados_limpos = dados_limpos.drop(['media_produto', 'std_produto', 'limite_superior', 'limite_inferior'], axis=1)
print(dados_limpos)
total_lucro = dados_limpos['Lucro_Real'].sum()
"""
1- Padronização dos precos de fretes por regiao (ex: para Sul -> 14.99$, para Norte -> 50.00$) -> valor cobrado para o cliente! (outra recomendação)
2- Buscar a causalidade dos Custo_Frete variarem tanto seja por produto e/ou regiao.
3 - Com um aumento percentual (ou reajuste) dos preços dos itens (como 3% de aumento) o lucro iria dobrar. uma recomendação
Padrão de vazamento de dinheiro -> O preço pelos produtos perde em comparação ao custo do frete, assim vender o produto diversas vezes não causa produtividade de dinheiro dependendo da onde enviado.
"""

reajuste_10 = dados['Preco_Vendido'] * 0.3

dados_reajuste = []
dados_reajuste = pd.DataFrame(dados_reajuste)

dados_reajuste['Produtos'] = dados['Produto']
dados_reajuste['Preco_Vendido_Reajuste'] = dados_limpos['Preco_Vendido'] + reajuste_10  
dados_reajuste['Custo_Unitario'] = dados['Custo_Unitario'] 
dados_reajuste['Custo_Frete'] = dados['Custo_Frete']
dados_reajuste['Lucro_Real_Reajuste'] = dados_reajuste['Preco_Vendido_Reajuste'] - dados_reajuste['Custo_Frete'] - dados_reajuste['Custo_Unitario']

total_lucro_reajuste = dados_reajuste['Lucro_Real_Reajuste'].sum()
print(dados_reajuste)
print("\nTotal Lucro sem reajuste:\n ",total_lucro.round(2))
print("\nTotal Lucro com reajuste:\n",total_lucro_reajuste.round(2))

agregacao = pd.Series({
    "Lucro Real": total_lucro,
    "Lucro Reajustado": total_lucro_reajuste
})
print("\n",agregacao)
#agregacao.to_excel("Lucros.xlsx",) EXCEL

ordenar_data = dados_limpos.sort_values(by='Data_Venda', ascending=True)
print(ordenar_data) # 2023-01-01 até 2023-12-06

lucro_real_positivo = ordenar_data[ordenar_data['Lucro_Real'] > 0]
print(lucro_real_positivo) # 318 rows significa que 500 - 318 = 182 -> rows que o lucro era negativo

lucro_real_negativo = ordenar_data[ordenar_data['Lucro_Real'] < 0]
print(lucro_real_negativo) # Acessório da mais prejuizo que beneficio.

contar = lucro_real_negativo.value_counts(subset='Categoria') # conta pela coluna categoria quantas vzs apareceu.
print(contar)# Acessórios     217 -> tabela padrão
             # Acessórios     175 -> tabela com lucro negativo