# Projeto para alteração de nomes de PDF

import os
import re
import PyPDF2
import subprocess

def encontrar_nome_e_cpf_no_pdf(pdf_path, palavras_chave=["Nome Completo", "Nome Empresarial", "Razão Social"]):
    """
    Tenta encontrar o nome (pessoa física ou jurídica) e o CPF/CNPJ em um arquivo PDF, procurando por palavras-chave.

    Args:
        pdf_path (str): O caminho para o arquivo PDF.
        palavras_chave (list): Uma lista de palavras-chave para procurar antes do nome.

    Returns:
        str: O nome/razão social e CPF/CNPJ extraídos do PDF ou None se não for encontrado.
    """
    try:
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            if not pdf_reader.pages:
                print(f"Erro: PDF '{pdf_path}' está vazio.")
                return None

            for page in pdf_reader.pages:
                text = page.extract_text()
                if not text.strip():
                    print(f"Aviso: Página vazia no PDF '{pdf_path}'. Pulando para a próxima página.")
                    continue

                for palavra_chave in palavras_chave:
                    # Modifiquei a regex para incluir a barra e o hífen, comuns em CNPJ
                    match = re.search(rf"{palavra_chave}\s*([\w\s\.\-/]+)", text, re.IGNORECASE)
                    if match:
                        nome_ou_razao_social_e_id = match.group(1).strip()
                        if nome_ou_razao_social_e_id:
                            return nome_ou_razao_social_e_id

            print(f"Aviso: Nenhuma palavra-chave encontrada no PDF '{pdf_path}'. Tentando extrair a primeira linha.")
            first_page = pdf_reader.pages[0]
            text = first_page.extract_text()
            if not text.strip():
                print(f"Erro: Não foi possível extrair texto do PDF '{pdf_path}'.")
                return None

            nome_ou_razao_social_e_id = text.split('\n')[0].strip()
            if nome_ou_razao_social_e_id:
                return nome_ou_razao_social_e_id
            else:
                print(f"Erro: Primeira linha do PDF '{pdf_path}' não parece ser um nome/razão social válido.")
                return None

    except PyPDF2.errors.PdfReadError:
        print(f"Erro: O arquivo '{pdf_path}' não é um PDF válido.")
        return None
    except Exception as e:
        print(f"Erro ao processar '{pdf_path}': {e}")
        return None


def remover_cpf_do_nome(nome_ou_razao_social_e_id):
    """
    Remove o CPF ou CNPJ (se presente) e o texto adicional do texto extraído.

    Args:
        nome_ou_razao_social_e_id (str): O texto que contém o nome/razão social, CPF/CNPJ e possivelmente texto adicional.

    Returns:
        str: O nome/razão social sem o CPF/CNPJ e sem o texto adicional.
    """
    # Procura por um padrão de CPF (XXX.XXX.XXX-XX)
    cpf_pattern = r"\d{3}\.\d{3}\.\d{3}-\d{2}"
    # Procura por um padrão de CNPJ (XX.XXX.XXX/YYYY-ZZ)
    cnpj_pattern = r"\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}"

    # Remove o CPF
    nome_sem_cpf_cnpj = re.sub(cpf_pattern, "", nome_ou_razao_social_e_id)
    # Remove o CNPJ
    nome_sem_cpf_cnpj = re.sub(cnpj_pattern, "", nome_sem_cpf_cnpj)

    # Expressão regular para capturar apenas o nome/razão social (letras maiúsculas, minúsculas, acentos, espaços e alguns caracteres especiais comuns em nomes de empresas)
    nome_pattern = r"^([A-Za-zÀ-ú\s\.\-,&]+)(?=[^A-Za-zÀ-ú\s\.\-,&]|$)"
    match = re.search(nome_pattern, nome_sem_cpf_cnpj)

    if match:
        nome_limpo = match.group(1).strip()
    else:
        nome_limpo = nome_sem_cpf_cnpj.strip()

    # Limpeza final
    nome_limpo = re.sub(r'[\/*?:"<>|\n]', "", nome_limpo)
    nome_limpo = re.sub(r'\s+', ' ', nome_limpo)
    nome_limpo = nome_limpo.strip()

    return nome_limpo


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
chamarScript() # Comentei essa linha para evitar a execução de outro script agora