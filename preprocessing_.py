"""
Script de pré-processamento do dataset de radionuclídeos em materiais de construção
===============================================================================

Este script documenta todas as transformações aplicadas aos dados brutos
para gerar o dataset final disponível no Zenodo.

Autor: Nancy
Data: 2026-07-05
Versão: 1.0
Licença: MIT

Instruções de uso:
------------------
1. Coloque este script na mesma pasta que seu arquivo de dados original
2. Execute: python preprocessamento.py
3. Os arquivos processados serão salvos na pasta 'dataset_zenodo/dados/'

Requisitos:
-----------
pip install pandas numpy pyarrow openpyxl
"""

import os
import pandas as pd
import numpy as np
from datetime import datetime

# ============================================================================
# CONFIGURAÇÕES INICIAIS
# ============================================================================

# Nome do arquivo de entrada (ajuste conforme seu caso)
ARQUIVO_ORIGINAL = 'dados_coleta_original.xlsx'  # Pode ser .csv ou .xlsx

# Nomes das colunas numéricas (ajuste para os nomes exatos da sua tabela)
COLUNAS_NUMERICAS = [
    'Ra',      # Concentração de ²²⁶Ra (Bq/kg)
    'Th',      # Concentração de ²³²Th (Bq/kg)
    'K',       # Concentração de ⁴⁰K (Bq/kg)
    'Ra_eq',   # Concentração equivalente de rádio (Bq/kg)
    'Th_eq',   # Concentração equivalente de tório (Bq/kg)
    'K_eq',    # Concentração equivalente de potássio (Bq/kg)
    'I_a',     # Índice de radiação alfa (adimensional)
    'I_b',     # Índice de radiação beta (adimensional)
    'I_g'      # Índice de radiação gama (adimensional)
]

# Coluna de identificação (ajuste se necessário)
COLUNA_ID = 'ID'

# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================

def classificar_material(id_amostra):
    """
    Classifica o tipo de material com base no identificador da amostra.
    
    Esta função deve ser personalizada conforme a nomenclatura dos seus IDs.
    
    Parâmetros:
    -----------
    id_amostra : str ou int
        Identificador único da amostra
    
    Retorna:
    --------
    str: Tipo de material classificado
    """
    id_str = str(id_amostra).upper()
    
    # ===== REGRAS DE CLASSIFICAÇÃO (PERSONALIZE AQUI) =====
    if id_str.startswith('CON'):
        return 'Concreto'
    elif id_str.startswith('TIJ'):
        return 'Tijolo'
    elif id_str.startswith('GRA'):
        return 'Granito'
    elif 'CIN' in id_str:
        return 'Cinza'
    elif 'ARE' in id_str:
        return 'Areia'
    elif 'CIM' in id_str:
        return 'Cimento'
    elif 'ARG' in id_str:
        return 'Argamassa'
    elif 'TEL' in id_str:
        return 'Telha'
    else:
        return 'Outro'


def criar_diretorios():
    """Cria a estrutura de diretórios para os arquivos de saída."""
    diretorios = [
        'dataset_zenodo',
        'dataset_zenodo/dados',
        'dataset_zenodo/documentacao',
        'dataset_zenodo/codigo'
    ]
    
    for diretorio in diretorios:
        os.makedirs(diretorio, exist_ok=True)
    
    print(" Estrutura de diretórios criada:")
    for d in diretorios:
        print(f"{d}/")


