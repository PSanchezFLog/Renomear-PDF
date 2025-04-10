import PyPDF2
import os
from Levenshtein import distance

def dividir_pdf(caminho_pdf, padrao, pasta_saida="pdf"):
    """
    Divide um PDF em arquivos separados com base em um padrão de texto.

    Args:
        caminho_pdf (str): Caminho do arquivo PDF de entrada.
        padrao (str): Padrão de texto que marca o final de cada informe.
        pasta_saida (str, opcional): Pasta para salvar os arquivos divididos.
    """

    if not os.path.exists(pasta_saida):
        os.makedirs(pasta_saida)

    with open(caminho_pdf, "rb") as arquivo_pdf:
        leitor_pdf = PyPDF2.PdfReader(arquivo_pdf)
        num_paginas = len(leitor_pdf.pages)
        inicio_informe = 0
        contador_arquivos = 1
        
        for pagina_atual in range(num_paginas):
            pagina = leitor_pdf.pages[pagina_atual]
            texto = pagina.extract_text()
            
            #verifica se o padrão está na página, com tolerância para pequenas diferenças de texto.
            if padrao in texto or distance(padrao, texto[-len(padrao)-3:-1]) < 5:
                escritor_pdf = PyPDF2.PdfWriter()
                
                for num_pagina in range(inicio_informe, pagina_atual + 1):
                    escritor_pdf.add_page(leitor_pdf.pages[num_pagina])
                
                nome_arquivo_saida = os.path.join(pasta_saida, f"informe_{contador_arquivos}.pdf")
                
                with open(nome_arquivo_saida, "wb") as arquivo_saida:
                    escritor_pdf.write(arquivo_saida)
                    
                inicio_informe = pagina_atual + 1
                contador_arquivos += 1

# Substitua 'seu_arquivo.pdf' pelo caminho do seu arquivo PDF e execute a função.
dividir_pdf(r"INFORMES DE RENDIMENTOS.pdf", "Aprovado pela Instrução Normativa RFB nº 2.060, de 13 de dezembro de 2021")

