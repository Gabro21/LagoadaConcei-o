import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from matplotlib import rcParams
from datetime import datetime

def plot_regressao_nivel_chuva():
    # Configurações visuais
    plt.style.use('seaborn-v0_8-whitegrid')
    rcParams.update({
        'font.size': 12,
        'font.family': 'sans-serif',
        'axes.titlesize': 16,
        'axes.titleweight': 'bold',
        'axes.labelweight': 'bold',
        'axes.grid': True,
        'grid.alpha': 0.3,
        'grid.linestyle': '--',
        'legend.frameon': True,
        'legend.framealpha': 0.95,
        'figure.titlesize': 18
    })

    # Caminho do arquivo
    file_path = 'C:/Users/ggoulart/OneDrive - Libra Comercializadora de Energia/Área de Trabalho/FERRAMENTAS/tcc/9_09_23.dat'

    try:
        # Ler cabeçalho para obter nomes das colunas
        with open(file_path, 'r', encoding='utf-8') as f:
            header_lines = [next(f) for _ in range(4)]

        column_names = [name.strip().strip('"') for name in header_lines[1].strip().split(',')]

        # Função para interpretar datas no formato correto
        dateparse = lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S')

        # Carregar dados
        df = pd.read_csv(
            file_path,
            skiprows=4,
            header=None,
            names=column_names,
            parse_dates=['TIMESTAMP'],
            date_parser=dateparse
        )

        df.set_index('TIMESTAMP', inplace=True)
        df = df.apply(pd.to_numeric, errors='coerce')
        df = df.loc['2023-08-07'].copy() #Altere para a data desejada

        # Verificar se as colunas necessárias existem
        if 'Nivel_Avg' not in df.columns or 'Uy_Avg' not in df.columns:
            print("Colunas 'Nivel_Avg' ou 'Uy_Avg' não encontradas no DataFrame")
            return

        # Remover valores nulos
        df_clean = df[['Nivel_Avg', 'Uy_Avg']].dropna() # Mude para as variaveis que deseja

        # Calcular regressão linear
        slope, intercept, r_value, p_value, std_err = stats.linregress(
            df_clean['Uy_Avg'], df_clean['Nivel_Avg']) 

        # Criar equação da reta
        line_eq = f'y = {slope:.2f}x + {intercept:.2f}\nR² = {r_value**2:.2f}'

        # Criar figura
        fig, ax = plt.subplots(figsize=(12, 8), dpi=120)

        # Gráfico de dispersão
        ax.scatter(df_clean['Uy_Avg'], df_clean['Nivel_Avg'], 
                   color='#1f77b4', alpha=0.6, s=50, label='Dados observados')

        # Linha de regressão
        ax.plot(df_clean['Uy_Avg'], 
                intercept + slope * df_clean['Uy_Avg'],
                color='#d62728', linewidth=2.5,
                label=f'Regressão Linear\n{line_eq}')

        # Configurações do gráfico
        ax.set_xlabel('Componente Uy do Vento (m/s)', fontsize=14, fontweight='bold')
        ax.set_ylabel('Nível da Água (cm)', fontsize=14, fontweight='bold')
        ax.set_title('Relação entre Componente Uy do Vento e Nível da Água', 
                     fontsize=16, pad=20, fontweight='bold')

        ax.grid(True, which='both', alpha=0.2)
        ax.legend(loc='upper left', fontsize=12, framealpha=0.95)

        # Ajustar layout
        plt.tight_layout()

        # Salvar gráfico
        output_path = 'C:/Users/ggoulart/OneDrive - Libra Comercializadora de Energia/Área de Trabalho/FERRAMENTAS/tcc/regressao_nivel_vento.png' #Altere para o caminho desejado
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        print(f"Gráfico de regressão salvo com sucesso em: {output_path}")
        print(f"Estatísticas da regressão:\n{line_eq}")

    except Exception as e:
        print(f"Erro ao processar dados: {e}")
        if 'df' in locals():
            print("Amostra dos dados:")
            print(df.head())

if __name__ == '__main__':
    plot_regressao_nivel_chuva()
