import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

def read_data(file):
    df = pd.read_excel(file, engine='xlrd')
    return df

def plot_data(df, show_lines):
    fig, ax1 = plt.subplots()

    color = 'tab:red'
    ax1.set_xlabel('Semana')
    ax1.set_ylabel('Cxs/Solv', color=color)
    ax1.bar(df['Semana'], df['Cxs/Solv'], color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()

    if show_lines['CINTA']:
        ax2.plot(df['Semana'], df['CINTA'], label='CINTA')
    if show_lines['ESPECIAL']:
        ax2.plot(df['Semana'], df['ESPECIAL'], label='ESPECIAL')
    if show_lines['GRANEL']:
        ax2.plot(df['Semana'], df['GRANEL'], label='GRANEL')
    if show_lines['POLPA']:
        ax2.plot(df['Semana'], df['POLPA'], label='POLPA')
    if show_lines['PVC']:
        ax2.plot(df['Semana'], df['PVC'], label='PVC')
    if show_lines['EXP']:
        ax2.plot(df['Semana'], df['EXP'], label='EXP')

    ax2.set_ylabel('Outras colunas', color='tab:blue')
    ax2.tick_params(axis='y', labelcolor='tab:blue')

    fig.legend()
    st.pyplot(fig)

def main():
    st.set_page_config(page_title="Gráfico de Barras e Linhas", layout="wide")
    st.title("Gráfico de Barras e Linhas")

    file = st.file_uploader("Selecione o arquivo Excel", type=["xlsx", "xls"])

    if file is not None:
        df = read_data(file)
        st.write(df)

        col_options = df.columns[1:].tolist()
        show_lines = {col: st.checkbox(col, value=True) for col in col_options}

        plot_data(df, show_lines)

if __name__ == '__main__':
    main()
