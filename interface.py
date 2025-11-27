import os
import csv
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox, simpledialog

# ============================================================
# CONFIG
# ============================================================
ARQ_USUARIOS = "usuarios.csv"
ARQ_ATIVIDADES = "atividades.csv"
THEME = "cyborg"

# ============================================================
# INICIALIZACAO
# ============================================================
def inicializar_arquivos():

    # usuarios.csv
    if not os.path.exists(ARQ_USUARIOS):
        with open(ARQ_USUARIOS, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["cpf","senha","nome","tipo"])
            w.writerow(["11111111111","1234","Joao Silva","aluno"])
            w.writerow(["22222222222","abcd","Prof. Carlos","professor"])
            w.writerow(["33333333333","admin","Administrador","admin"])

    # atividades.csv unificado
    if not os.path.exists(ARQ_ATIVIDADES):
        with open(ARQ_ATIVIDADES, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["id","tipo","cpf_aluno","disciplina","descricao","status","nota"])


# ============================================================
# UTIL USUARIOS
# ============================================================
def ler_usuarios():
    with open(ARQ_USUARIOS, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def sobrescrever_usuarios(lista):
    with open(ARQ_USUARIOS, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["cpf","senha","nome","tipo"])
        w.writeheader()
        w.writerows(lista)

def salvar_usuario(row):
    with open(ARQ_USUARIOS, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([row["cpf"], row["senha"], row["nome"], row["tipo"]])

def usuario_existe(cpf):
    return any(u["cpf"] == cpf for u in ler_usuarios())

def validar_login(cpf, senha):
    for u in ler_usuarios():
        if u["cpf"] == cpf and u["senha"] == senha:
            return u
    return None


# ============================================================
# UTIL ATIVIDADES
# ============================================================
def ler_atividades():
    with open(ARQ_ATIVIDADES, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def sobrescrever_atividades(lista):
    with open(ARQ_ATIVIDADES, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["id","tipo","cpf_aluno","disciplina","descricao","status","nota"])
        w.writeheader()
        w.writerows(lista)

def gerar_novo_id(ativs):
    try:
        ids = [int(a["id"]) for a in ativs]
        return max(ids) + 1 if ids else 1
    except:
        return 1


# ============================================================
# FRONT-END
# ============================================================
inicializar_arquivos()
app = ttk.Window(themename=THEME)
app.title("Sistema Educacional PIM")
app.geometry("800x520")


# ============================================================
# ADMIN - LISTAR / EDITAR / EXCLUIR
# ============================================================
def ui_listar_usuarios():

    usuarios = ler_usuarios()
    win = ttk.Toplevel(app)
    win.title("Usuarios")
    win.geometry("650x400")

    ttk.Label(win, text="Usuarios Cadastrados", font=("Helvetica", 14, "bold")).pack(pady=10)

    cols = ("cpf","nome","tipo")
    tree = ttk.Treeview(win, columns=cols, show="headings", height=12)
    for c in cols:
        tree.heading(c, text=c.upper())
        tree.column(c, width=180, anchor="center")
    tree.pack(fill=BOTH, expand=YES, padx=10, pady=6)

    for u in usuarios:
        tree.insert("", "end", values=(u["cpf"], u["nome"], u["tipo"]))

    # EXCLUIR USUARIO
    def excluir():
        sel = tree.focus()
        if not sel:
            messagebox.showwarning("Aviso","Selecione um usuario.")
            return

        cpf = tree.item(sel)["values"][0]
        nome = tree.item(sel)["values"][1]

        if not messagebox.askyesno("Confirmar", f"Excluir usuario {nome} ({cpf})?"):
            return

        novos = [u for u in usuarios if u["cpf"] != cpf]
        sobrescrever_usuarios(novos)
        messagebox.showinfo("OK","Usuario excluido.")
        win.destroy()

    # EDITAR
    def editar():
        sel = tree.focus()
        if not sel:
            messagebox.showwarning("Aviso","Selecione um usuario.")
            return

        cpf_sel = tree.item(sel)["values"][0]
        usuarios_all = ler_usuarios()
        usuario = next((x for x in usuarios_all if x["cpf"] == cpf_sel), None)

        ew = ttk.Toplevel(win)
        ew.title("Editar Usuario")
        ew.geometry("420x300")

        ttk.Label(ew, text="Editar Usuario", font=("Helvetica", 14, "bold")).pack(pady=8)

        f = ttk.Frame(ew); f.pack()

        ttk.Label(f, text="CPF:").grid(row=0,column=0)
        ecpf = ttk.Entry(f, width=30); ecpf.grid(row=0,column=1)
        ecpf.insert(0, usuario["cpf"])
        ecpf.config(state="disabled")

        ttk.Label(f, text="Senha:").grid(row=1,column=0)
        esenha = ttk.Entry(f, width=30); esenha.grid(row=1,column=1)
        esenha.insert(0, usuario["senha"])

        ttk.Label(f, text="Nome:").grid(row=2,column=0)
        enome = ttk.Entry(f, width=30); enome.grid(row=2,column=1)
        enome.insert(0, usuario["nome"])

        ttk.Label(f, text="Tipo:").grid(row=3,column=0)
        var = ttk.StringVar(value=usuario["tipo"])
        cb = ttk.Combobox(f, textvariable=var, values=["aluno","professor","admin"], width=28)
        cb.grid(row=3,column=1)

        def salvar_edicao():
            usuario["senha"] = esenha.get().strip()
            usuario["nome"] = enome.get().strip()
            usuario["tipo"] = var.get().strip()
            sobrescrever_usuarios(usuarios_all)
            messagebox.showinfo("OK","Atualizado.")
            ew.destroy()
            win.destroy()

        ttk.Button(ew, text="Salvar", command=salvar_edicao, bootstyle="success").pack(pady=10)
        ttk.Button(ew, text="Cancelar", command=ew.destroy, bootstyle="danger").pack()

    btns = ttk.Frame(win); btns.pack(pady=8)
    ttk.Button(btns, text="Excluir", command=excluir, bootstyle="danger").grid(row=0,column=0,padx=8)
    ttk.Button(btns, text="Editar", command=editar, bootstyle="warning").grid(row=0,column=1,padx=8)
    ttk.Button(btns, text="Fechar", command=win.destroy, bootstyle="secondary").grid(row=0,column=2,padx=8)


# ============================================================
# ADMIN - CADASTRAR
# ============================================================
def ui_cadastrar_usuario():

    win = ttk.Toplevel(app)
    win.title("Cadastrar Usuario")
    win.geometry("420x300")

    ttk.Label(win, text="Cadastrar Usuario", font=("Helvetica", 14, "bold")).pack(pady=10)

    f = ttk.Frame(win); f.pack()
    ttk.Label(f, text="CPF:").grid(row=0,column=0,pady=6)
    e_cpf = ttk.Entry(f, width=32); e_cpf.grid(row=0,column=1)

    ttk.Label(f, text="Senha:").grid(row=1,column=0,pady=6)
    e_senha = ttk.Entry(f, width=32, show="*"); e_senha.grid(row=1,column=1)

    ttk.Label(f, text="Nome:").grid(row=2,column=0,pady=6)
    e_nome = ttk.Entry(f, width=32); e_nome.grid(row=2,column=1)

    ttk.Label(f, text="Tipo:").grid(row=3,column=0,pady=6)
    var = ttk.StringVar(value="aluno")
    cb = ttk.Combobox(f, textvariable=var, values=["aluno","professor","admin"], width=30)
    cb.grid(row=3,column=1)

    def salvar():
        cpf = e_cpf.get().strip()
        senha = e_senha.get().strip()
        nome = e_nome.get().strip()
        tipo = var.get()

        if not (cpf and senha and nome):
            messagebox.showwarning("Aviso","Preencha tudo.")
            return

        if usuario_existe(cpf):
            messagebox.showerror("Erro","CPF ja cadastrado.")
            return

        salvar_usuario({"cpf":cpf,"senha":senha,"nome":nome,"tipo":tipo})
        messagebox.showinfo("OK","Cadastrado.")
        win.destroy()

    ttk.Button(win, text="Salvar", command=salvar, bootstyle="success").pack(pady=10)
    ttk.Button(win, text="Cancelar", command=win.destroy, bootstyle="danger").pack()


# ============================================================
# PROFESSOR - POSTAR ATIVIDADE
# ============================================================
def ui_postar_atividade():

    win = ttk.Toplevel(app)
    win.title("Postar Atividade")
    win.geometry("480x300")

    ttk.Label(win, text="Postar Atividade", font=("Helvetica", 14, "bold")).pack(pady=10)

    f = ttk.Frame(win); f.pack()
    ttk.Label(f, text="Disciplina:").grid(row=0,column=0,pady=6)
    e_disc = ttk.Entry(f, width=36); e_disc.grid(row=0,column=1)

    ttk.Label(f, text="Descricao:").grid(row=1,column=0,pady=6)
    e_desc = ttk.Entry(f, width=36); e_desc.grid(row=1,column=1)

    def salvar():
        disc = e_disc.get().strip()
        desc = e_desc.get().strip()

        if not (disc and desc):
            messagebox.showwarning("Aviso","Preencha tudo.")
            return

        ativs = ler_atividades()
        novo_id = gerar_novo_id(ativs)

        ativs.append({
            "id": str(novo_id),
            "tipo": "publicada",
            "cpf_aluno": "",
            "disciplina": disc,
            "descricao": desc,
            "status": "Publicada",
            "nota": ""
        })

        sobrescrever_atividades(ativs)
        messagebox.showinfo("OK","Atividade publicada.")
        win.destroy()

    ttk.Button(win, text="Publicar", command=salvar, bootstyle="success").pack(pady=10)


# ============================================================
# ALUNO - VER ATIVIDADES PUBLICADAS
# ============================================================
def ui_ver_atividades(cpf):

    ativs = ler_atividades()
    publicadas = [a for a in ativs if a["tipo"] == "publicada"]

    win = ttk.Toplevel(app)
    win.title("Atividades Disponiveis")
    win.geometry("760x420")

    ttk.Label(win, text="Atividades Disponiveis", font=("Helvetica", 14, "bold")).pack(pady=10)

    cols = ("id","disciplina","descricao","status")
    tree = ttk.Treeview(win, columns=cols, show="headings")
    for c in cols:
        tree.heading(c, text=c.upper())
        tree.column(c, width=160, anchor="center")
    tree.pack(fill=BOTH, expand=YES, padx=10, pady=10)

    for a in publicadas:
        tree.insert("", "end", values=(a["id"], a["disciplina"], a["descricao"], a["status"]))

    def enviar():
        sel = tree.focus()
        if not sel:
            messagebox.showwarning("Aviso","Selecione uma atividade.")
            return

        vals = tree.item(sel)["values"]
        atividade_id = vals[0]
        disciplina = vals[1]

        resp = simpledialog.askstring("Resposta","Digite sua resposta:")
        if not resp:
            return

        ativs = ler_atividades()

        ativs.append({
            "id": str(atividade_id),
            "tipo": "submissao",
            "cpf_aluno": cpf,
            "disciplina": disciplina,
            "descricao": resp,
            "status": "Pendente",
            "nota": ""
        })

        sobrescrever_atividades(ativs)
        messagebox.showinfo("OK","Submissao enviada.")
        win.destroy()

    ttk.Button(win, text="Enviar Submissao", command=enviar, bootstyle="success").pack(pady=8)


# ============================================================
# ALUNO - MINHAS SUBMISSOES
# ============================================================
def ui_minhas_submissoes(cpf):

    ativs = ler_atividades()
    minhas = [a for a in ativs if a["tipo"] == "submissao" and a["cpf_aluno"] == cpf]

    win = ttk.Toplevel(app)
    win.title("Minhas Submissoes")
    win.geometry("760x420")

    ttk.Label(win, text="Minhas Submissoes", font=("Helvetica", 14, "bold")).pack(pady=10)

    cols = ("id","disc","descricao","status","nota")
    tree = ttk.Treeview(win, columns=cols, show="headings")
    for c in cols:
        tree.heading(c, text=c.upper())
        tree.column(c, width=140, anchor="center")
    tree.pack(fill=BOTH, expand=YES, padx=10, pady=10)

    for a in minhas:
        tree.insert("", "end", values=(a["id"], a["disciplina"], a["descricao"], a["status"], a["nota"]))


# ============================================================
# PROFESSOR - AVALIAR SUBMISSOES
# ============================================================
def ui_avaliar():

    ativs = ler_atividades()
    subs = [a for a in ativs if a["tipo"] == "submissao"]

    win = ttk.Toplevel(app)
    win.title("Avaliar Submissoes")
    win.geometry("760x420")

    ttk.Label(win, text="Avaliar Submissoes", font=("Helvetica", 14, "bold")).pack(pady=10)

    cols = ("cpf","id","disc","descricao","status","nota")
    tree = ttk.Treeview(win, columns=cols, show="headings")
    for c in cols:
        tree.heading(c, text=c.upper())
        tree.column(c, width=120, anchor="center")
    tree.pack(fill=BOTH, expand=YES, padx=10, pady=10)

    for a in subs:
        tree.insert("", "end", values=(a["cpf_aluno"], a["id"], a["disciplina"], a["descricao"], a["status"], a["nota"]))

    def avaliar():
        sel = tree.focus()
        if not sel:
            messagebox.showwarning("Aviso","Selecione.")
            return

        vals = tree.item(sel)["values"]
        cpf = vals[0]
        atividade_id = vals[1]
        descricao = vals[3]

        nota = simpledialog.askstring("Nota","Informe a nota:")
        if not nota:
            return

        for a in ativs:
            if a["tipo"] == "submissao" and a["cpf_aluno"] == cpf and a["id"] == str(atividade_id) and a["descricao"] == descricao:
                a["nota"] = nota
                a["status"] = "Avaliada"

        sobrescrever_atividades(ativs)
        messagebox.showinfo("OK","Avaliado.")
        win.destroy()

    ttk.Button(win, text="Avaliar Selecionada", command=avaliar, bootstyle="success").pack(pady=8)


# ============================================================
# MENU APOS LOGIN
# ============================================================
def abrir_menu(usuario):

    win = ttk.Toplevel(app)
    win.title("Menu")
    win.geometry("400x430")

    nome = usuario["nome"]
    tipo = usuario["tipo"]
    cpf = usuario["cpf"]

    ttk.Label(win, text=f"Bem-vindo, {nome}", font=("Helvetica", 16, "bold")).pack(pady=12)

    if tipo == "aluno":
        ttk.Button(win, text="Ver Atividades", command=lambda: ui_ver_atividades(cpf), bootstyle="info").pack(pady=6)
        ttk.Button(win, text="Minhas Submissoes", command=lambda: ui_minhas_submissoes(cpf), bootstyle="success").pack(pady=6)

    elif tipo == "professor":
        ttk.Button(win, text="Postar Atividade", command=ui_postar_atividade, bootstyle="primary").pack(pady=6)
        ttk.Button(win, text="Avaliar Submissoes", command=ui_avaliar, bootstyle="danger").pack(pady=6)

    elif tipo == "admin":
        ttk.Button(win, text="Cadastrar Usuario", command=ui_cadastrar_usuario, bootstyle="success").pack(pady=6)
        ttk.Button(win, text="Listar Usuarios", command=ui_listar_usuarios, bootstyle="info").pack(pady=6)

    ttk.Button(win, text="Sair", command=win.destroy, bootstyle="secondary").pack(pady=16)


# ============================================================
# LOGIN
# ============================================================
def fazer_login():

    cpf = entry_cpf.get().strip()
    senha = entry_senha.get().strip()

    if not cpf or not senha:
        messagebox.showwarning("Aviso","Preencha CPF e senha.")
        return

    user = validar_login(cpf, senha)
    if user is None:
        messagebox.showerror("Erro","CPF ou senha incorretos.")
        return

    abrir_menu(user)


# ============================================================
# TELA PRINCIPAL
# ============================================================
f = ttk.Frame(app, padding=20)
f.pack(expand=YES)

ttk.Label(f, text="SISTEMA EDUCACIONAL PIM", font=("Helvetica", 20, "bold")).pack(pady=10)

frm = ttk.Frame(f); frm.pack(pady=10)

ttk.Label(frm, text="CPF:").grid(row=0,column=0,pady=8)
entry_cpf = ttk.Entry(frm, width=42); entry_cpf.grid(row=0,column=1)

ttk.Label(frm, text="Senha:").grid(row=1,column=0,pady=8)
entry_senha = ttk.Entry(frm, width=42, show="*"); entry_senha.grid(row=1,column=1)

ttk.Button(f, text="Entrar", command=fazer_login, bootstyle="primary").pack(pady=10)
ttk.Button(f, text="Sair", command=app.destroy, bootstyle="danger").pack()

app.mainloop()
