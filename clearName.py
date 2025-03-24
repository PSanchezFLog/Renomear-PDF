import os
import re

def limpar_nome_arquivo(nome_arquivo, texto_padrao_apos_nome=["Natureza do Rendimento", "Rendimentos do trabalho assalariado", "Rendimentos Tributáveis"]):
    """
    Remove o texto adicional que vem depois do nome no nome do arquivo, procurando por um texto padrão.

    Args:
        nome_arquivo (str): O nome do arquivo a ser limpo (incluindo a extensão .pdf).
        texto_padrao_apos_nome (list): Uma lista de textos padrões que podem vir após o nome.

    Returns:
        str: O nome do arquivo limpo.
    """
    nome_limpo = nome_arquivo
    for texto_padrao in texto_padrao_apos_nome:
        # Encontra a posição do texto padrão no nome do arquivo
        posicao = nome_limpo.find(texto_padrao)
        if posicao != -1:
            # Remove o texto padrão e tudo que vem depois dele
            nome_limpo = nome_limpo[:posicao]
            break  # Sai do loop após encontrar e remover o primeiro padrão

    # Limpeza final
    nome_limpo = re.sub(r'[\/*?:"<>|\n]', "", nome_limpo)
    nome_limpo = re.sub(r'\s+', ' ', nome_limpo)
    nome_limpo = nome_limpo.strip()

    return nome_limpo


def limpar_nomes_no_diretorio(diretorio):
    """
    Limpa os nomes de todos os arquivos em um diretório.

    Args:
        diretorio (str): O diretório onde os arquivos estão localizados.
    """
    for filename in os.listdir(diretorio):
        if filename.lower().endswith(".pdf"):  # Apenas para arquivos PDF
            filepath = os.path.join(diretorio, filename)
            novo_nome = limpar_nome_arquivo(filename) #Passando o nome completo do arquivo

            if not novo_nome:
                print(f"Erro: Nome extraído do arquivo '{filename}' está vazio após a limpeza.")
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
                os.rename(filepath, novo_nome_completo)
                print(f"Arquivo '{filename}' renomeado para '{novo_nome}.pdf'")
            except Exception as e:
                print(f"Erro ao renomear '{filename}': {e}")


# Exemplo de uso:

diretorio_arquivos = r"C:\Users\pedro.sanchez\Projetos\RenomearPDF\pdf"  # Substitua pelo seu diretório
limpar_nomes_no_diretorio(diretorio_arquivos)