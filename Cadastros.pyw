import os
import json
import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
import requests

# ---------------- Configurações de atualização ----------------
URL_VERSAO = "https://raw.githubusercontent.com/darkphanton0/Cadastros/main/versão.txt"
URL_CADASTRO = "https://raw.githubusercontent.com/darkphanton0/Cadastros/main/Cadastros.pyw"
VERSAO_LOCAL = "versão.txt"
CADASTRO_LOCAL = "Cadastros.pyw"

# ---------------- Função de verificação de atualização ----------------
def verificar_atualizacao():
    root = tk.Tk()
    root.withdraw()  # Esconde a janela principal

    try:
        print("Buscando atualização...")
        resp = requests.get(URL_VERSAO)
        resp.raise_for_status()
        versao_remota = resp.text.strip()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao buscar versão: {e}")
        return

    if os.path.exists(VERSAO_LOCAL):
        with open(VERSAO_LOCAL, 'r', encoding="utf-8") as f:
            versao_local = f.read().strip()
    else:
        versao_local = ""

    if versao_remota != versao_local:
        if messagebox.askyesno("Atualização", f"Nova versão disponível ({versao_remota}). Deseja atualizar?"):
            try:
                r = requests.get(URL_CADASTRO)
                r.raise_for_status()
                with open(CADASTRO_LOCAL, 'wb') as f:
                    f.write(r.content)
                with open(VERSAO_LOCAL, 'w', encoding="utf-8") as f:
                    f.write(versao_remota)
                messagebox.showinfo("Atualização", "Atualização concluída com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao atualizar: {e}")
        else:
            messagebox.showinfo("Atualização", "Atualização cancelada pelo usuário.")
    else:
        print("Nenhuma atualização encontrada.")
        messagebox.showinfo("Atualização", "Nenhuma atualização encontrada.")

# ---------------- Funções de CRUD ----------------
PRODUTOS_JSON = "produtos.json"

def carregar_produtos():
    if os.path.exists(PRODUTOS_JSON):
        with open(PRODUTOS_JSON, 'r', encoding="utf-8") as f:
            return json.load(f)
    return []

def salvar_produtos():
    with open(PRODUTOS_JSON, 'w', encoding="utf-8") as f:
        json.dump(produtos, f, ensure_ascii=False, indent=4)

def pesquisar_produto():
    for item in tree.get_children():
        tree.delete(item)

    ncm = entry_ncm.get().strip()
    desc = entry_desc.get().strip().upper()
    pis = combo_pis.get().strip()
    icms = combo_icms.get().strip()

    for i, p in enumerate(produtos):
        if (not ncm or ncm in p.get("ncm","")) and \
           (not desc or desc in p.get("descricao","").upper()) and \
           (not pis or pis == p.get("pis_cofins","")) and \
           (not icms or icms == p.get("icms","")):
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

# ---------------- Formulário de cadastro/edição ----------------
def abrir_formulario(produto=None, indice=None):
    janela = ctk.CTkToplevel()
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
    tk.Label(janela, text="Natureza da Receita:").pack()
    natureza_entry = tk.Entry(janela)
    natureza_entry.pack()

    if produto:
        ncm_entry.insert(0, produto.get("ncm",""))
        desc_entry.insert(0, produto.get("descricao",""))
        pis_combo.set(produto.get("pis_cofins",""))
        icms_combo.set(produto.get("icms",""))
        natureza_entry.insert(0, produto.get("natureza_receita",""))

    else:
        pis_combo.set("NORMAL")
        icms_combo.set("NORMAL")

    def salvar():
        ncm = ncm_entry.get().strip()
        desc = desc_entry.get().strip().upper()
        pis = pis_combo.get().strip()
        icms = icms_combo.get().strip()
        natureza = natureza_entry.get().strip().upper() if pis=="MONOFASICO" else ""

        if not ncm or not desc:
            messagebox.showwarning("Atenção","Preencha NCM e Descrição!")
            return

        if produto:
            for i,p in enumerate(produtos):
                if i!=indice and p.get("descricao","").upper()==desc:
                    messagebox.showerror("Erro","Já existe um produto com essa descrição!")
                    return
            produto.update({"ncm":ncm,"descricao":desc,"pis_cofins":pis,"icms":icms,"natureza_receita":natureza})
            produtos[indice]=produto
            messagebox.showinfo("Sucesso","Produto atualizado com sucesso!")
        else:
            for p in produtos:
                if p.get("descricao","").upper()==desc:
                    messagebox.showerror("Erro","Já existe um produto com essa descrição!")
                    return
            produtos.append({"ncm":ncm,"descricao":desc,"pis_cofins":pis,"icms":icms,"natureza_receita":natureza})
            messagebox.showinfo("Sucesso","Produto cadastrado com sucesso!")

        salvar_produtos()
        janela.destroy()
        pesquisar_produto()

    tk.Button(janela, text="Salvar", command=salvar).pack(pady=10)
    janela.bind("<Return>", lambda event: salvar())

