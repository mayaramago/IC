import numpy as np
import pandas as pd

# Configuração para mostrar todas as linhas
pd.set_option('display.max_rows', None)

# Ajustes nas configurações de simulação baseadas no impacto
impact_settings = {
    'baixo': {'mean': 0.01, 'std': 0.005, 'threshold': 0.015},
    'médio': {'mean': 0.008, 'std': 0.01, 'threshold': 0.02},
    'alto': {'mean': 0.005, 'std': 0.015, 'threshold': 0.04}
}

# Função para simular a probabilidade de ocorrência de um risco
def simulate_risk(risk_impact, n=30000):
    settings = impact_settings[risk_impact.strip().lower()]
    simulations = np.random.normal(loc=settings['mean'], scale=settings['std'], size=n)
    probability = np.mean(simulations > settings['threshold'])
    return probability

# Leitura e aplicação da simulação
file_path = # coloque aqui o caminho
df = pd.read_csv(file_path, sep=';')
df.columns = ['CÓDIGO RISCO', 'IMPACTO']
df['IMPACTO'] = df['IMPACTO'].str.strip().str.lower()
df['Simulated Prob'] = df['IMPACTO'].apply(simulate_risk)

print("Dados carregados com sucesso:")
print(df)

# Definir pesos para diferentes níveis de impacto
weights = {'baixo': 0.5, 'médio': 1.0, 'alto': 1.5}

# Aplicar pesos às probabilidades simuladas conforme o impacto
df['Weighted Prob'] = df['Simulated Prob'].multiply(df['IMPACTO'].map(weights))

# Calcular o Índice de Contingência como a soma das probabilidades ponderadas
IC = df['Weighted Prob'].sum()

print(f"Índice de Contingência Calculado: {IC:.2f}%")