def salvar_relatorio_validacao(df, colunas_numericas):
    """
    Gera um relatório de validação dos dados processados.
    
    Parâmetros:
    -----------
    df : pandas.DataFrame
        DataFrame processado
    colunas_numericas : list
        Lista com os nomes das colunas numéricas
    """
    relatorio = []
    relatorio.append("="*60)
    relatorio.append("RELATÓRIO DE VALIDAÇÃO DO DATASET")
    relatorio.append("="*60)
    relatorio.append(f"\n Dimensões: {df.shape[0]} linhas × {df.shape[1]} colunas")
    
    # Valores ausentes
    relatorio.append("\n (1) VALORES AUSENTES (NaN):")
    for col in colunas_numericas:
        nulos = df[col].isnull().sum()
        status = "OK" if nulos == 0 else "Warning"
        relatorio.append(f"   {status} {col}: {nulos} ausentes")
    
    # IDs duplicados
    duplicados = df[COLUNA_ID].duplicated().sum()
    status = "OK" if duplicados == 0 else "Waurning"
    relatorio.append(f"\n (2) IDs DUPLICADOS: {status} {duplicados} duplicados")
    
    # Distribuição de materiais
    relatorio.append("\n (3) DISTRIBUIÇÃO DOS MATERIAIS:")
    for material, count in df['Material'].value_counts().items():
        relatorio.append(f"   - {material}: {count} amostras ({count/len(df)*100:.1f}%)")
    
    # Estatísticas básicas
    relatorio.append("\n (4)  ESTATÍSTICAS DESCRITIVAS (principais colunas):")
    for col in colunas_numericas[:3]:  # Mostra apenas as 3 primeiras
        relatorio.append(f"\n  {col}:")
        relatorio.append(f"      Média: {df[col].mean():.2f}")
        relatorio.append(f"      Desvio: {df[col].std():.2f}")
        relatorio.append(f"      Mínimo: {df[col].min():.2f}")
        relatorio.append(f"      Máximo: {df[col].max():.2f}")
    
    relatorio.append("\n" + "="*60)
    relatorio.append(" VALIDAÇÃO CONCLUÍDA")
    relatorio.append("="*60)
    
    # Salvar relatório
    relatorio_texto = "\n".join(relatorio)
    with open('dataset_zenodo/documentacao/relatorio_validacao.txt', 'w', encoding='utf-8') as f:
        f.write(relatorio_texto)
    
    print(relatorio_texto)


# ============================================================================
# PROCESSAMENTO PRINCIPAL
# ============================================================================

