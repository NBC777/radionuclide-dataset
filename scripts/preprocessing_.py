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

import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rcParams
     

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
            # Tenta primeiro na pasta scripts/
            config_path = Path('scripts') / config_file
            if not config_path.exists():
                config_path = Path(config_file)  # Tenta na raiz
            
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            print(f"Configuração carregada: {config_path}")
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

        # Obter separador decimal da configuração
        separador_decimal = self.config['entrada'].get('decimal', '.')  # padrão: ponto
        
        try:
            if extensao == '.xlsx':
                self.df = pd.read_excel(
                    arquivo,
                    sheet_name=self.config['entrada']['planilha'],
                    decimal=separador_decimal
                )
            elif extensao == '.csv':
                separador = self.config['entrada'].get('separador', separador_decimal)
                if separador == '\\t':
                    separador = '\t'
                self.df = pd.read_csv(
                    arquivo,
                    sep=separador,  
                    encoding=self.config['entrada'].get('encoding', 'utf-8'),
                    decimal= separador_decimal
                )
            elif extensao == '.ods':
                self.df = pd.read_excel(arquivo, engine='odf', decimal=separador_decimal)
            else:
                raise ValueError(f"Formato não suportado: {extensao}")
            
            print(f"Dados carregados: {self.df.shape[0]} linhas x {self.df.shape[1]} colunas")
            
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
            status = "OK" if nulos == 0 else f" Warning {nulos} NaN"
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
        # ----------------------------------------------------------------
        # PASSO 8: Gerar relatórios
        # ----------------------------------------------------------------
        if self.config['saida'].get('criar_relatorio', True):
            self._gerar_relatorio(colunas_encontradas)
        
        if self.config['saida'].get('salvar_estatisticas', True):
            self._salvar_estatisticas(colunas_encontradas)
        
        # ----------------------------------------------------------------
        # PASSO 9: Gerar gráficos
        # ----------------------------------------------------------------
        if self.config['saida'].get('criar_graficos', True):
            self._gerar_graficos(colunas_encontradas) 

        # ----------------------------------------------------------------
        # PASSO 10: Salvar código para reprodutibilidade
        # ----------------------------------------------------------------
        if self.config['saida'].get('salvar_codigo', True):
            self._salvar_codigo()  # <-- ADICIONE ESTA LINHA
        
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
    
    #
    def _salvar_resultados(self):
        """Salva os dados processados para uso em Machine Learning."""
        print("\n Salvando arquivos processados...")
        
        pasta_saida = Path(self.config['geral']['pasta_saida'])
        nome_base = self.config['geral'].get('arquivo_saida', 'dados_processados')
        
        # Criar diretórios
        for subdir in ['dados', 'documentacao', 'codigo']:
            (pasta_saida / subdir).mkdir(parents=True, exist_ok=True)
        
        # ============================================================
        # 1. SALVAR CSV PARA ML (ponto decimal, vírgula separadora)
        # ============================================================
        arquivo_csv = pasta_saida / 'dados' / f'{nome_base}.csv'
        
        # PRIMEIRO: Garantir que todas as colunas numéricas são float
        colunas_numericas = self.config['colunas']['numericas']
        for col in colunas_numericas:
            if col in self.df.columns:
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
        
        # SEGUNDO: Salvar com separadores corretos
        self.df.to_csv(
            arquivo_csv,
            index=False,
            sep=',',           # Vírgula separa colunas
            decimal='.',       # Ponto separa decimais
            encoding='utf-8',
            float_format='%.12f'  # FORÇA 12 casas decimais com ponto
        )
        print(f" CSV para ML: {arquivo_csv.name}")
        print(f"   Formato: sep=',' decimal='.'")
        
        # ============================================================
        # 2. SALVAR EXCEL (para visualização)
        # ============================================================
        arquivo_xlsx = pasta_saida / 'dados' / f'{nome_base}.xlsx'
        self.df.to_excel(arquivo_xlsx, index=False, engine='openpyxl')
        print(f"Excel: {arquivo_xlsx.name}")
        
        # ============================================================
        # 3. SALVAR CSV COM TAB (para Excel PT-BR)
        # ============================================================
        arquivo_csv_br = pasta_saida / 'dados' / f'{nome_base}_BR.csv'
        
        # Para o formato brasileiro, precisamos converter para string com vírgula
        df_br = self.df.copy()
        for col in colunas_numericas:
            if col in df_br.columns:
                # Converter para string com vírgula decimal
                df_br[col] = df_br[col].apply(
                    lambda x: f"{x:.12f}".replace('.', ',') if pd.notna(x) else ''
                )
        
        df_br.to_csv(
            arquivo_csv_br,
            index=False,
            sep=';',
            encoding='utf-8-sig'
        )
        print(f" CSV (BR): {arquivo_csv_br.name}")
        
        print("\n Arquivos salvos com sucesso!")    

    
    def _gerar_relatorio(self, colunas_numericas):
        """Gera relatório de validação em texto."""   
        print("\n Gerando relatório de validação...")
        
        relatorio = []
        relatorio.append("="*70)
        relatorio.append("RELATÓRIO DE VALIDAÇÃO DO DATASET")
        relatorio.append("="*70)
        relatorio.append(f"\n DIMENSÕES: {self.df.shape[0]} linhas x {self.df.shape[1]} colunas")
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
            relatorio.append(f"\n {col}:")
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


    def _gerar_graficos(self, colunas_numericas):
        """
        Generates statistical plots for the dataset.
        All titles, labels, and legends are in English.
        """
        print("\n Generating statistical plots...")
        
        import matplotlib.pyplot as plt
        import seaborn as sns
        from matplotlib import rcParams
        import numpy as np
        
        # Configure style
        rcParams['font.size'] = 10
        rcParams['figure.dpi'] = 100
        sns.set_style("whitegrid")
        sns.set_palette("husl")
        
        pasta_saida = Path(self.config['geral']['pasta_saida'])
        pasta_figuras = pasta_saida / 'figuras'
        
        # Create figures folder
        pasta_figuras.mkdir(parents=True, exist_ok=True)
        print(f"Folder created: {pasta_figuras}")
        
        # ============================================================
        # 1. DISTRIBUTION OF MATERIALS
        # ============================================================
        fig, ax = plt.subplots(figsize=(10, 6))
        contagem = self.df['Material'].value_counts()
        colors = sns.color_palette("husl", len(contagem))
        bars = contagem.plot(kind='bar', ax=ax, color=colors)
        ax.set_title('Distribution of Materials in the Dataset', fontsize=14, fontweight='bold')
        ax.set_xlabel('Material Type', fontsize=12)
        ax.set_ylabel('Number of Samples', fontsize=12)
        ax.tick_params(axis='x', rotation=45)
        
        # Add value labels on bars
        for i, v in enumerate(contagem.values):
            ax.text(i, v + 0.5, str(v), ha='center', fontweight='bold', fontsize=11)
        
        plt.tight_layout()
        plt.savefig(pasta_figuras / 'distribuicao_materiais.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f" Material distribution")
        
        # ============================================================
        # 2. BOXPLOT OF RADIONUCLIDES
        # ============================================================
        fig, axes = plt.subplots(1, 3, figsize=(16, 6))
        
        radionuclides = ['226Ra', '232Th', '40K']
        titles = ['²²⁶Ra', '²³²Th', '⁴⁰K']
        
        for idx, (col, titulo) in enumerate(zip(radionuclides, titles)):
            if col in colunas_numericas:
                # Create boxplot with seaborn
                sns.boxplot(
                    data=self.df,
                    x='Material',
                    y=col,
                    ax=axes[idx],
                    palette='husl',
                    showfliers=True,
                    width=0.6
                )
                
                # Add jittered points to show distribution
                sns.stripplot(
                    data=self.df,
                    x='Material',
                    y=col,
                    ax=axes[idx],
                    color='black',
                    alpha=0.3,
                    size=3,
                    jitter=True
                )
                
                # Configure plot
                axes[idx].set_title(f'{titulo}', fontsize=13, fontweight='bold')
                axes[idx].set_xlabel('Material Type', fontsize=11)
                axes[idx].set_ylabel('Activity (Bq/kg)', fontsize=11)
                axes[idx].tick_params(axis='x', rotation=45, labelsize=9)
                axes[idx].tick_params(axis='y', labelsize=9)
                axes[idx].grid(True, alpha=0.3)
        
        plt.suptitle('Distribution of Radionuclides by Material Type', 
                    fontsize=15, fontweight='bold', y=1.02)
        plt.tight_layout()
        plt.savefig(pasta_figuras / 'boxplot_radionuclideos.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f" Boxplot of radionuclides")
        
        # ============================================================
        # 3. CORRELATION MATRIX
        # ============================================================
        fig, ax = plt.subplots(figsize=(10, 8))
        
        df_corr = self.df[colunas_numericas]
        corr = df_corr.corr()
        mask = np.triu(np.ones_like(corr, dtype=bool))
        
        sns.heatmap(
            corr, 
            mask=mask,
            annot=True, 
            fmt='.2f',
            cmap='RdBu_r',
            center=0,
            square=True,
            linewidths=0.5,
            cbar_kws={"shrink": 0.8, "label": "Correlation Coefficient"},
            ax=ax
        )
        ax.set_title('Correlation Matrix of Radionuclides and Indices', 
                    fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.savefig(pasta_figuras / 'matriz_correlacao.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"Correlation matrix")
        
        # ============================================================
        # 4. PAIRPLOT (relationships between main variables)
        # ============================================================
        vars_principais = ['226Ra', '232Th', '40K', 'Raeq', 'IA']
        df_pair = self.df[['Material'] + vars_principais].dropna()
        
        fig = sns.pairplot(
            df_pair,
            hue='Material',
            vars=vars_principais,
            diag_kind='kde',
            plot_kws={'alpha': 0.6, 's': 30},
            diag_kws={'alpha': 0.5}
        )
        fig.fig.suptitle('Relationships Between Radionuclides and Indices', 
                        y=1.02, fontsize=14, fontweight='bold')
        plt.savefig(pasta_figuras / 'pairplot_radionuclideos.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"Pairplot of main variables")
        
        # ============================================================
        # 5. ERROR BARS BY MATERIAL
        # ============================================================
        fig, ax = plt.subplots(figsize=(12, 6))
        
        stats_by_material = self.df.groupby('Material')[colunas_numericas].agg(['mean', 'std'])
        
        x = np.arange(len(stats_by_material.index))
        width = 0.25
        
        # 226Ra
        ax.bar(x - width, stats_by_material[('226Ra', 'mean')], width, 
            yerr=stats_by_material[('226Ra', 'std')],
            label='²²⁶Ra', capsize=3, color='#2E86AB', error_kw={'elinewidth': 2})
        
        # 232Th
        ax.bar(x, stats_by_material[('232Th', 'mean')], width,
            yerr=stats_by_material[('232Th', 'std')],
            label='²³²Th', capsize=3, color='#A23B72', error_kw={'elinewidth': 2})
        
        # 40K
        ax.bar(x + width, stats_by_material[('40K', 'mean')], width,
            yerr=stats_by_material[('40K', 'std')],
            label='⁴⁰K', capsize=3, color='#F18F01', error_kw={'elinewidth': 2})
        
        ax.set_xlabel('Material Type', fontsize=12)
        ax.set_ylabel('Mean Activity (Bq/kg)', fontsize=12)
        ax.set_title('Mean Activities by Material with Error Bars (±1σ)', 
                    fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(stats_by_material.index, rotation=45)
        ax.legend(loc='upper right', fontsize=11)
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(pasta_figuras / 'barras_erro_materiais.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"Error bars by material")
        
        # ============================================================
        # 6. HISTOGRAM OF INDICES
        # ============================================================
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        
        indices = ['IA', 'IB', 'IG']
        titles_idx = ['Activity Index (IA)', 'External Index (IB)', 'Internal Index (IG)']
        
        for idx, (col, titulo) in enumerate(zip(indices, titles_idx)):
            if col in colunas_numericas:
                self.df[col].hist(bins=20, ax=axes[idx], color='#2E86AB', 
                                edgecolor='black', alpha=0.7)
                axes[idx].axvline(self.df[col].mean(), color='red', linestyle='--', 
                                linewidth=2, label=f'Mean: {self.df[col].mean():.3f}')
                axes[idx].axvline(self.df[col].median(), color='green', linestyle='--',
                                linewidth=2, label=f'Median: {self.df[col].median():.3f}')
                axes[idx].set_title(titulo, fontsize=12, fontweight='bold')
                axes[idx].set_xlabel('Value', fontsize=11)
                axes[idx].set_ylabel('Frequency', fontsize=11)
                axes[idx].legend(fontsize=9)
                axes[idx].grid(True, alpha=0.3)
        
        plt.suptitle('Distribution of Radiation Indices', 
                    fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.savefig(pasta_figuras / 'histograma_indices.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"Histogram of indices")
        
        # ============================================================
        # 7. STATISTICAL SUMMARY TABLE (CORRIGIDA)
        # ============================================================
        fig, ax = plt.subplots(figsize=(14, 8))
        
        stats_table = self.df[colunas_numericas].describe().round(2)
        
        ax.axis('off')
        
        # Criar a tabela
        table = ax.table(
            cellText=stats_table.values,
            rowLabels=stats_table.index,
            colLabels=stats_table.columns,
            cellLoc='center',
            loc='center'
        )
        table.auto_set_font_size(False)
        table.set_fontsize(9)
        table.scale(1.2, 1.5)
        
        # Colorir cabeçalho - MÉTODO SEGURO
        # Itera sobre todas as células e colore apenas a primeira linha
        for (row, col), cell in table.get_celld().items():
            if row == 0:  # Primeira linha (cabeçalho)
                cell.set_facecolor('#2E86AB')
                cell.set_text_props(weight='bold', color='white')
            # Opcional: colorir a primeira coluna (índices) também
            elif col == 0:
                cell.set_facecolor('#E8F4F8')
                cell.set_text_props(weight='bold')
        
        ax.set_title('Statistical Summary of Numerical Variables', 
                    fontsize=14, fontweight='bold', pad=20)
        
        plt.tight_layout()
        plt.savefig(pasta_figuras / 'tabela_estatisticas.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f" Statistical summary table")
        
        print(f"\n All plots saved in: {pasta_figuras}/")

    def _salvar_codigo(self):
        """
        Copia os arquivos da pasta scripts/ para dataset_zenodo/codigo/
        para garantir reprodutibilidade no Zenodo.
        """
        print("\n Salvando código para reprodutibilidade...")
        
        import shutil
        from pathlib import Path
        
        # ============================================================
        # DEFINIR CAMINHOS
        # ============================================================
        pasta_scripts = Path('scripts')
        pasta_codigo = Path(self.config['geral']['pasta_saida']) / 'codigo'
        
        # Criar pasta codigo/ se não existir
        pasta_codigo.mkdir(parents=True, exist_ok=True)
        
        # ============================================================
        # 1. COPIAR O SCRIPT PRINCIPAL
        # ============================================================
        arquivo_origem = pasta_scripts / 'preprocessing_.py'
        arquivo_destino = pasta_codigo / 'preprocessing.py'
        
        if arquivo_origem.exists():
            shutil.copy2(arquivo_origem, arquivo_destino)
            print(f" Copiado: preprocessing_.py → preprocessing.py")
        else:
            print(f" Arquivo não encontrado: {arquivo_origem}")
        
        # ============================================================
        # 2. COPIAR O CONFIG.YAML
        # ============================================================
        arquivo_origem = pasta_scripts / 'config.yaml'
        arquivo_destino = pasta_codigo / 'config.yaml'
        
        if arquivo_origem.exists():
            shutil.copy2(arquivo_origem, arquivo_destino)
            print(f" Copiado: config.yaml")
        else:
            print(f"Arquivo não encontrado: {arquivo_origem}")
        
        # ============================================================
        # 3. COPIAR O REQUIREMENTS.TXT
        # ============================================================
        arquivo_origem = pasta_scripts / 'requirements.txt'
        arquivo_destino = pasta_codigo / 'requirements.txt'
        
        if arquivo_origem.exists():
            shutil.copy2(arquivo_origem, arquivo_destino)
            print(f" Copiado: requirements.txt")
        else:
            print(f"Arquivo não encontrado: {arquivo_origem}")
        
        # ============================================================
        # 4. CRIAR O ENVIRONMENT.YML
        # ============================================================
        arquivo_env = pasta_codigo / 'environment.yml'
        
        # Verifica se já existe na pasta scripts/
        env_origem = pasta_scripts / 'environment.yml'
        if env_origem.exists():
            shutil.copy2(env_origem, arquivo_env)
            print(f"Copiado: environment.yml")
        else:
            # Criar um environment.yml padrão  
            with open(arquivo_env, 'w', encoding='utf-8') as f:
                f.write("""name: project_cetem
        channels:
        - conda-forge
        - defaults
        dependencies:
        - python=3.10
        - pandas>=2.0.0
        - numpy>=1.24.0
        - matplotlib>=3.7.0
        - seaborn>=0.12.0
        - openpyxl>=3.1.0
        - pyarrow>=12.0.0
        - pyyaml>=6.0.0
        - scikit-learn>=1.3.0
        """)
                print(f"Criado: environment.yml (padrão)")
            
            # ============================================================
            # 5. CRIAR README.MD DO CÓDIGO
            # ============================================================
            readme_path = pasta_codigo / 'README.md'
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write("""# Código para Pré-processamento do Dataset de Radionuclídeos

        ## Arquivos

        | Arquivo | Descrição |
        |---------|-----------|
        | `preprocessing.py` | Script principal de pré-processamento |
        | `config.yaml` | Arquivo de configuração |
        | `requirements.txt` | Dependências Python (pip) |
        | `environment.yml` | Ambiente Conda completo |

        ##  Instalação

        ### Usando Conda (Recomendado)
        ```bash
        conda env create -f environment.yml
        conda activate project_cetem
        ```
                        
        ```python
        pip install -r requirements.txt
        ```
        ##  Saída

        O script gera:

            Dados processados: ../dados/ (CSV e Excel)

            Figuras: ../figuras/ (PNG, 300 DPI)

            Relatórios: ../documentacao/ (Validação e estatísticas)


        ## Licença

        MIT License

        Este código é parte do dataset disponível no Zenodo.
        """)
        
        print(f" Criado: README.md")

        print(f"\n Código salvo em: {pasta_codigo}/")   



                    


            








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
    AR: "Comercial sand"
    A: "Structural cement"
    PB: "Crushed rock"
    HB: "Hollow ceramic / bore brick"
    PP: "Stone dust"
    SB: "Solid clay brick"
    CB: "Concrete block brick"
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

#df = pd.read_csv(
#    'dataset_zenodo/dados/dados_processados.csv',
#    sep=',',
#    decimal='.',
#    encoding='utf-8'
#)