import urllib.request
import os
import json
from tkinter import messagebox, Tk

# ---------------- Configurações ----------------
# Links raw dos arquivos no GitHub
ARQUIVOS = {
    "Cadastros.pyw": "https://raw.githubusercontent.com/darkphanton0/Cadastros/main/Cadastros.pyw",
    "produtos.json": "https://raw.githubusercontent.com/darkphanton0/Cadastros/main/produtos.json",
    "versao.txt": "https://raw.githubusercontent.com/darkphanton0/Cadastros/main/versao.txt",
    "README.txt": "https://raw.githubusercontent.com/darkphanton0/Cadastros/main/README.txt",
    "requisitos.bat": "https://raw.githubusercontent.com/darkphanton0/Cadastros/main/requisitos.bat",
    "execute.pyw": "https://raw.githubusercontent.com/darkphanton0/Cadastros/main/execute.pyw",
}

# Pasta do script
PASTA = os.path.dirname(__file__)
VERSAO_LOCAL = os.path.join(PASTA, "versão.txt")

# ---------------- Funções ----------------
def baixar_arquivo(nome, url):
    """Baixa um arquivo do GitHub e salva na mesma pasta do script."""
    caminho = os.path.join(PASTA, nome)
    try:
        urllib.request.urlretrieve(url, caminho)
        print(f"{nome} atualizado com sucesso!")
    except Exception as e:
        print(f"Erro ao baixar {nome}: {e}")

def ler_versao_local():
    if os.path.exists(VERSAO_LOCAL):
        with open(VERSAO_LOCAL, "r", encoding="utf-8") as f:
            return f.read().strip()
    return ""

def ler_versao_remota():
    try:
        caminho_temp = os.path.join(PASTA, "_temp_versao.txt")
        urllib.request.urlretrieve(ARQUIVOS["versão.txt"], caminho_temp)
        with open(caminho_temp, "r", encoding="utf-8") as f:
            versao = f.read().strip()
        os.remove(caminho_temp)
        return versao
    except Exception as e:
        print(f"Não foi possível verificar a versão remota: {e}")
        return None

def verificar_e_atualizar():
    versao_local = ler_versao_local()
    versao_remota = ler_versao_remota()

    if versao_remota is None:
        print("Erro ao acessar a versão remota. Atualização cancelada.")
        return

    if versao_remota != versao_local:
        root = Tk()
        root.withdraw()  # Esconde a janela principal do Tkinter
        resposta = messagebox.askyesno(
            "Atualização disponível",
            f"Nova versão disponível: {versao_remota}\nVersão atual: {versao_local}\nDeseja atualizar?"
        )
        root.destroy()

        if resposta:
            print("Atualizando arquivos...")
            for nome, url in ARQUIVOS.items():
                baixar_arquivo(nome, url)
            print("Todos os arquivos foram atualizados!")
        else:
            print("Atualização cancelada pelo usuário.")
    else:
        print("Nenhuma atualização encontrada.")

# ---------------- Execução ----------------
if __name__ == "__main__":
    verificar_e_atualizar()
    print("Sistema pronto para iniciar.")