def main():
    """
    Função principal que executa todo o fluxo de pré-processamento.
    """
    print("="*60)
    print(" INICIANDO PRÉ-PROCESSAMENTO DO DATASET")
    print("="*60)
    print(f"\n Arquivo de entrada: {ARQUIVO_ORIGINAL}")
    print(f" Colunas numéricas: {len(COLUNAS_NUMERICAS)} colunas")
    print("-"*60)
    
    # ------------------------------------------------------------------------
    # PASSO 1: Carregar dados brutos
    # ------------------------------------------------------------------------
    print("\n PASSO 1: Carregando dados brutos...")
    
    try:
        if ARQUIVO_ORIGINAL.endswith('.xlsx'):
            df = pd.read_excel(ARQUIVO_ORIGINAL)
            print(" Arquivo Excel carregado")
        elif ARQUIVO_ORIGINAL.endswith('.csv'):
            df = pd.read_csv(ARQUIVO_ORIGINAL)
            print(" Arquivo CSV carregado")
        elif ARQUIVO_ORIGINAL.endswith('.txt'):
            df = pd.read_csv(ARQUIVO_ORIGINAL, sep='\t')
            print(" Arquivo TXT (tab-separated) carregado")
        else:
            df = pd.read_csv(ARQUIVO_ORIGINAL)
            print(" Arquivo genérico carregado")
    except FileNotFoundError:
        print(f" ERRO: Arquivo '{ARQUIVO_ORIGINAL}' não encontrado!")
        print(f"Certifique-se de que o arquivo está na mesma pasta do script.")
        return
    except Exception as e:
        print(f"ERRO ao carregar arquivo: {e}")
        return
    
    print(f" Dimensões: {df.shape[0]} linhas × {df.shape[1]} colunas")
    
    # ------------------------------------------------------------------------
    # PASSO 2: Verificar colunas existentes
    # ------------------------------------------------------------------------
    print("\n PASSO 2: Verificando colunas...")
    
    colunas_encontradas = []
    colunas_faltando = []
    
    for col in COLUNAS_NUMERICAS:
        if col in df.columns:
            colunas_encontradas.append(col)
            print(f" {col} - encontrada")
        else:
            colunas_faltando.append(col)
            print(f" {col} - NÃO encontrada")
    
    if colunas_faltando:
        print(f"\n  ATENÇÃO: {len(colunas_faltando)} colunas não foram encontradas!")
        print(" Colunas disponíveis:", df.columns.tolist())
        print(" Ajuste a lista COLUNAS_NUMERICAS no script.")
        return
    
    # ------------------------------------------------------------------------
    # PASSO 3: Converter para tipos numéricos
    # ------------------------------------------------------------------------
    print("\n PASSO 3: Convertendo para tipos numéricos...")
    
    for col in colunas_encontradas:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        print(f"{col} → {df[col].dtype}")
    
    # ------------------------------------------------------------------------
    # PASSO 4: Criar coluna 'Material'
    # ------------------------------------------------------------------------
    print("\n PASSO 4: Criando coluna 'Material'...")
    
    df['Material'] = df[COLUNA_ID].apply(classificar_material)
    
    # Contagem de materiais
    print(" Coluna criada!")
    print("Distribuição:")
    for material, count in df['Material'].value_counts().items():
        print(f"  - {material}: {count} amostras")
    
    # ------------------------------------------------------------------------
    # PASSO 5: Reorganizar colunas
    # ------------------------------------------------------------------------
    print("\n PASSO 5: Reorganizando colunas...")
    
    ordem_final = [COLUNA_ID, 'Material'] + colunas_encontradas
    df = df[ordem_final]
    print(f"Ordem final: {df.columns.tolist()}")
    
    # ------------------------------------------------------------------------
    # PASSO 6: Verificação de qualidade
    # ------------------------------------------------------------------------
    print("\n PASSO 6: Verificação de qualidade...")
    
    # Valores ausentes
    total_nulos = df[colunas_encontradas].isnull().sum().sum()
    if total_nulos == 0:
        print(" Nenhum valor ausente (NaN) encontrado!")
    else:
        print(f"ATENÇÃO: {total_nulos} valores ausentes encontrados!")
        for col in colunas_encontradas:
            nulos = df[col].isnull().sum()
            if nulos > 0:
                print(f"      - {col}: {nulos} ausentes")
    
    # IDs duplicados
    duplicados = df[COLUNA_ID].duplicated().sum()
    if duplicados == 0:
        print("Nenhum ID duplicado encontrado!")
    else:
        print(f" ATENÇÃO: {duplicados} IDs duplicados encontrados!")
    
    # ------------------------------------------------------------------------
    # PASSO 7: Salvar arquivos
    # ------------------------------------------------------------------------
    print("\n PASSO 7: Salvando arquivos...")
    
    # Criar diretórios
    criar_diretorios()
    
    # Salvar formatos
    df.to_csv('dataset_zenodo/dados/dados_brutos.csv', index=False, encoding='utf-8-sig')
    print(" Ddados_brutos.csv (CSV universal)")
    
    df.to_parquet('dataset_zenodo/dados/dados_processados.parquet', compression='snappy')
    print(" Dados_processados.parquet (Parquet otimizado)")
    
    df.to_excel('dataset_zenodo/dados/dados_completos.xlsx', index=False)
    print("Dados_completos.xlsx (Excel acessível)")
    
    # ------------------------------------------------------------------------
    # PASSO 8: Gerar relatório de validação
    # ------------------------------------------------------------------------
    print("\n PASSO 8: Gerando relatório de validação...")
    salvar_relatorio_validacao(df, colunas_encontradas)
    
    # ------------------------------------------------------------------------
    # PASSO 9: Finalização
    # ------------------------------------------------------------------------
    print("\n" + "="*60)
    print(" PRÉ-PROCESSAMENTO CONCLUÍDO COM SUCESSO!")
    print("="*60)
    print(f"\n Arquivos gerados em: dataset_zenodo/dados/")
    print(" Relatório: dataset_zenodo/documentacao/relatorio_validacao.txt")
    print(f"\n Resumo final:")
    print(f"   - Amostras: {len(df)}")
    print(f"   - Colunas: {len(df.columns)}")
    print(f"   - Materiais: {df['Material'].nunique()}")
    print(f"   - Valores NaN: {total_nulos}")
    print(f"   - IDs duplicados: {duplicados}")
    print("\n Dataset pronto para publicação no Zenodo!")


# ============================================================================
# EXECUÇÃO
# ============================================================================

if __name__ == "__main__":
    main()
