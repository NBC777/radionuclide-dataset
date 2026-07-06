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

import sys
import argparse
from pathlib import Path
from datetime import datetime

import pandas as pd
import numpy as np
import yaml

# ============================================================================
# CLASSE PRINCIPAL
# ============================================================================

class DataPreprocessor:
    """Classe para pré-processamento automatizado de dados."""
    
    def __init__(self, config_file='config.yaml'):
        """
        Inicializa o pré-processador com um arquivo de configuração.
        
        Parâmetros:
        -----------
        config_file : str
            Caminho para o arquivo YAML de configuração
        """
        self.config = self._carregar_config(config_file)
        self.df = None
        self.metadata = {}
        
    def _carregar_config(self, config_file):
        """Carrega a configuração do arquivo YAML."""
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            print(f"Configuração carregada: {config_file}")
            return config
        except FileNotFoundError:
            print(f"ERRO: Arquivo de configuração '{config_file}' não encontrado!")
            sys.exit(1)
        except yaml.YAMLError as e:
            print(f"ERRO: Arquivo YAML inválido: {e}")
            sys.exit(1)
    
    def _encontrar_arquivo_entrada(self):
        """
        Encontra automaticamente o arquivo de entrada na pasta data.
        
        Retorna:
        --------
        Path: Caminho completo para o arquivo encontrado
        """
        pasta_data = Path(self.config['geral']['pasta_dados'])
        arquivo_config = self.config['entrada']['arquivo']
        
        # Tenta encontrar o arquivo específico
        arquivo = pasta_data / arquivo_config
        
        if arquivo.exists():
            return arquivo
        
        # Se não encontrar, tenta encontrar qualquer arquivo .xlsx, .csv, .ods
        padroes = ['*.xlsx', '*.csv', '*.ods', '*.xls']
        for padrao in padroes:
            arquivos = list(pasta_data.glob(padrao))
            if arquivos:
                print(f"Arquivo '{arquivo_config}' não encontrado. Usando: {arquivos[0].name}")
                return arquivos[0]
        
        raise FileNotFoundError(f"Nenhum arquivo de dados encontrado em {pasta_data}/")
    
    def _carregar_dados(self, arquivo):
        """
        Carrega os dados do arquivo de entrada.
        
        Parâmetros:
        -----------
        arquivo : Path
            Caminho para o arquivo de dados
        """
        print(f"\n Carregando dados: {arquivo.name}")
        
        extensao = arquivo.suffix.lower()
        
        try:
            if extensao == '.xlsx':
                self.df = pd.read_excel(
                    arquivo,
                    sheet_name=self.config['entrada']['planilha']
                )
            elif extensao == '.csv':
                separador = self.config['entrada'].get('separador', ',')
                if separador == '\\t':
                    separador = '\t'
                self.df = pd.read_csv(
                    arquivo,
                    sep=separador,
                    encoding=self.config['entrada'].get('encoding', 'utf-8')
                )
            elif extensao == '.ods':
                self.df = pd.read_excel(arquivo, engine='odf')
            else:
                raise ValueError(f"Formato não suportado: {extensao}")
            
            print(f"Dados carregados: {self.df.shape[0]} linhas × {self.df.shape[1]} colunas")
            
        except Exception as e:
            print(f"ERRO ao carregar dados: {e}")
            sys.exit(1)
    
    def _classificar_material(self, id_amostra):
        """
        Classifica o material baseado no ID da amostra.
        
        Parâmetros:
        -----------
        id_amostra : str
            Identificador da amostra
            
        Retorna:
        --------
        str: Tipo de material classificado
        """
        id_str = str(id_amostra).upper()
        regras = self.config.get('classificacao', {}).get('regras', {})
        padrao = self.config.get('classificacao', {}).get('padrao', 'Outro')
        
        for prefixo, material in regras.items():
            if id_str.startswith(prefixo) or prefixo in id_str:
                return material
        
        return padrao
    
    def _validar_colunas(self, colunas_numericas):
        """
        Valida se todas as colunas necessárias existem no DataFrame.
        
        Parâmetros:
        -----------
        colunas_numericas : list
            Lista de colunas numéricas esperadas
            
        Retorna:
        --------
        list: Colunas que foram encontradas
        """
        print("\n🔍 Validando colunas...")
        
        colunas_encontradas = []
        colunas_faltando = []
        
        for col in colunas_numericas:
            if col in self.df.columns:
                colunas_encontradas.append(col)
                print(f"{col}")
            else:
                colunas_faltando.append(col)
                print(f"{col} - NÃO encontrada")
        
        if colunas_faltando:
            print(f"\n ATENÇÃO: {len(colunas_faltando)} colunas não encontradas!")
            print(f"  Colunas disponíveis: {self.df.columns.tolist()}")
            print("  Ajuste o arquivo config.yaml")
            return []
        
        return colunas_encontradas
    
    def processar(self):
        """
        Executa todo o fluxo de pré-processamento.
        """
        print("="*70)
        print(" INICIANDO PRÉ-PROCESSAMENTO AUTOMATIZADO")
        print("="*70)
        
        # ----------------------------------------------------------------
        # PASSO 1: Localizar e carregar dados
        # ----------------------------------------------------------------
        arquivo = self._encontrar_arquivo_entrada()
        self._carregar_dados(arquivo)
        
        # ----------------------------------------------------------------
        # PASSO 2: Validar colunas
        # ----------------------------------------------------------------
        colunas_numericas = self.config['colunas']['numericas']
        colunas_encontradas = self._validar_colunas(colunas_numericas)
        
        if not colunas_encontradas:
            return
        
        # ----------------------------------------------------------------
        # PASSO 3: Converter para tipos numéricos
        # ----------------------------------------------------------------
        print("\n Convertendo colunas para numéricas...")
        for col in colunas_encontradas:
            self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
            nulos = self.df[col].isnull().sum()
            status = "OK" if nulos == 0 else f"⚠️ {nulos} NaN"
            print(f"  {col}: {self.df[col].dtype} ({status})")
        
        # ----------------------------------------------------------------
        # PASSO 4: Classificar materiais
        # ----------------------------------------------------------------
        print("\n  Classificando materiais...")
        coluna_id = self.config['colunas']['identificador']
        self.df['Material'] = self.df[coluna_id].apply(self._classificar_material)
        
        for material, count in self.df['Material'].value_counts().items():
            print(f"  {material}: {count} amostras ({count/len(self.df)*100:.1f}%)")
        
        # ----------------------------------------------------------------
        # PASSO 5: Reorganizar colunas
        # ----------------------------------------------------------------
        print("\n Reorganizando colunas...")
        ordem_final = [coluna_id, 'Material'] + colunas_encontradas
        self.df = self.df[ordem_final]
        print(f"   Ordem final: {len(ordem_final)} colunas")
        
        # ----------------------------------------------------------------
        # PASSO 6: Verificação de qualidade
        # ----------------------------------------------------------------
        print("\n Verificando qualidade dos dados...")
        
        total_nulos = self.df[colunas_encontradas].isnull().sum().sum()
        if total_nulos == 0:
            print(" Nenhum valor ausente encontrado!")
        else:
            print(f" {total_nulos} valores ausentes encontrados")
            for col in colunas_encontradas:
                nulos = self.df[col].isnull().sum()
                if nulos > 0:
                    print(f"    - {col}: {nulos} ausentes")
        
        duplicados = self.df[coluna_id].duplicated().sum()
        if duplicados == 0:
            print(" Nenhum ID duplicado encontrado!")
        else:
            print(f" {duplicados} IDs duplicados encontrados!")
        
        self.metadata.update({
            'total_nulos': total_nulos,
            'duplicados': duplicados,
            'num_amostras': len(self.df),
            'num_colunas': len(self.df.columns),
            'num_materiais': self.df['Material'].nunique()
        })
        
        # ----------------------------------------------------------------
        # PASSO 7: Salvar arquivos processados
        # ----------------------------------------------------------------
        self._salvar_resultados()
        
        # ----------------------------------------------------------------
        # PASSO 8: Gerar relatórios
        # ----------------------------------------------------------------
        if self.config['saida'].get('criar_relatorio', True):
            self._gerar_relatorio(colunas_encontradas)
        
        if self.config['saida'].get('salvar_estatisticas', True):
            self._salvar_estatisticas(colunas_encontradas)
        
        # ----------------------------------------------------------------
        # Finalização
        # ----------------------------------------------------------------
        print("\n" + "="*70)
        print(" PRÉ-PROCESSAMENTO CONCLUÍDO COM SUCESSO!")
        print("="*70)
        print(f"\n Resumo final:")
        print(f"  Amostras: {self.metadata['num_amostras']}")
        print(f"  Colunas: {self.metadata['num_colunas']}")
        print(f"  Materiais: {self.metadata['num_materiais']}")
        print(f"  Valores NaN: {self.metadata['total_nulos']}")
        print(f"  IDs duplicados: {self.metadata['duplicados']}")
        
        pasta_saida = self.config['geral']['pasta_saida']
        print(f"\n Arquivos salvos em: {pasta_saida}/")
    
    def _salvar_resultados(self):
        """Salva os dados processados em múltiplos formatos."""
        print("\n Salvando arquivos processados...")
        
        pasta_saida = Path(self.config['geral']['pasta_saida'])
        nome_base = self.config['geral'].get('arquivo_saida', 'dados_processados')
        
        # Criar diretórios
        for subdir in ['dados', 'documentacao', 'codigo']:
            (pasta_saida / subdir).mkdir(parents=True, exist_ok=True)
        
        formatos = self.config['saida'].get('formatos', ['csv', 'parquet', 'xlsx'])
        
        for formato in formatos:
            try:
                if formato == 'csv':
                    arquivo = pasta_saida / 'dados' / f'{nome_base}.csv'
                    self.df.to_csv(arquivo, index=False, encoding='utf-8-sig')
                    print(f" CSV: {arquivo.name}")
                    
                elif formato == 'parquet':
                    arquivo = pasta_saida / 'dados' / f'{nome_base}.parquet'
                    self.df.to_parquet(arquivo, compression='snappy')
                    print(f" Parquet: {arquivo.name}")
                    
                elif formato == 'xlsx':
                    arquivo = pasta_saida / 'dados' / f'{nome_base}.xlsx'
                    self.df.to_excel(arquivo, index=False, engine='openpyxl')
                    print(f" Excel: {arquivo.name}")
                    
            except Exception as e:
                print(f"  Erro ao salvar {formato}: {e}")
    
    def _gerar_relatorio(self, colunas_numericas):
        """Gera relatório de validação em texto."""
        print("\n📄 Gerando relatório de validação...")
        
        relatorio = []
        relatorio.append("="*70)
        relatorio.append("RELATÓRIO DE VALIDAÇÃO DO DATASET")
        relatorio.append("="*70)
        relatorio.append(f"\n DIMENSÕES: {self.df.shape[0]} linhas × {self.df.shape[1]} colunas")
        relatorio.append(f" Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        
        # Valores ausentes
        relatorio.append("\n" + "-"*70)
        relatorio.append("(1) VALORES AUSENTES (NaN):")
        for col in colunas_numericas:
            nulos = self.df[col].isnull().sum()
            pct = (nulos / len(self.df)) * 100
            status = " OK" if nulos == 0 else f"{nulos} ({pct:.1f}%)"
            relatorio.append(f"  {status} - {col}")
        
        # IDs duplicados
        relatorio.append("\n" + "-"*70)
        relatorio.append(" (2) IDs DUPLICADOS:")
        coluna_id = self.config['colunas']['identificador']
        duplicados = self.df[coluna_id].duplicated().sum()
        status = "OK" if duplicados == 0 else f" {duplicados} duplicados"
        relatorio.append(f"  {status}")
        
        # Distribuição de materiais
        relatorio.append("\n" + "-"*70)
        relatorio.append(" (3) DISTRIBUIÇÃO DOS MATERIAIS:")
        for material, count in self.df['Material'].value_counts().items():
            pct = (count / len(self.df)) * 100
            relatorio.append(f"  {material}: {count} amostras ({pct:.1f}%)")
        
        # Estatísticas descritivas
        relatorio.append("\n" + "-"*70)
        relatorio.append(" (4) ESTATÍSTICAS DESCRITIVAS:")
        for col in colunas_numericas[:5]:  # Mostra as 5 primeiras
            relatorio.append(f"\n  📊 {col}:")
            relatorio.append(f"    Média: {self.df[col].mean():.4f}")
            relatorio.append(f"    Desvio: {self.df[col].std():.4f}")
            relatorio.append(f"    Mínimo: {self.df[col].min():.4f}")
            relatorio.append(f"    Máximo: {self.df[col].max():.4f}")
            relatorio.append(f"    Mediana: {self.df[col].median():.4f}")
        
        relatorio.append("\n" + "="*70)
        relatorio.append(" VALIDAÇÃO CONCLUÍDA")
        relatorio.append("="*70)
        
        # Salvar
        pasta_saida = Path(self.config['geral']['pasta_saida'])
        arquivo = pasta_saida / 'documentacao' / 'relatorio_validacao.txt'
        
        with open(arquivo, 'w', encoding='utf-8') as f:
            f.write("\n".join(relatorio))
        
        print(f" Relatório salvo: {arquivo}")
    
    def _salvar_estatisticas(self, colunas_numericas):
        """Salva estatísticas descritivas em CSV."""
        print("\n Salvando estatísticas descritivas...")
        
        stats = []
        for col in colunas_numericas:
            stats.append({
                'Coluna': col,
                'Média': self.df[col].mean(),
                'Desvio Padrão': self.df[col].std(),
                'Mínimo': self.df[col].min(),
                'Máximo': self.df[col].max(),
                'Mediana': self.df[col].median(),
                'Q1': self.df[col].quantile(0.25),
                'Q3': self.df[col].quantile(0.75),
                'Valores Ausentes': self.df[col].isnull().sum()
            })
        
        df_stats = pd.DataFrame(stats)
        
        pasta_saida = Path(self.config['geral']['pasta_saida'])
        arquivo = pasta_saida / 'documentacao' / 'estatisticas_descritivas.csv'
        
        df_stats.to_csv(arquivo, index=False, encoding='utf-8-sig')
        print(f" Estatísticas salvas: {arquivo}")


# ============================================================================
# EXECUÇÃO PRINCIPAL
# ============================================================================

def main():
    """Função principal."""
    parser = argparse.ArgumentParser(
        description='Pré-processamento automatizado de dados de radionuclídeos'
    )
    parser.add_argument(
        '--config',
        default='config.yaml',
        help='Arquivo de configuração YAML (padrão: config.yaml)'
    )
    parser.add_argument(
        '--generate-config',
        action='store_true',
        help='Gera um arquivo de configuração modelo'
    )
    
    args = parser.parse_args()
    
    # Gerar configuração modelo
    if args.generate_config:
        config_modelo = """# ============================================================================
# CONFIGURAÇÃO DO PRÉ-PROCESSAMENTO
# ============================================================================

# Configurações gerais
geral:
  pasta_dados: "data"  # Pasta onde estão os dados de entrada
  pasta_saida: "dataset_zenodo"  # Pasta onde serão salvos os resultados
  arquivo_saida: "dados_processados"  # Nome base para os arquivos de saída

# Configuração do arquivo de entrada
entrada:
  arquivo: "OriginalData.xlsx"  # Nome do arquivo (.xlsx, .csv, .ods)
  planilha: 0  # Índice ou nome da planilha (para Excel)
  separador: ","  # Para CSV ("," ou ";" ou "\\t")
  encoding: "utf-8"  # Codificação do arquivo

# Configuração das colunas
colunas:
  identificador: "Samples"  # Coluna que identifica cada amostra
  numericas:  # Colunas com dados numéricos
    - "226Ra"
    - "232Th"
    - "40K"
    - "Raeq"
    - "Theq"
    - "Keq"
    - "IA"
    - "IB"
    - "IG"

# Configuração da classificação de materiais
classificacao:
  regras:
    CON: "Concreto"
    TIJ: "Tijolo"
    GRA: "Granito"
    CIN: "Cinza"
    ARE: "Areia"
    CIM: "Cimento"
    ARG: "Argamassa"
    TEL: "Telha"
  padrao: "Outro"

# Configuração dos formatos de saída
saida:
  formatos:
    - "csv"
    - "parquet"
    - "xlsx"
  criar_relatorio: true
  salvar_estatisticas: true
"""
        with open('config_modelo.yaml', 'w', encoding='utf-8') as f:
            f.write(config_modelo)
        print(" Arquivo 'config_modelo.yaml' criado!")
        print("   Renomeie para 'config.yaml' e ajuste conforme necessário.")
        return
    
    # Executar pré-processamento
    preprocessador = DataPreprocessor(args.config)
    preprocessador.processar()


if __name__ == "__main__":
    main()





#   python preprocessing.py --generate-config