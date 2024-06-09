# [INDÍCE DE CONTINGÊNCIA DE OBRAS CIVIS - ACIMA DE MILHÕES ]

## Metodologia
Foi considerada uma mescla de 3 abordagens para tornar o índice de contingência mais apurado para situações em que não se tem histórico de dados. 

1)	Simulação de Monte Carlo 

2)	Lógica Fuzzy 

3)	Análise de performance e competitividade dos ICs encontrados e atribuídos

## Parâmetros dos Dados
Os dados foram retirados da matriz de risco de obras, com até 65 riscos mapeados. 
As classificações dos riscos serão em Impacto no Custo (IF), Impacto no cronograma (AC), Impacto combinado de custo e cronograma (IFAC) e probabilidade de ocorrência (MC) 
Os riscos serão classificados de acordo com as variáveis:

•	Impacto Financeiro (IF): Variável linguística com os termos baixo, médio e alto;
•	Atraso no Cronograma (AC): Variável linguística com os termos baixo, médio e alto;
•	Impacto combinado no financeiro e atraso de cronograma (IFAC): Variável linguística com os termos baixo, médio e alto;
•	Probabilidade de ocorrência (MC): variável numérica através da simulação de monte carlo
 

Faixas de Valores para as Variáveis
Impacto Financeiro (em % do total do projeto = 1 bilhão de reais):
•	Baixo: (≤1 milhão de reais)
•	Médio: (>1 a ≤5 milhões de reais)
•	Alto: (>5 milhões de reais)
Atraso no Cronograma (em semanas):
•	Baixo: ≤4 semanas
•	Médio: >4 a ≤8 semanas
•	Alto: >8 semanas

## Encontrando a probabilidade de ocorrência (MC) 

### Parâmetros de riscos
A média e DP estão configurados para refletir uma probabilidade razoável de ocorrência, o que é crucial para planejamento de contingências e alocação de recursos. Os limiares estão ajustados para diferenciar efetivamente entre os impactos esperados de riscos baixos e médios.

1. Riscos Baixos:
Probabilidade Média: Aproximadamente 15%
A probabilidade de ocorrência de riscos baixos variando em torno de 15% sugere uma frequência moderada de eventos menores, que são esperados e gerenciáveis dentro do contexto da obra. Essa frequência é adequada dado o limiar e os parâmetros definidos, indicando que pequenos contratempos são prováveis mas não frequentemente severos.

2. Riscos Médios:
Probabilidade Média: Aproximadamente 11.5%
Riscos médios apresentando uma probabilidade de cerca de 11.5% de ocorrência são realistas para um projeto desta envergadura. Isto reflete uma boa calibração no balanceamento entre a severidade e a frequência esperada desses eventos, que devem ser considerados no planejamento e preparação da gestão de riscos.

3. Riscos Altos:
Probabilidade Média: Aproximadamente 1%
A probabilidade muito baixa para riscos altos é desejável e reflete adequadamente a natureza desses riscos; altamente impactantes mas raros. A configuração dos parâmetros foi eficaz para garantir que tais riscos só se manifestem sob condições extremas, alinhado com o alto limiar estabelecido.
Sendo assim, para encontrar esta probabilidade, optou-se por rodar 30.000 simulações sob a metodologia de monte carlo com o acréscimo dos parâmetros abaixo: 

Riscos Baixos:
•	Média: 0.015 - probabilidade de ocorrência.
•	Desvio padrão: 0.005 - diminuir a variabilidade.
•	Limiar: 0.015 - confirma a ocorrência do risco baixo sem ser excessivamente fácil de superar.

Riscos Médios:
•	Média: 0.00115 - refletir a chance de ocorrência.
•	Desvio padrão: 0.01 - adicionar mais variabilidade.
•	Limiar: 0.02 - maior chance de superação, sem ser demasiado baixo.

Riscos Altos:
•	Média: 0.005 - probabilidade de ocorrência.
•	Desvio padrão: 0.015 - Aumentado significativamente para refletir a alta variabilidade e severidade destes riscos quando ocorrem.
•	Limiar: 0.04 - permitir que eventos realmente graves sejam capturados pela simulação mais frequentemente.

#	Estabelecendo ICs 

## IC – Monte Carlo
Após 10.000 simulações, foi encontrado o IC de 5,49%
Parâmetros de simulação 
Ajustes nas configurações de simulação baseadas no impacto
    'baixo': {'mean': 0.01, 'std': 0.005, 'threshold': 0.015},
    'médio': {'mean': 0.008, 'std': 0.01, 'threshold': 0.02},
    'alto': {'mean': 0.005, 'std': 0.015, 'threshold': 0.04}