# ---------------- Ações ----------------
def abrir_cadastro():
    abrir_formulario()

def abrir_edicao():
    item = tree.selection()
    if not item:
        messagebox.showwarning("Atenção","Selecione um produto para editar.")
        return
    indice=int(item[0])
    produto=produtos[indice]
    abrir_formulario(produto,indice)

def excluir_produto():
    item = tree.selection()
    if not item:
        messagebox.showwarning("Atenção","Selecione um produto para excluir.")
        return
    indice=int(item[0])
    produtos.pop(indice)
    salvar_produtos()
    pesquisar_produto()

def copiar_ncm(event):
    item = tree.selection()
    if item:
        indice=int(item[0])
        ncm_valor=produtos[indice].get("ncm","")
        root.clipboard_clear()
        root.clipboard_append(ncm_valor)
        messagebox.showinfo("Copiado", f"NCM '{ncm_valor}' copiado para a área de transferência!")

# ---------------- Interface ----------------
verificar_atualizacao()  # chama atualização antes de iniciar

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

root=ctk.CTk()
root.title("Sistema de Pesquisa de Produtos")
root.geometry("950x500")

frame_pesquisa = ctk.CTkFrame(root)
frame_pesquisa.pack(pady=10, fill="x", padx=10)

tk.Label(frame_pesquisa,text="NCM:").grid(row=0,column=0,padx=5,pady=5)
entry_ncm=tk.Entry(frame_pesquisa,width=15)
entry_ncm.grid(row=0,column=1,padx=5,pady=5)
tk.Label(frame_pesquisa,text="Descrição:").grid(row=0,column=2,padx=5,pady=5)
entry_desc=tk.Entry(frame_pesquisa,width=30)
entry_desc.grid(row=0,column=3,padx=5,pady=5)
tk.Label(frame_pesquisa,text="PIS/COFINS:").grid(row=0,column=4,padx=5,pady=5)
combo_pis=ttk.Combobox(frame_pesquisa,values=["","NORMAL","MONOFASICO"],state="readonly",width=15)
combo_pis.grid(row=0,column=5,padx=5,pady=5)
combo_pis.set("")
tk.Label(frame_pesquisa,text="ICMS:").grid(row=0,column=6,padx=5,pady=5)
combo_icms=ttk.Combobox(frame_pesquisa,values=["","NORMAL","ST"],state="readonly",width=15)
combo_icms.grid(row=0,column=7,padx=5,pady=5)
combo_icms.set("")
tk.Button(frame_pesquisa,text="Buscar",command=pesquisar_produto).grid(row=0,column=8,padx=5)
tk.Button(frame_pesquisa,text="Limpar filtros",command=limpar_filtros).grid(row=0,column=9,padx=5)

def acionar_enter(event):
    pesquisar_produto()

entry_ncm.bind("<Return>",acionar_enter)
entry_desc.bind("<Return>",acionar_enter)
combo_pis.bind("<Return>",acionar_enter)
combo_icms.bind("<Return>",acionar_enter)

tree=ttk.Treeview(root,columns=("NCM","Descrição","PIS/COFINS","ICMS","Natureza Receita"),show="headings")
tree.heading("NCM",text="NCM")
tree.heading("Descrição",text="Descrição")
tree.heading("PIS/COFINS",text="PIS/COFINS")
tree.heading("ICMS",text="ICMS")
tree.heading("Natureza Receita",text="Natureza Receita")
tree.pack(pady=10,fill="both",expand=True)
tree.bind("<Double-1>",copiar_ncm)

frame_botoes=ctk.CTkFrame(root)
frame_botoes.pack(pady=5)
ctk.CTkButton(frame_botoes,text="Cadastrar Novo Produto",command=abrir_cadastro).grid(row=0,column=0,padx=5)
ctk.CTkButton(frame_botoes,text="Editar",command=abrir_edicao).grid(row=0,column=1,padx=5)
ctk.CTkButton(frame_botoes,text="Excluir",command=excluir_produto).grid(row=0,column=2,padx=5)

root.bind("<F2>", lambda event: abrir_cadastro())
root.bind("<F3>", lambda event: abrir_edicao())
root.bind("<F5>", lambda event: limpar_filtros())

produtos = carregar_produtos()
pesquisar_produto()

root.mainloop()
