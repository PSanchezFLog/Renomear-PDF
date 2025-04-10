# Renomeador Automático de Comprovantes de Rendimentos (PDF)
###### Versão 1.1.0
## Funcionalidade principal: Renomear grandes volumes de PDF referente a Comprovantes de Rendimentos


### 1. Como utilizar:

1. Utilizar o separador caso o arquivo com os informes todos juntos (em um arquivo só maior)
2. Buscar os arquivos e direcionar o programa para a pasta correta
3. Criar uma pasta de nome pdf onde os PDF's vão ficar contidos
4. A pasta deve estar no mesmo local que o arquivo main.py
5. Executar o programa main.py (necessário ter Python instalado e a biblioteca PyPDF2. Para instalar a biblioteca, execute o comando: `pip install PyPDF2`)
6. Alguns arquivos podem não ser renomeados automaticamente, nesses casos, a renomeação manual será necessária

### 2. Processo de Renomeação:

O programa extrai informações sobre o nome do titular do comprovante de rendimento em um arquivo PDF e utiliza esses dados para gerar um novo nome de arquivo padronizado.
Exemplo: "Comprovante_001.pdf" pode ser renomeado para "Nome Exemplo.pdf"


### 3. Atualizações:

##### Patch 1.1.0

1. Melhoria na aquisição de dados do PDF
2. Redução no trabalho manual realizado


#### Patch 1.2.0

1. Criação do arquivo para separa PDF's


### 4. Limitações:

##### Limitações
*   O programa pode ter dificuldades em extrair informações de PDFs com layouts muito diferentes ou imagens em vez de texto.
*   Nesses casos, a renomeação manual será necessária.


### 5. Contato:

##### Contato:
e-mail: pedro.sanchez@fatlog.com.br
celular: (11) 91933-5693

### 6. Requisitos do Programa:

* Python 3.x
* PyPDF2