## IC – Fuzzy Logic

Parâmetros de simulação 
Para a lógica Fuzzy, deve-se determinar para cada risco baixo, médio ou alto, o grau de variação de 0 a 1.

### Funções de Pertinência

Em vez de limitar a três níveis, expandiu-se para uma escala mais contínua (escala de 0 a 1 com incrementos de 0.1) com ajustes de pontos médios para refletir a severidade relativa (baixo: 0.25, médio: 0.5, alto: 0.75).
O ajuste no código padrão do método para garantir uma distribuição mais granular foi:
  if impact_label == 'baixo':
        impacts.append(0.25)  # ajuste na escala para baixo
    elif impact_label == 'médio':
        impacts.append(0.5)  # ajuste na escala para médio
    elif impact_label == 'alto':
        impacts.append(0.75)  # ajuste na escala para alto

Considerou-se utilizar funções de pertinência trapezoidais ou gaussianas ao invés das triangulares, para capturar melhor a incerteza e a variação na percepção dos níveis de impacto.

O IC está sendo calculado com uma saída entre 0% a 10%, e a saída do IC tiveram suas faixas para 'baixo', 'médio' e 'alto' ajustadas para permitir uma saída entre 0% e 10%, com a definição precisa das faixas que afetam diretamente o resultado do IC.

Para agregação do IC, foi aplicada a técnica defuzzificação -centroide. 

impacto = ctrl.Antecedent(np.arange(0, 1.01, 0.01), 'impacto')
probabilidade = ctrl.Antecedent(np.arange(0, 0.21, 0.01), 'probabilidade')
IC_fuzzy = ctrl.Consequent(np.arange(0, 10.1, 0.1), 'IC_fuzzy')  
Saída de 0% a 10%

### Regras

As regras estabelecidas entre as sobreposições dos parâmetros alto, médio e baixo foram: 
•	Se impacto baixo e probabilidade baixa, então ICFuzzy é baixo
•	Se impacto médio e probabilidade baixa, então ICFuzzy é baixo
E assim por diante, conforme abaixo: 

Rules
rule1 = ctrl.Rule(impacto['baixo'] & probabilidade['baixa'], IC_fuzzy['baixo'])
rule2 = ctrl.Rule(impacto['médio'] & probabilidade['baixa'], IC_fuzzy['baixo'])
rule3 = ctrl.Rule(impacto['alto'] & probabilidade['baixa'], IC_fuzzy['médio'])
rule4 = ctrl.Rule(impacto['baixo'] & probabilidade['média'], IC_fuzzy['médio'])
rule5 = ctrl.Rule(impacto['médio'] & probabilidade['média'], IC_fuzzy['médio'])
rule6 = ctrl.Rule(impacto['alto'] & probabilidade['média'], IC_fuzzy['alto'])
rule7 = ctrl.Rule(impacto['baixo'] & probabilidade['alta'], IC_fuzzy['alto'])
rule8 = ctrl.Rule(impacto['médio'] & probabilidade['alta'], IC_fuzzy['alto'])
rule9 = ctrl.Rule(impacto['alto'] & probabilidade['alta'], IC_fuzzy['alto'])

Após 10.000 simulações, foi encontrado o IC de 4,15%

# Simulação de Cenários com ICs comparativos

Para acumular mais indicadores que pudessem estabelecer a performance dos índices de contingência escolhidos, foram criados: 

## Medição da competitividade da Empresa

Feita uma nova simulação de Monte Carlo, agora com 10.000 replicações, considerando as premissas: 

•	O custo direto da obra é de 1.100 bilhão de reais;
•	Tenho outros 3 concorrentes (Concorrente 1, concorrente 2, concorrente 3) que podem variar deste valor -10% a +10%; 
•	Eles podem considerar índices de contingência de IC 1% a 10% sobre o valor de 1.100 bilhão. Ou seja, o valor final da obra é 1 bilhão + IC aplicado. 
----------------------------------------
 Os indicadores abaixo avaliarão se a empresa tem capacidade financeira para lidar com situações onde o IC pode ser insuficiente 

##	Análise de Reserva de Contingência
Cálculo da Reserva de Contingência Necessária:- Reserva por Risco: `Reserva_{risco} = \text{Probabilidade} \times \text{Impacto Financeiro}`
- Reserva Total de Contingência: `Reserva Total = \sum (\text{Reserva}_{risco})`

