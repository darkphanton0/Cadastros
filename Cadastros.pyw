import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
import json
import os
import sys
import base64
import tempfile

# ---------------- Ícone embutido ----------------
icone_base64 = """
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
"""  # aqui você coloca a string base64 completa do seu icone.ico

# Cria arquivo temporário do ícone
tmp_icone = tempfile.NamedTemporaryFile(delete=False, suffix=".ico")
tmp_icone.write(base64.b64decode(icone_base64))
tmp_icone.close()

# ---------------- Caminho do JSON ----------------
def resource_path(filename):
    """Retorna caminho absoluto, mesmo no .exe"""
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, filename)

ARQUIVO = resource_path("produtos.json")

# ---------------- Funções de produtos ----------------
def carregar_produtos():
    if os.path.exists(ARQUIVO):
        try:
            with open(ARQUIVO, "r", encoding="utf-8") as f:
                data = f.read().strip()
                if not data:
                    return []
                produtos_carregados = json.loads(data)
                for p in produtos_carregados:
                    if "pis_cofins" not in p:
                        p["pis_cofins"] = "NORMAL"
                    if "icms" not in p:
                        p["icms"] = "NORMAL"
                    if "natureza_receita" not in p:
                        p["natureza_receita"] = ""
                return produtos_carregados
        except json.JSONDecodeError:
            return []
    return []

def salvar_produtos():
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(produtos, f, indent=4, ensure_ascii=False)

# ---------------- Funções de pesquisa ----------------
def pesquisar_produto():
    termo_ncm = entry_ncm.get().strip().lower()
    termo_desc = entry_desc.get().strip().lower()
    termo_pis = combo_pis.get().strip().lower()
    termo_icms = combo_icms.get().strip().lower()

    for item in tree.get_children():
        tree.delete(item)

    for i, produto in enumerate(produtos):
        ncm = produto.get("ncm", "").strip().lower()
        desc = produto.get("descricao", "").strip().lower()
        pis = produto.get("pis_cofins", "NORMAL").strip().lower()
        icms = produto.get("icms", "NORMAL").strip().lower()

        match = True
        if termo_ncm and termo_ncm not in ncm:
            match = False
        if termo_desc and termo_desc not in desc:
            match = False
        if termo_pis and termo_pis != pis:
            match = False
        if termo_icms and termo_icms != icms:
            match = False

        if match:
            tree.insert("", "end", iid=i, values=(
                produto.get("ncm",""),
                produto.get("descricao",""),
                produto.get("pis_cofins",""),
                produto.get("icms",""),
                produto.get("natureza_receita","")
            ))

def limpar_filtros():
    entry_ncm.delete(0, tk.END)
    entry_desc.delete(0, tk.END)
    combo_pis.set("")
    combo_icms.set("")
    pesquisar_produto()

# ---------------- Janela de cadastro/edição ----------------
def abrir_formulario(produto=None, indice=None):
    janela = tk.Toplevel(root)
    janela.title("Cadastro de Produto" if produto is None else "Editar Produto")
    janela.geometry("400x450")
    janela.iconbitmap(tmp_icone.name)  # ícone embutido

    # NCM
    tk.Label(janela, text="NCM:").pack(pady=5)
    ncm_entry = tk.Entry(janela)
    ncm_entry.pack(pady=5)

    # Descrição
    tk.Label(janela, text="Descrição:").pack(pady=5)
    desc_entry = tk.Entry(janela, width=40)
    desc_entry.pack(pady=5)

    # PIS/COFINS
    tk.Label(janela, text="PIS/COFINS:").pack(pady=5)
    pis_options = ["NORMAL", "MONOFASICO"]
    pis_combo = ttk.Combobox(janela, values=pis_options, state="readonly")
    pis_combo.pack(pady=5)

    # Natureza da Receita (aparece só se MONOFASICO)
    natureza_label = tk.Label(janela, text="Natureza da Receita:")
    natureza_entry = tk.Entry(janela, width=40)

    def mostrar_natureza(event=None):
        if pis_combo.get() == "MONOFASICO":
            natureza_label.pack(pady=5)
            natureza_entry.pack(pady=5)
        else:
            natureza_label.pack_forget()
            natureza_entry.pack_forget()

    pis_combo.bind("<<ComboboxSelected>>", mostrar_natureza)

    # ICMS
    tk.Label(janela, text="ICMS:").pack(pady=5)
    icms_options = ["NORMAL", "ST"]
    icms_combo = ttk.Combobox(janela, values=icms_options, state="readonly")
    icms_combo.pack(pady=5)

    # Preenche campos caso seja edição
    if produto:
        ncm_entry.insert(0, produto.get("ncm",""))
        desc_entry.insert(0, produto.get("descricao",""))
        pis_combo.set(produto.get("pis_cofins","NORMAL"))
        icms_combo.set(produto.get("icms","NORMAL"))
        if produto.get("pis_cofins") == "MONOFASICO":
            mostrar_natureza()
            natureza_entry.insert(0, produto.get("natureza_receita",""))
    else:
        pis_combo.set("NORMAL")
        icms_combo.set("NORMAL")

    # Função salvar
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

# ---------------- Funções de ação ----------------
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

# ---------------- Função copiar NCM ----------------
def copiar_ncm(event):
    item = tree.selection()
    if item:
        indice = int(item[0])
        ncm_valor = produtos[indice].get("ncm","")
        root.clipboard_clear()
        root.clipboard_append(ncm_valor)
        messagebox.showinfo("Copiado", f"NCM '{ncm_valor}' copiado para a área de transferência!")

# ---------------- Interface principal ----------------
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Sistema de Pesquisa de Produtos")
root.geometry("950x500")
root.iconbitmap(tmp_icone.name)  # ícone embutido

# Campos de pesquisa
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

# Enter para pesquisar
def acionar_enter(event):
    pesquisar_produto()

entry_ncm.bind("<Return>", acionar_enter)
entry_desc.bind("<Return>", acionar_enter)
combo_pis.bind("<Return>", acionar_enter)
combo_icms.bind("<Return>", acionar_enter)

# Lista de resultados
tree = ttk.Treeview(root, columns=("NCM", "Descrição", "PIS/COFINS", "ICMS", "Natureza Receita"), show="headings")
tree.heading("NCM", text="NCM")
tree.heading("Descrição", text="Descrição")
tree.heading("PIS/COFINS", text="PIS/COFINS")
tree.heading("ICMS", text="ICMS")
tree.heading("Natureza Receita", text="Natureza Receita")
tree.pack(pady=10, fill="both", expand=True)
tree.bind("<Double-1>", copiar_ncm)

# Botões de ação
frame_botoes = ctk.CTkFrame(root)
frame_botoes.pack(pady=5)
ctk.CTkButton(frame_botoes, text="Cadastrar Novo Produto ", command=abrir_cadastro).grid(row=0, column=0, padx=5)
ctk.CTkButton(frame_botoes, text="Editar ", command=abrir_edicao).grid(row=0, column=1, padx=5)
ctk.CTkButton(frame_botoes, text="Excluir", command=excluir_produto).grid(row=0, column=2, padx=5)

# Atalhos
root.bind("<F2>", lambda event: abrir_cadastro())
root.bind("<F3>", lambda event: abrir_edicao())
root.bind("<F5>", lambda event: limpar_filtros())

# Carregar produtos
produtos = carregar_produtos()
pesquisar_produto()

root.mainloop()




