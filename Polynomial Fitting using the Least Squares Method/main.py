import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# df = pd.read_csv('jul19-jun20.csv')
# feriados = pd.read_csv('feriados_2019_2020.csv')
df = pd.read_csv('accidentsByDay.csv')
feriados = pd.read_csv('accidents_in_holidays_2019_2024.csv')

# Converter a coluna de datas para o formato datetime
df['date'] = pd.to_datetime(df['date']).dt.date
feriados['date'] = pd.to_datetime(feriados['date']).dt.date
df_merged = pd.merge(df, feriados, how='left', on='date')

df_merged['feriado'] = df_merged['nome_feriado'].notna()


# df_merged['media_movel'] = df_merged['number_accidents'].rolling(window=10).mean()
# df_merged['desvio_padrao'] = df_merged['number_accidents'].rolling(window=10).std()
# desvio_padrao_medio = df_merged['desvio_padrao'].mean()
# df_merged['alto_desvio'] = df_merged['desvio_padrao'] > 1.5 * desvio_padrao_medio


df_feriados = df_merged[df_merged['feriado'] == True]
df_nao_feriados = df_merged[df_merged['feriado'] == False]

grauF = 5
grauNF = 5
x_feriados = np.arange(len(df_feriados))
y_feriados = df_feriados['number_accidents']
coef_feriados = np.polyfit(x_feriados, y_feriados, grauF)
polinomio_feriados = np.poly1d(coef_feriados)

x_nao_feriados = np.arange(len(df_nao_feriados))
y_nao_feriados = df_nao_feriados['number_accidents']
coef_nao_feriados = np.polyfit(x_nao_feriados, y_nao_feriados, grauNF)
polinomio_nao_feriados = np.poly1d(coef_nao_feriados)

#region plot

# Plotando os dados
plt.figure(figsize=(10, 6))

# Plotar os dados reais de não feriados
plt.scatter(df_nao_feriados['date'], df_nao_feriados['number_accidents'], color='#6666ff', label='Não Feriados')

# Plotar os dados reais de feriados
plt.scatter(df_feriados['date'], df_feriados['number_accidents'], color='#ff2222', label='Feriados')

# Gerar o range de dates para o polinômio dos feriados
x_vals_feriados = np.linspace(0, len(df_feriados) - 1, len(df_feriados))
plt.plot(df_feriados['date'], polinomio_feriados(x_vals_feriados), color='#ff0000', label='Tendência Feriados')

# Gerar o range de dates para o polinômio dos não feriados
x_vals_nao_feriados = np.linspace(0, len(df_nao_feriados) - 1, len(df_nao_feriados))
plt.plot(df_nao_feriados['date'], polinomio_nao_feriados(x_vals_nao_feriados), color='#000070', label='Tendência Não Feriados')


for idx, row in df_feriados.iterrows():
    if row['nome_feriado']:
        plt.annotate(row['nome_feriado'], (row['date'], row['number_accidents']),
                     textcoords="offset points", xytext=(0,0), ha='center', fontsize=9, color='#000000',rotation=30)

#endregion

# Configurações do gráfico
plt.title('Tendência de Acidentes de Trânsito em Feriados vs. Não Feriados')
plt.xlabel('Data')
plt.ylabel('Número de Acidentes')
plt.legend()
plt.grid(True)
#plt.xticks(rotation=45)  # Rotaciona as datas para melhor visualização
plt.tight_layout()  # Ajusta o layout para evitar sobreposição
plt.show()