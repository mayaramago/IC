import numpy as np
import pandas as pd

# Parâmetros iniciais
custo_base = 1.1e9  # 1.100 bilhão de reais
ic_pessoal = sorted([0.03, 0.0415, 0.0549])  # ICs ordenados do menor para o maior
ic_min = 0.01 * 1.1e9  # Mínimo de 1% de 1.100 bilhão
ic_max = 0.08 * 1.1e9  # Máximo de 8% de 1.100 bilhão
ic_step = 0.01 * 1.1e9  # Incremento
threshold_seguranca = 1.1  # Threshold de segurança para o ICC
percentual_resultado_liquido = 0.20  # 20% do resultado líquido considerado
resultado_liquido = custo_base * percentual_resultado_liquido

# Definição dos dados
dados = [
 #coloque aqui seus dados 
]

# Conversão para DataFrame
df = pd.DataFrame(dados)
df['Impacto Financeiro'] = df['Impacto'].map({'baixo': 1e6, 'médio': 3e6, 'alto': 5.5e6})

# Simulação de Monte Carlo
n_simulations = 10000
simulated_costs = np.zeros(n_simulations)

# Realizar simulações
for i in range(n_simulations):
    occurrences = np.random.rand(len(df)) < df['Probabilidade']
    simulated_costs[i] = (occurrences * df['Impacto Financeiro']).sum()


# Análise para cada IC estabelecido
for ic in [1.1e9 * x for x in [0.03, 0.0415, 0.0549]]:
    ic_coverage = simulated_costs <= ic
    coverage_rate = ic_coverage.mean() * 100
    excess_cost = simulated_costs[~ic_coverage]
    average_excess_cost = excess_cost.mean() if np.any(~ic_coverage) else 0
    icc_value = df['Probabilidade'].dot(df['Impacto Financeiro']) / ic
    insufficiency_probability = 100 * (1 - coverage_rate / 100)
    ic_percentage = (ic / custo_base) * 100  # Convertendo IC para percentual
    exposure_percentage = (average_excess_cost / resultado_liquido) * 100 if average_excess_cost > 0 else 0

    print(f"Para um IC de {ic_percentage:.2f}%:")
    print(f" - ICC (Índice de Cobertura Contingencial): {icc_value:.2f} (Limiar de segurança: {threshold_seguranca})")
    print(f" - Cobertura de riscos: {coverage_rate:.2f}%")
    print(f" - Probabilidade de insuficiência: {insufficiency_probability:.2f}%")
    print(f" - Exposição do resultado líquido à insuficiência: {exposure_percentage:.2f}% do resultado líquido")

# Análise de Sensibilidade
ic_min = 0.01 * custo_base
ic_max = 0.08 * custo_base
ics_variados = np.linspace(ic_min, ic_max, 10)  # Ajuste para obter mais valores

sensitivity_results = {}
excess_costs = {}

for ic in ics_variados:
    ic_coverage = simulated_costs <= ic
    excess_cost = simulated_costs[simulated_costs > ic] - ic if np.any(simulated_costs > ic) else np.array([0])
    average_excess_cost = np.mean(excess_cost)
    icc_varied = df['Probabilidade'].dot(df['Impacto Financeiro']) / ic
    sensitivity_results[ic] = icc_varied
    excess_costs[ic] = average_excess_cost

# Ordenando os resultados para apresentação
sorted_ics = sorted(sensitivity_results.items(), key=lambda x: x[1])  # Ordenando pelo ICC

print("\nSensitivity Analysis:")
for ic, icc in sorted_ics[:10]:  # Mostrando apenas os dez primeiros resultados
    ic_percentage = (ic / custo_base) * 100
    exposure_percentage = (excess_costs[ic] / resultado_liquido) * 100
    print(f" - Para um IC de {ic_percentage:.2f}%, o ICC ajustado é {icc:.2f}")
    print(f" - Exposição do resultado líquido à insuficiência: {exposure_percentage:.2f}% do resultado líquido")