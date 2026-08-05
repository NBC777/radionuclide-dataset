# Código para Pré-processamento do Dataset de Radionuclídeos

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
        