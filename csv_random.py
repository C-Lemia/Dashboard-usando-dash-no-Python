import pandas as pd
import numpy as np

# Gerando dados fictícios 1
np.random.seed(42)
meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
receita_bruta = np.random.randint(1000, 5000, size=12)
deducoes_receita = np.random.randint(200, 1000, size=12)
receita_liquida = receita_bruta - deducoes_receita
custos_produtos_vendidos = np.random.randint(500, 2000, size=12)
despesas_operacionais = np.random.randint(300, 1500, size=12)
resultado_bruto = receita_liquida - custos_produtos_vendidos
resultado_operacional = resultado_bruto - despesas_operacionais
ebitda = resultado_operacional - np.random.randint(100, 500, size=12)
impostos = np.random.randint(50, 300, size=12)
resultado_final = ebitda - impostos

dados = {
    "Mes": meses,
    "Receita_Operacional_Bruta": receita_bruta,
    "Deducoes_Receita_Bruta": deducoes_receita,
    "Receita_Operacional_Liquida": receita_liquida,
    "Custos_Produtos_Vendidos": custos_produtos_vendidos,
    "Despesas_Operacionais": despesas_operacionais,
    "Resultado_Bruto": resultado_bruto,
    "Resultado_Operacional": resultado_operacional,
    "EBITDA": ebitda,
    "Impostos": impostos,
    "Resultado_Final": resultado_final
}

df_demonstrativo = pd.DataFrame(dados)
df_demonstrativo.to_csv('demonstrativo_financeiro.csv', index=False)

# Gerando dados fictícios 2
np.random.seed(42)
months = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
receitas = np.random.randint(10, 50, size=12)
custos = np.random.randint(5, 30, size=12)
lucros = receitas - custos
endividamento = np.random.uniform(20, 40, size=12)

data = {
    "Mes": months,
    "Receitas": receitas,
    "Custos": custos,
    "Lucros": lucros,
    "Endividamento": endividamento
}

df = pd.DataFrame(data)
df.to_csv('financial_data.csv', index=False)
