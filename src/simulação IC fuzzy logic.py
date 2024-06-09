import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Dados embutidos diretamente no código
dados = [
   # coloque aqui os dados

]

# Mapeamento dos impactos e probabilidade
impact_map = {'baixo': 0.25, 'médio': 0.50, 'alto': 0.75}
impacts = [impact_map[item["Impacto"]] for item in dados]
probabilities = [item["Probabilidade"] for item in dados]

# Antecedentes e Consequente
impacto = ctrl.Antecedent(np.arange(0, 1.01, 0.01), 'impacto')
probabilidade = ctrl.Antecedent(np.arange(0, 0.21, 0.01), 'probabilidade')
IC_fuzzy = ctrl.Consequent(np.arange(0, 10.1, 0.1), 'IC_fuzzy')  # Saída de 0% a 10%

# Funções de pertinência
impacto.automf(3, names=['baixo', 'médio', 'alto'])
probabilidade.automf(3, names=['baixa', 'média', 'alta'])

# Customização das funções de pertinência para IC_fuzzy
IC_fuzzy['baixo'] = fuzz.trimf(IC_fuzzy.universe, [0, 2, 4])
IC_fuzzy['médio'] = fuzz.trimf(IC_fuzzy.universe, [2, 4, 6])
IC_fuzzy['alto'] = fuzz.trimf(IC_fuzzy.universe, [4, 6, 8])

# Regras
rule1 = ctrl.Rule(impacto['baixo'] & probabilidade['baixa'], IC_fuzzy['baixo'])
rule2 = ctrl.Rule(impacto['baixo'] & probabilidade['média'], IC_fuzzy['baixo'])
rule3 = ctrl.Rule(impacto['baixo'] & probabilidade['alta'], IC_fuzzy['médio'])
rule4 = ctrl.Rule(impacto['médio'] & probabilidade['baixa'], IC_fuzzy['baixo'])
rule5 = ctrl.Rule(impacto['médio'] & probabilidade['média'], IC_fuzzy['médio'])
rule6 = ctrl.Rule(impacto['médio'] & probabilidade['alta'], IC_fuzzy['alto'])
rule7 = ctrl.Rule(impacto['alto'] & probabilidade['baixa'], IC_fuzzy['médio'])
rule8 = ctrl.Rule(impacto['alto'] & probabilidade['média'], IC_fuzzy['alto'])
rule9 = ctrl.Rule(impacto['alto'] & probabilidade['alta'], IC_fuzzy['alto'])

system = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])
simulator = ctrl.ControlSystemSimulation(system)

# Aplicação das regras e cálculo do IC
results = []
for imp, prob in zip(impacts, probabilities):
    simulator.input['impacto'] = imp
    simulator.input['probabilidade'] = prob
    simulator.compute()
    results.append(simulator.output['IC_fuzzy'])

# Calculando o IC agregado
IC_agregado = np.mean(results)
print(f"Índice de Contingência Agregado: {IC_agregado:.2f}%")

