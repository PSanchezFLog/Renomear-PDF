# Projeto para alteração de nomes de PDF

import os
import re
import PyPDF2
import subprocess

def encontrar_nome_e_cpf_no_pdf(pdf_path, palavras_chave=["Nome Completo"]):
    """
    Tenta encontrar o nome e o CPF de uma pessoa em um arquivo PDF, procurando por palavras-chave.

    Args:
        pdf_path (str): O caminho para o arquivo PDF.
        palavras_chave (list): Uma lista de palavras-chave para procurar antes do nome.

    Returns:
        str: O nome e CPF extraídos do PDF ou None se não for encontrado.
    """
    try:
        with open(pdf_path, 'rb') as pdf_file: # Abre o arquivo conforme a necessidade, e após a utilização já fecha o arquivo novamente
            pdf_reader = PyPDF2.PdfReader(pdf_file) # Lê o arquivo e envia ele para memoria
            if not pdf_reader.pages:  # Verifica se o PDF está vazio
                print(f"Erro: PDF '{pdf_path}' está vazio.")
                return None

            for page in pdf_reader.pages:  # Itera por todas as páginas
                text = page.extract_text()
                if not text.strip():
                    print(f"Aviso: Página vazia no PDF '{pdf_path}'. Pulando para a próxima página.")
                    continue

                for palavra_chave in palavras_chave:
                    # Procura pela palavra-chave e extrai o texto após ela (agora incluindo CPF)
                    match = re.search(rf"{palavra_chave}\s*([\w\s\.\-]+)", text, re.IGNORECASE)
                    if match:
                        nome_e_cpf = match.group(1).strip()
                        if nome_e_cpf:
                            return nome_e_cpf

            print(f"Aviso: Nenhuma palavra-chave encontrada no PDF '{pdf_path}'. Tentando extrair a primeira linha.")
            # Se nenhuma palavra-chave for encontrada, tenta extrair a primeira linha
            first_page = pdf_reader.pages[0] 
            text = first_page.extract_text()
            if not text.strip():
                print(f"Erro: Não foi possível extrair texto do PDF '{pdf_path}'.")
                return None
            
            # Tenta extrair a primeira linha (agora incluindo CPF)
            nome_e_cpf = text.split('\n')[0].strip()
            if nome_e_cpf:
                return nome_e_cpf
            else:
                print(f"Erro: Primeira linha do PDF '{pdf_path}' não parece ser um nome válido.")
                return None

    except PyPDF2.errors.PdfReadError:
        print(f"Erro: O arquivo '{pdf_path}' não é um PDF válido.")
        return None
    except Exception as e:
        print(f"Erro ao processar '{pdf_path}': {e}")
        return None


def remover_cpf_do_nome(nome_e_cpf):
    """
    Remove o CPF (se presente) e o texto adicional do texto que contém o nome e o CPF.

    Args:
        nome_e_cpf (str): O texto que contém o nome, o CPF e possivelmente texto adicional.

    Returns:
        str: O nome sem o CPF e sem o texto adicional.
    """
    # Procura por um padrão de CPF (XXX.XXX.XXX-XX)
    cpf_pattern = r"\d{3}\.\d{3}\.\d{3}-\d{2}"
    
    # Remove o CPF
    nome_sem_cpf = re.sub(cpf_pattern, "", nome_e_cpf)
    
    # Expressão regular para capturar apenas o nome (letras maiúsculas, minúsculas, acentos e espaços)
    # e parar quando encontrar algo que não seja uma letra ou espaço.
    nome_pattern = r"^([A-Za-zÀ-ú]+(?:\s[A-Za-zÀ-ú]+)*)(?=[^A-Za-zÀ-ú\s]|$)"

    # Procura pelo nome usando a nova expressão regular
    match = re.search(nome_pattern, nome_sem_cpf)
    
    if match:
        nome = match.group(1).strip()
    else:
        nome = nome_sem_cpf.strip() # Caso não encontre o padrão, retorna o texto limpo.
    
    # Limpeza final
    nome = re.sub(r'[\/*?:"<>|\n]', "", nome)
    nome = re.sub(r'\s+', ' ', nome)
    nome = nome.strip()
    
    return nome


def renomear_pdf(diretorio):
    """
    Renomeia arquivos PDF em um diretório com base no nome extraído de cada PDF.

    Args:
        diretorio (str): O diretório onde os arquivos PDF estão localizados.
    """
    for filename in os.listdir(diretorio):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(diretorio, filename)
            nome_e_cpf = encontrar_nome_e_cpf_no_pdf(pdf_path)

            if nome_e_cpf:
                novo_nome = remover_cpf_do_nome(nome_e_cpf)

                if not novo_nome:
                    print(f"Erro: Nome extraído do PDF '{filename}' está vazio após a limpeza.")
                    continue

                novo_nome_completo = os.path.join(diretorio, novo_nome + ".pdf")

                # Verifica se o novo nome já existe
                contador = 1
                nome_base = novo_nome
                while os.path.exists(novo_nome_completo):
                    novo_nome = f"{nome_base} ({contador})"
                    novo_nome_completo = os.path.join(diretorio, novo_nome + ".pdf")
                    contador += 1

                try:
                    os.rename(pdf_path, novo_nome_completo)
                    print(f"Arquivo '{filename}' renomeado para '{novo_nome}.pdf'")
                except Exception as e:
                    print(f"Erro ao renomear '{filename}': {e}")

def chamarScript():
    subprocess.run(['python', '.\RenomearPDF\clearName.py'])


# Exemplo de uso:
diretorio_pdfs = r"C:\Users\pedro.sanchez\Projetos\RenomearPDF\pdf"  # Substitua pelo seu diretório
renomear_pdf(diretorio_pdfs)
chamarScript()

