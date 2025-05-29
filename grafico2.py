import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import rcParams

def plot_nivel_temp_vento():
    # Configurações visuais - apenas parâmetros válidos
    plt.style.use('seaborn-v0_8-whitegrid')
    rcParams.update({
        'font.size': 12,
        'font.family': 'sans-serif',
        'axes.titlesize': 16,
        'axes.titleweight': 'bold',
        'axes.labelweight': 'bold',
        'axes.grid': True,
        'grid.alpha': 0.15,
        'grid.linestyle': '-',
        'grid.color': '#bbbbbb',
        'legend.frameon': True,
        'legend.framealpha': 0.95,
        'legend.shadow': False,
        'legend.edgecolor': 'gray',
        'figure.titlesize': 18
    })

    # Caminho do arquivo
    file_path = 'C:/Users/ggoulart/OneDrive - Libra Comercializadora de Energia/Área de Trabalho/FERRAMENTAS/tcc/9_09_23.dat'

    # Carregamento dos dados
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            header_lines = [next(f) for _ in range(4)]

        column_names = [name.strip().strip('"') for name in header_lines[1].strip().split(',')]

        # Tenta ler os dados com diferentes formatos de data
        for date_parse_method in [
            {'parse_dates': [0], 'dayfirst': True},
            {'parse_dates': [0], 'format': 'mixed'},
            {'parse_dates': [0], 'infer_datetime_format': True}
        ]:
            try:
                df = pd.read_csv(file_path, skiprows=4, header=None, 
                               names=column_names, **date_parse_method)
                break
            except ValueError:
                continue

        # Garante que o índice é datetime
        df.set_index(column_names[0], inplace=True)
        if not isinstance(df.index, pd.DatetimeIndex):
            df.index = pd.to_datetime(df.index, errors='coerce')
        
        # Converte as colunas para numérico
        df = df.apply(pd.to_numeric, errors='coerce')
        
        # Filtra o período
        df = df.loc['2023-08-07':'2023-08-10'].copy() #Altere para a data desejada
        
    except Exception as e:
        print(f"Erro ao carregar dados: {e}")
        if 'df' in locals():
            print("Amostra da coluna de datas:")
            print(df.iloc[:,0].head() if len(df.columns) > 0 else "DataFrame vazio")
        return

    # Verifica se há dados após o filtro
    if df.empty:
        print("Nenhum dado encontrado para o período especificado")
        return

    # Gráfico
    fig, ax1 = plt.subplots(figsize=(24, 9), dpi=120)
    
    # Nível da água (esquerda)
    nivel_line = ax1.plot(df.index, df['Nivel_Avg'], color='#1f77b4', linewidth=2.2, label='Nível da Água (cm)')
    ax1.set_ylabel('Nível (cm)', fontsize=18, fontweight='bold', color='#1f77b4', labelpad=15)
    ax1.tick_params(axis='y', labelcolor='#1f77b4', labelsize=18)
    ax1.set_ylim(df['Nivel_Avg'].min() * 0.9, df['Nivel_Avg'].max() * 1.1)

    # V (direita)
    ax2 = ax1.twinx()
    temp_line = ax2.plot(df.index, df['Vel_1m_Avg'], color='#ff6600', linewidth=2, label='Velocidade do Vento (m/s)')
    ax2.set_ylabel('Velocidade do Vento (m/s)', fontsize=18, fontweight='bold', color='#ff6600', labelpad=15)
    ax2.tick_params(axis='y', labelcolor='#ff6600', labelsize=18)
    ax2.set_ylim(df['Vel_1m_Avg'].min() * 0.9, df['Vel_1m_Avg'].max() * 1.1)

    # # # Vento (terciário à direita)
    ax3 = ax1.twinx()
    ax3.spines['right'].set_position(('axes', 1.05))  # deslocamento
    vento_line = ax3.plot(df.index, df['Uy_Avg'], color='#339966', linewidth=2, label='Componente V (m/s)')
    ax3.set_ylabel('Componente V (m/s)', fontsize=18, fontweight='bold', color='#339966', labelpad=15)
    ax3.tick_params(axis='y', labelcolor='#339966', labelsize=18)
    ax3.set_ylim(df['Uy_Avg'].min() * 0.9, df['Uy_Avg'].max() * 1.1)
    # ax3.set_ylim(-5, 5)
    # # Eixo x - configuração robusta para ticks
    ax1.set_xlabel('Data', fontsize=20, fontweight='bold', labelpad=15)
    
    locator = mdates.HourLocator(interval=6)  # Marcações a cada 6 horas
    formatter = mdates.DateFormatter('%d/%m %Hh')
    ax1.xaxis.set_major_locator(locator)
    ax1.xaxis.set_major_formatter(formatter)
    
    # Rotação e alinhamento dos labels
    plt.setp(ax1.get_xticklabels(), rotation=45, ha='right', fontsize=20)

    # Legenda unificada
    lines = nivel_line + temp_line  + vento_line
    labels = [l.get_label() for l in lines]
    leg = ax1.legend(lines, labels, loc='upper left', bbox_to_anchor=(0.01, 0.99),
                    fontsize=14, framealpha=0.95, shadow=True)
    leg.set_title('Variáveis Monitoradas', prop={'weight': 'bold', 'size': 12})

    # Período anotado
    periodo = f"Período: {df.index[0].strftime('%d/%m/%Y')} a {df.index[-1].strftime('%d/%m/%Y')}"
    plt.annotate(periodo,
                xy=(0.5, -0.30),
                xycoords='axes fraction',
                ha='center',
                fontsize=11,
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", lw=1))

    # Ajustes finais
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.2, top=0.9)

    # Salvamento
    output_path = 'C:/Users/ggoulart/OneDrive - Libra Comercializadora de Energia/Área de Trabalho/FERRAMENTAS/tcc/grafico_temp_nivel_vento7.png' # Altere para o diretorio desejado
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"Gráfico salvo com sucesso em: {output_path}")

if __name__ == '__main__':
    plot_nivel_temp_vento()