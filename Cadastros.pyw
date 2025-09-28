import os
import shutil
import requests
import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk

# ---------------- Configurações de atualização ----------------
URL_VERSAO = "https://drive.google.com/uc?export=download&id=1Y_AlFKJKHE6F6_HctUUqG8vwm7HLHjhF"      # Link direto para versão
URL_CADASTRO = "https://drive.google.com/uc?export=download&id=1rJf-anrtHpJ938zJ5oeKF2jDg9w6_CMz"   # Link direto para arquivo atualizado
VERSAO_LOCAL = "versao.txt"
CADASTRO_LOCAL = "Cadastros.pyw"

# ---------------- Funções de atualização ----------------
def baixar_arquivo(url, destino):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(destino, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        return True
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao baixar arquivo: {e}")
        return False

def verificar_atualizacao():
    messagebox.showinfo("Atualização", "Buscando atualização...")
    temp_versao = "versao_temp.txt"
    if not baixar_arquivo(URL_VERSAO, temp_versao):
        return False

    # Lê versão do servidor
    with open(temp_versao, 'r') as f:
        versao_servidor = f.read().strip()
    os.remove(temp_versao)

    # Lê versão local
    if os.path.exists(VERSAO_LOCAL):
        with open(VERSAO_LOCAL, 'r') as f:
            versao_local = f.read().strip()
    else:
        versao_local = ""

    if versao_servidor != versao_local:
        atualizar = messagebox.askyesno("Atualização", f"Nova versão disponível ({versao_servidor}). Deseja atualizar?")
        if atualizar:
            if baixar_arquivo(URL_CADASTRO, CADASTRO_LOCAL):
                with open(VERSAO_LOCAL, 'w') as f:
                    f.write(versao_servidor)
                messagebox.showinfo("Atualização", "Atualização concluída com sucesso!")
            else:
                messagebox.showerror("Atualização", "Falha ao baixar atualização!")
            return True
        else:
            return True
    else:
        messagebox.showinfo("Atualização", "Nenhuma atualização encontrada.")
        return True

# ---------------- Funções de produtos ----------------
produtos = []

def salvar_produtos():
    # Salva produtos em JSON
    import json
    with open("produtos.json", "w") as f:
        json.dump(produtos, f, indent=4)

def carregar_produtos():
    import json
    if os.path.exists("produtos.json"):
        with open("produtos.json", "r") as f:
            return json.load(f)
    return []

def pesquisar_produto():
    for item in tree.get_children():
        tree.delete(item)

    filtro_ncm = entry_ncm.get().strip()
    filtro_desc = entry_desc.get().strip().upper()
    filtro_pis = combo_pis.get().strip()
    filtro_icms = combo_icms.get().strip()

    for i, p in enumerate(produtos):
        if ((not filtro_ncm or filtro_ncm in p.get("ncm", "")) and
            (not filtro_desc or filtro_desc in p.get("descricao", "").upper()) and
            (not filtro_pis or filtro_pis == p.get("pis_cofins", "")) and
            (not filtro_icms or filtro_icms == p.get("icms", ""))):
            tree.insert("", "end", iid=i, values=(
                p.get("ncm",""),
                p.get("descricao",""),
                p.get("pis_cofins",""),
                p.get("icms",""),
                p.get("natureza_receita","")
            ))

def limpar_filtros():
    entry_ncm.delete(0, tk.END)
    entry_desc.delete(0, tk.END)
    combo_pis.set("")
    combo_icms.set("")
    pesquisar_produto()

def abrir_formulario(produto=None, indice=None):
    janela = tk.Toplevel(root)
    janela.title("Cadastro de Produto")
    janela.geometry("400x300")

    tk.Label(janela, text="NCM:").pack()
    ncm_entry = tk.Entry(janela)
    ncm_entry.pack()
    tk.Label(janela, text="Descrição:").pack()
    desc_entry = tk.Entry(janela)
    desc_entry.pack()
    tk.Label(janela, text="PIS/COFINS:").pack()
    pis_combo = ttk.Combobox(janela, values=["NORMAL","MONOFASICO"], state="readonly")
    pis_combo.pack()
    tk.Label(janela, text="ICMS:").pack()
    icms_combo = ttk.Combobox(janela, values=["NORMAL","ST"], state="readonly")
    icms_combo.pack()
    tk.Label(janela, text="Natureza Receita (se MONOFASICO):").pack()
    natureza_entry = tk.Entry(janela)
    natureza_entry.pack()

    if produto:
        ncm_entry.insert(0, produto.get("ncm",""))
        desc_entry.insert(0, produto.get("descricao",""))
        pis_combo.set(produto.get("pis_cofins","NORMAL"))
        icms_combo.set(produto.get("icms","NORMAL"))
        natureza_entry.insert(0, produto.get("natureza_receita",""))
    else:
        pis_combo.set("NORMAL")
        icms_combo.set("NORMAL")

    def salvar():
        ncm = ncm_entry.get().strip()
        desc = desc_entry.get().strip().upper()
        pis = pis_combo.get().strip()
        icms = icms_combo.get().strip()
        natureza = natureza_entry.get().strip().upper() if pis == "MONOFASICO" else ""

        if not ncm or not desc:
            messagebox.showwarning("Atenção", "Preencha NCM e Descrição!")
            return

        if produto:  # edição
            for i, p in enumerate(produtos):
                if i != indice and p.get("descricao","").upper() == desc:
                    messagebox.showerror("Erro", "Já existe um produto com essa descrição!")
                    return
            produto["ncm"] = ncm
            produto["descricao"] = desc
            produto["pis_cofins"] = pis
            produto["icms"] = icms
            produto["natureza_receita"] = natureza
            produtos[indice] = produto
            messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!")
        else:  # novo cadastro
            for p in produtos:
                if p.get("descricao","").upper() == desc:
                    messagebox.showerror("Erro", "Já existe um produto com essa descrição!")
                    return
            produtos.append({
                "ncm": ncm,
                "descricao": desc,
                "pis_cofins": pis,
                "icms": icms,
                "natureza_receita": natureza
            })
            messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")

        salvar_produtos()
        janela.destroy()
        pesquisar_produto()

    tk.Button(janela, text="Salvar", command=salvar).pack(pady=10)
    janela.bind("<Return>", lambda event: salvar())

def abrir_cadastro():
    abrir_formulario()

def abrir_edicao():
    item = tree.selection()
    if not item:
        messagebox.showwarning("Atenção", "Selecione um produto para editar.")
        return
    indice = int(item[0])
    produto = produtos[indice]
    abrir_formulario(produto, indice)

def excluir_produto():
    item = tree.selection()
    if not item:
        messagebox.showwarning("Atenção", "Selecione um produto para excluir.")
        return
    indice = int(item[0])
    produtos.pop(indice)
    salvar_produtos()
    pesquisar_produto()

def copiar_ncm(event):
    item = tree.selection()
    if item:
        indice = int(item[0])
        ncm_valor = produtos[indice].get("ncm","")
        root.clipboard_clear()
        root.clipboard_append(ncm_valor)
        messagebox.showinfo("Copiado", f"NCM '{ncm_valor}' copiado para a área de transferência!")

# ---------------- Interface ----------------
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Sistema de Pesquisa de Produtos")
root.geometry("950x500")

frame_pesquisa = ctk.CTkFrame(root)
frame_pesquisa.pack(pady=10, fill="x", padx=10)

tk.Label(frame_pesquisa, text="NCM:").grid(row=0, column=0, padx=5, pady=5)
entry_ncm = tk.Entry(frame_pesquisa, width=15)
entry_ncm.grid(row=0, column=1, padx=5, pady=5)
tk.Label(frame_pesquisa, text="Descrição:").grid(row=0, column=2, padx=5, pady=5)
entry_desc = tk.Entry(frame_pesquisa, width=30)
entry_desc.grid(row=0, column=3, padx=5, pady=5)
tk.Label(frame_pesquisa, text="PIS/COFINS:").grid(row=0, column=4, padx=5, pady=5)
combo_pis = ttk.Combobox(frame_pesquisa, values=["", "NORMAL", "MONOFASICO"], state="readonly", width=15)
combo_pis.grid(row=0, column=5, padx=5, pady=5)
combo_pis.set("")
tk.Label(frame_pesquisa, text="ICMS:").grid(row=0, column=6, padx=5, pady=5)
combo_icms = ttk.Combobox(frame_pesquisa, values=["", "NORMAL", "ST"], state="readonly", width=15)
combo_icms.grid(row=0, column=7, padx=5, pady=5)
combo_icms.set("")
tk.Button(frame_pesquisa, text="Buscar", command=pesquisar_produto).grid(row=0, column=8, padx=5)
tk.Button(frame_pesquisa, text="Limpar filtros", command=limpar_filtros).grid(row=0, column=9, padx=5)

def acionar_enter(event):
    pesquisar_produto()

entry_ncm.bind("<Return>", acionar_enter)
entry_desc.bind("<Return>", acionar_enter)
combo_pis.bind("<Return>", acionar_enter)
combo_icms.bind("<Return>", acionar_enter)

tree = ttk.Treeview(root, columns=("NCM", "Descrição", "PIS/COFINS", "ICMS", "Natureza Receita"), show="headings")
tree.heading("NCM", text="NCM")
tree.heading("Descrição", text="Descrição")
tree.heading("PIS/COFINS", text="PIS/COFINS")
tree.heading("ICMS", text="ICMS")
tree.heading("Natureza Receita", text="Natureza Receita")
tree.pack(pady=10, fill="both", expand=True)
tree.bind("<Double-1>", copiar_ncm)

frame_botoes = ctk.CTkFrame(root)
frame_botoes.pack(pady=5)
ctk.CTkButton(frame_botoes, text="Cadastrar Novo Produto", command=abrir_cadastro).grid(row=0, column=0, padx=5)
ctk.CTkButton(frame_botoes, text="Editar", command=abrir_edicao).grid(row=0, column=1, padx=5)
ctk.CTkButton(frame_botoes, text="Excluir", command=excluir_produto).grid(row=0, column=2, padx=5)

root.bind("<F2>", lambda event: abrir_cadastro())
root.bind("<F3>", lambda event: abrir_edicao())
root.bind("<F5>", lambda event: limpar_filtros())

# ---------------- Inicialização ----------------
produtos = carregar_produtos()
verificar_atualizacao()
pesquisar_produto()
root.mainloop()