Armazenado o valor de reserva total, é possível obter o Índice de Cobertura de Contingência (ICC)
Cálculo do ICC:

`ICC = \frac{\text{IC Estabelecido}}{\text{Reserva Total Necessária}}`

Sendo, 
•	ICC > 1: Indica que o IC é suficiente para cobrir as contingências estimadas
•	ICC < 1: Indica insuficiência, sugerindo risco de sustentabilidade financeira

## Simulação de Monte Carlo para Estimar a Adequação do IC

Foi realizada a simulação das demandas de contingência, considerando cenários onde múltiplos riscos ocorrem com base nas suas probabilidades e então calcula-se o custo total de contingência para cada cenário.

Probabilidade de Insuficiência do IC:

É determinada então a proporção de simulações onde o custo total de contingências excede o IC estabelecido pelos métodos Fuzzy e Monte Carlo. 
Ou seja, os cenários os quais os riscos combinados ocorrem de modo a ultrapassar o custo de contingência anteriormente previsto. 

# Análise de Sensibilidade
## Variação do IC:
Analise como mudanças no IC afetam o ICC e a probabilidade de insuficiência (usando Monte Carlo).

## Threshold (limiar) de Segurança:
Estabeleça um limite mínimo para o ICC (e.g., ICC > 1.1) que ofereça uma margem de segurança.


# Análise de Sensibilidade - Parâmetros
Foi avaliada a performance de três valores para o índice de contingência: 3%, 4,15% e 5,49%. 

IC – Indice percentual de contingência a ser aplicado sobre o valor global do contrato
ICC- Índice que mede a distância entre a contingência aplicada e o valor total necessário caso todos os riscos ocorram simultaneamente. 
Valor de obra calculado: 1.100 bilhão   |  Prazo de obra: 36 meses   |  Lucro estimado: 20%

# Análise de Sensibilidade - Resultados
Quando 3.00% de IC, as chances de ganho são 6.18% maior em relação a IC 4.15% e 10.92% maior em relação a IC 5.49%.
Quando 4.15% de IC, as chances de ganho são 6.18% menor em relação a IC 3.00% e 4.74% maior em relação a IC 5.49%.
Quando 5.49% de IC, as chances de ganho são 10.92% menor em relação a IC 3.00% e 4.74% menor em relação a IC 4.15%.

## Para um IC de 3.00%:
•	ICC (Índice de Cobertura Contingencial): 0.42 (Limiar de segurança: 1.1)
•	Cobertura de riscos: 99.88%
•	Probabilidade de insuficiência: 0.12%
•	Exposição do resultado líquido à insuficiência: 15.98% do resultado líquido

## Para um IC de 4.15% e 5,49%:
•	ICC (Índice de Cobertura Contingencial): 0.31 (Limiar de segurança: 1.1)
•	ICC (Índice de Cobertura Contingencial): 0.23 (Limiar de segurança: 1.1)
•	Cobertura de riscos: 100.00%
•	Probabilidade de insuficiência: 0.00%
•	Exposição do resultado líquido à insuficiência: 0.00% do resultado líquido


## Análise de Sensibilidade:
•	Para um IC de 8.00%, o ICC ajustado é 0.16 e compromete 0.00% do resultado líquido
•	Para um IC de 4.89%, o ICC ajustado é 0.26 e compromete 0.00% do resultado líquido
•	Para um IC de 3.33%, o ICC ajustado é 0.38 e compromete 0.00% do resultado líquido
•	Para um IC de 2.56%, o ICC ajustado é 0.50 e  compromete 1.20% do resultado líquido
•	Para um IC de 1.78%, o ICC ajustado é 0.71 e  compromete 1.49% do resultado líquido
•	Para um IC de 1.00%, o ICC ajustado é 1.27 e compromete 2.68% do resultado líquido

O IC com maior competitividade é de 3,33%

## Estrutura do Projeto

A estrutura de diretórios do projeto foi organizada da seguinte forma:
```
├── README.md 
├── data
│ ├── processed
│ └── raw
├── models
├── notebooks 
├── reports
│ └── figures 
├── requirements.txt
├── src
```

## Próximos Passos

Os próximos passos poderiam explorar a faixas de valores de obras e como os índices de contingência se comportam com obras de valores menores e maiores, inclusive quais são os clusters de valores de obra os quais o ICC performa semelhantemente. 





