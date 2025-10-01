import requests
import os
import subprocess
import sys
import tkinter as tk
from tkinter import messagebox

# ---------------- Configurações ----------------
GITHUB_API_URL = "https://api.github.com/repos/darkphanton0/Cadastros/releases/latest"
VERSAO_LOCAL = "versao.txt"
CADASTRO_LOCAL = "Cadastros.pyw"
PRODUTOS_LOCAL = "produtos.json"

# ---------------- Funções ----------------
def obter_versao_local():
    if os.path.exists(VERSAO_LOCAL):
        with open(VERSAO_LOCAL, "r", encoding="utf-8") as f:
            return f.read().strip()
    return "0.0"

def salvar_versao_local(versao):
    with open(VERSAO_LOCAL, "w", encoding="utf-8") as f:
        f.write(versao)

def verificar_e_atualizar():
    try:
        # Obter info da última release
        response = requests.get(GITHUB_API_URL, timeout=10)
        response.raise_for_status()
        release_data = response.json()

        versao_remota = release_data["tag_name"].lstrip("v")  # Ex: "v1.2" -> "1.2"
        versao_local = obter_versao_local()

        if versao_remota != versao_local:
            root = tk.Tk()
            root.withdraw()
            if messagebox.askyesno("Atualização encontrada",
                                   f"Nova versão {versao_remota} disponível.\nDeseja atualizar agora?"):
                for asset in release_data["assets"]:
                    nome_arquivo = asset["name"]
                    url_download = asset["browser_download_url"]

                    print(f"Baixando {nome_arquivo}...")
                    r = requests.get(url_download, stream=True)
                    r.raise_for_status()
                    with open(nome_arquivo, "wb") as f:
                        for chunk in r.iter_content(1024):
                            f.write(chunk)
                    print(f"{nome_arquivo} atualizado com sucesso!")

                salvar_versao_local(versao_remota)
                messagebox.showinfo("Atualização concluída",
                                    f"O sistema foi atualizado para a versão {versao_remota}.")
            root.destroy()
        else:
            print("Nenhuma atualização encontrada.")

    except Exception as e:
        print("Erro ao verificar atualização:", e)

def iniciar_cadastro():
    if os.path.exists(CADASTRO_LOCAL):
        subprocess.Popen([sys.executable, CADASTRO_LOCAL])
    else:
        messagebox.showerror("Erro", f"Arquivo {CADASTRO_LOCAL} não encontrado!")

# ---------------- Programa principal ----------------
if __name__ == "__main__":
    verificar_e_atualizar()
    iniciar_cadastro()
