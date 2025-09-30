import os
import sys
import requests
from tkinter import messagebox, Tk

# ---------------- Configurações ----------------
ARQUIVOS = {
    "Cadastros.pyw": "https://raw.githubusercontent.com/darkphanton0/Cadastros/main/Cadastros.pyw",
    "produtos.json": "https://raw.githubusercontent.com/darkphanton0/Cadastros/main/produtos.json",
    "readme.txt": "https://raw.githubusercontent.com/darkphanton0/Cadastros/main/readme.txt",
    "requisitos.bat": "https://raw.githubusercontent.com/darkphanton0/Cadastros/main/requisitos.bat",
    "versão.txt": "https://raw.githubusercontent.com/darkphanton0/Cadastros/main/versão.txt"
}
VERSAO_LOCAL = "versão.txt"

# Inicializa Tk para messagebox
root = Tk()
root.withdraw()

# ---------------- Funções ----------------
def baixar_arquivo(url, destino):
    try:
        r = requests.get(url)
        r.raise_for_status()
        with open(destino, "wb") as f:
            f.write(r.content)
        return True
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao baixar {destino}:\n{e}")
        return False

def verificar_e_atualizar():
    # Baixa a versão do servidor
    versao_temp = "versao_servidor.txt"
    if not baixar_arquivo(ARQUIVOS["versão.txt"], versao_temp):
        return
    
    # Lê versões
    versao_nova = open(versao_temp, "r", encoding="utf-8").read().strip()
    versao_atual = open(VERSAO_LOCAL, "r", encoding="utf-8").read().strip() if os.path.exists(VERSAO_LOCAL) else ""
    
    if versao_nova != versao_atual:
        if messagebox.askyesno("Atualização", f"Nova versão detectada ({versao_nova}). Deseja atualizar?"):
            # Baixa todos os arquivos
            for nome, url in ARQUIVOS.items():
                if nome != "versão.txt":  # já lemos a versão separadamente
                    baixar_arquivo(url, nome)
            # Atualiza a versão local
            with open(VERSAO_LOCAL, "w", encoding="utf-8") as f:
                f.write(versao_nova)
            messagebox.showinfo("Atualização", "Atualização concluída!")
    os.remove(versao_temp)

# ---------------- Execução ----------------
if __name__ == "__main__":
    verificar_e_atualizar()
    # Executa o Cadastros.pyw atualizado
    if os.path.exists("Cadastros.pyw"):
        os.system(f'start "" "{os.path.abspath("Cadastros.pyw")}"')
    else:
        messagebox.showerror("Erro", "Arquivo Cadastros.pyw não encontrado!")
