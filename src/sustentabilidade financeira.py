import pandas as pd

# Dados dos riscos
dados = {
    'Risco': [
        'Risco 1', 'Risco 2', 'Risco 3', 'Risco 4', 'Risco 5', 'Risco 6', 'Risco 7', 'Risco 8', 'Risco 9', 'Risco 10',
        'Risco 11', 'Risco 12', 'Risco 13', 'Risco 14', 'Risco 15', 'Risco 16', 'Risco 17', 'Risco 18', 'Risco 19', 'Risco 20',
        'Risco 21', 'Risco 22', 'Risco 23', 'Risco 24', 'Risco 25', 'Risco 26', 'Risco 27', 'Risco 28', 'Risco 29', 'Risco 30',
        'Risco 31', 'Risco 32', 'Risco 33', 'Risco 34', 'Risco 35', 'Risco 36', 'Risco 37', 'Risco 38', 'Risco 39', 'Risco 40',
        'Risco 41', 'Risco 42', 'Risco 43', 'Risco 44', 'Risco 45', 'Risco 46', 'Risco 47', 'Risco 48', 'Risco 49', 'Risco 50',
        'Risco 51', 'Risco 52', 'Risco 53', 'Risco 54', 'Risco 55', 'Risco 56', 'Risco 57', 'Risco 58', 'Risco 59', 'Risco 60',
        'Risco 61', 'Risco 62', 'Risco 63'
    ],
    'Impacto': [
        'médio', 'baixo', 'baixo', 'baixo', 'baixo', 'baixo', 'médio', 'médio', 'médio', 'médio',
        'médio', 'médio', 'médio', 'médio', 'médio', 'baixo', 'baixo', 'médio', 'médio', 'baixo',
        'baixo', 'baixo', 'médio', 'médio', 'baixo', 'médio', 'alto', 'baixo', 'médio', 'alto',
        'baixo', 'baixo', 'baixo', 'médio', 'médio', 'baixo', 'baixo', 'alto', 'baixo', 'médio',
        'baixo', 'médio', 'alto', 'alto', 'baixo', 'baixo', 'baixo', 'médio', 'baixo', 'baixo',
        'baixo', 'médio', 'baixo', 'baixo', 'alto', 'alto', 'alto', 'baixo', 'baixo', 'baixo',
        'baixo', 'baixo', 'baixo', 'baixo', 'baixo'
    ],
    'Probabilidade': [
        0.12, 0.16, 0.16, 0.16, 0.16, 0.16, 0.11, 0.12, 0.11, 0.11,
        0.12, 0.12, 0.12, 0.12, 0.11, 0.16, 0.16, 0.12, 0.11, 0.16,
        0.16, 0.16, 0.11, 0.12, 0.16, 0.12, 0.01, 0.16, 0.11, 0.01,
        0.15, 0.16, 0.16, 0.12, 0.12, 0.16, 0.16, 0.01, 0.15, 0.12,
        0.16, 0.12, 0.01, 0.01, 0.16, 0.16, 0.16, 0.12, 0.16, 0.16,
        0.16, 0.12, 0.16, 0.16, 0.01, 0.01, 0.01, 0.16, 0.16, 0.16,
        0.16, 0.16, 0.15, 0.16, 0.16
    ]
}

df = pd.DataFrame(dados)

# Mapeando impacto para valores numéricos conforme os intervalos especificados
impacto_valores = {'baixo': 1e6, 'médio': 3e6, 'alto': 5.5e6}  
df['Impacto Financeiro'] = df['Impacto'].map(impacto_valores)

# Calculando a reserva necessária para cada risco
df['Reserva Risco'] = df['Probabilidade'] * df['Impacto Financeiro']

# Calculando a Reserva Total de Contingência
reserva_total = df['Reserva Risco'].sum()

print("Reserva Total de Contingência Necessária: R$", reserva_total)
