# app.py
import os
import csv
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox, simpledialog

# -------------------- CONFIG --------------------
ARQ_USUARIOS = "usuarios.csv"
ARQ_ATIVIDADES = "atividades.csv"   # atividades enviadas por alunos / avaliadas por prof
ARQ_NOTAS = "notas.csv"             # lancamento de np1,np2 (sem media aqui)
THEME = "cyborg"

# -------------------- INICIALIZACAO --------------------
def inicializar_arquivos():
    # usuarios: cpf,senha,nome,tipo
    if not os.path.exists(ARQ_USUARIOS):
        with open(ARQ_USUARIOS, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["cpf","senha","nome","tipo"])
            # exemplos iniciais
            w.writerow(["11111111111","1234","Joao Silva","aluno"])
            w.writerow(["22222222222","abcd","Prof. Carlos","professor"])
            w.writerow(["33333333333","admin","Administrador","admin"])
    # atividades: cpf_aluno,disciplina,descricao,status,nota
    if not os.path.exists(ARQ_ATIVIDADES):
        with open(ARQ_ATIVIDADES, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["cpf_aluno","disciplina","descricao","status","nota"])
    # notas: cpf_aluno,disciplina,nota1,nota2
    if not os.path.exists(ARQ_NOTAS):
        with open(ARQ_NOTAS, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["cpf_aluno","disciplina","nota1","nota2"])

# -------------------- UTILIDADES USUARIOS --------------------
def ler_usuarios():
    with open(ARQ_USUARIOS, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def salvar_usuario(csv_row):
    # csv_row: dict com cpf,senha,nome,tipo
    with open(ARQ_USUARIOS, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([csv_row["cpf"], csv_row["senha"], csv_row["nome"], csv_row["tipo"]])

def sobrescrever_usuarios(lista_dicts):
    with open(ARQ_USUARIOS, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["cpf","senha","nome","tipo"])
        writer.writeheader()
        writer.writerows(lista_dicts)

def usuario_existe(cpf):
    return any(u["cpf"] == cpf for u in ler_usuarios())

def validar_login(cpf, senha):
    for u in ler_usuarios():
        if u["cpf"] == cpf and u["senha"] == senha:
            return u
    return None

# -------------------- UTILIDADES ATIVIDADES / NOTAS --------------------
def ler_atividades():
    with open(ARQ_ATIVIDADES, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def sobrescrever_atividades(lista):
    with open(ARQ_ATIVIDADES, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["cpf_aluno","disciplina","descricao","status","nota"])
        writer.writeheader()
        writer.writerows(lista)

def ler_notas():
    with open(ARQ_NOTAS, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def salvar_nota_row(row):
    with open(ARQ_NOTAS, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([row["cpf_aluno"], row["disciplina"], row["nota1"], row["nota2"]])

# -------------------- FRONTE-END (ttkbootstrap) --------------------
inicializar_arquivos()
app = ttk.Window(themename=THEME)
app.title("Sistema Educacional PIM")
app.geometry("700x480")

# -------------------- FUNCOES DO ADMIN --------------------
def ui_cadastrar_usuario(parent=None):
    win = ttk.Toplevel(parent or app)
    win.title("Cadastrar Usuario")
    win.geometry("420x320")

    ttk.Label(win, text="Cadastrar Usuario", font=("Helvetica", 14, "bold")).pack(pady=8)

    frm = ttk.Frame(win); frm.pack(pady=6, padx=10, fill=X)
    ttk.Label(frm, text="CPF:").grid(row=0, column=0, sticky=W, pady=4)
    e_cpf = ttk.Entry(frm, width=30); e_cpf.grid(row=0, column=1, pady=4)
    ttk.Label(frm, text="Senha:").grid(row=1, column=0, sticky=W, pady=4)
    e_senha = ttk.Entry(frm, width=30, show="*"); e_senha.grid(row=1, column=1, pady=4)
    ttk.Label(frm, text="Nome:").grid(row=2, column=0, sticky=W, pady=4)
    e_nome = ttk.Entry(frm, width=30); e_nome.grid(row=2, column=1, pady=4)
    ttk.Label(frm, text="Tipo:").grid(row=3, column=0, sticky=W, pady=4)
    tipo_var = ttk.StringVar(value="aluno")
    cb_tipo = ttk.Combobox(frm, textvariable=tipo_var, values=["aluno","professor","admin"], width=28)
    cb_tipo.grid(row=3, column=1, pady=4)

    def salvar():
        cpf = e_cpf.get().strip()
        senha = e_senha.get().strip()
        nome = e_nome.get().strip()
        tipo = tipo_var.get().strip()
        if not (cpf and senha and nome and tipo):
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return
        if usuario_existe(cpf):
            messagebox.showerror("Erro", "CPF ja cadastrado!")
            return
        salvar_usuario({"cpf":cpf,"senha":senha,"nome":nome,"tipo":tipo})
        messagebox.showinfo("Sucesso", "Usuario cadastrado com sucesso!")
        win.destroy()

    ttk.Button(win, text="Salvar", command=salvar, bootstyle="success").pack(pady=10)
    ttk.Button(win, text="Cancelar", command=win.destroy, bootstyle="danger").pack()

def ui_listar_usuarios(parent=None):
    usuarios = ler_usuarios()
    win = ttk.Toplevel(parent or app)
    win.title("Lista de Usuarios")
    win.geometry("620x380")

    ttk.Label(win, text="Usuarios Cadastrados", font=("Helvetica", 14, "bold")).pack(pady=8)
    cols = ("cpf","nome","tipo")
    tree = ttk.Treeview(win, columns=cols, show="headings", height=12)
    for c in cols:
        tree.heading(c, text=c.upper())
        tree.column(c, width=180, anchor="center")
    tree.pack(fill=BOTH, expand=YES, padx=10, pady=6)

    for u in usuarios:
        # ocultar senha por seguranca (nao exibimos)
        tree.insert("", "end", values=(u["cpf"], u["nome"], u["tipo"]))

    def excluir_selecionado():
        sel = tree.focus()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione um usuario para excluir.")
            return
        item = tree.item(sel)["values"]
        cpf = item[0]
        nome = item[1]
        if messagebox.askyesno("Confirmar", f"Excluir usuario {nome} ({cpf})?"):
            novos = [x for x in usuarios if x["cpf"] != cpf]
            sobrescrever_usuarios(novos)
            messagebox.showinfo("Sucesso", "Usuario excluido.")
            win.destroy()

    def editar_selecionado():
        sel = tree.focus()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione um usuario para editar.")
            return
        item = tree.item(sel)["values"]
        cpf_sel = item[0]
        usuarios_all = ler_usuarios()
        usuario = next((x for x in usuarios_all if x["cpf"] == cpf_sel), None)
        if not usuario:
            messagebox.showerror("Erro", "Usuario nao encontrado.")
            return
        # abrir janela de edicao pre-preenchida
        ew = ttk.Toplevel(win)
        ew.title("Editar Usuario")
        ew.geometry("420x300")
        ttk.Label(ew, text="Editar Usuario", font=("Helvetica", 14, "bold")).pack(pady=8)
        f = ttk.Frame(ew); f.pack(padx=10, pady=6)
        ttk.Label(f, text="CPF:").grid(row=0, column=0, sticky=W)
        ecpf = ttk.Entry(f, width=28); ecpf.grid(row=0, column=1); ecpf.insert(0, usuario["cpf"]); ecpf.config(state="disabled")
        ttk.Label(f, text="Senha:").grid(row=1, column=0, sticky=W)
        esenha = ttk.Entry(f, width=28); esenha.grid(row=1, column=1); esenha.insert(0, usuario["senha"])
        ttk.Label(f, text="Nome:").grid(row=2, column=0, sticky=W)
        enome = ttk.Entry(f, width=28); enome.grid(row=2, column=1); enome.insert(0, usuario["nome"])
        ttk.Label(f, text="Tipo:").grid(row=3, column=0, sticky=W)
        tvar = ttk.StringVar(value=usuario["tipo"])
        cbt = ttk.Combobox(f, textvariable=tvar, values=["aluno","professor","admin"], width=26); cbt.grid(row=3, column=1)
        def salvar_edicao():
            usuario["senha"] = esenha.get().strip()
            usuario["nome"] = enome.get().strip()
            usuario["tipo"] = tvar.get().strip()
            sobrescrever_usuarios(usuarios_all)
            messagebox.showinfo("Sucesso", "Usuario atualizado.")
            ew.destroy()
            win.destroy()
        ttk.Button(ew, text="Salvar", command=salvar_edicao, bootstyle="success").pack(pady=8)
        ttk.Button(ew, text="Cancelar", command=ew.destroy, bootstyle="danger").pack()

    btns = ttk.Frame(win); btns.pack(pady=6)
    ttk.Button(btns, text="Excluir Selecionado", command=excluir_selecionado, bootstyle="danger").grid(row=0, column=0, padx=6)
    ttk.Button(btns, text="Editar Selecionado", command=editar_selecionado, bootstyle="warning").grid(row=0, column=1, padx=6)
    ttk.Button(btns, text="Fechar", command=win.destroy, bootstyle="secondary").grid(row=0, column=2, padx=6)

# -------------------- FUNCOES DO ALUNO --------------------
def ui_enviar_atividade(cpf_aluno):
    win = ttk.Toplevel(app)
    win.title("Enviar Atividade")
    win.geometry("440x320")
    ttk.Label(win, text="Enviar Atividade", font=("Helvetica", 14, "bold")).pack(pady=8)
    frm = ttk.Frame(win); frm.pack(padx=10, pady=6)
    ttk.Label(frm, text="Disciplina:").grid(row=0, column=0, sticky=W)
    e_disc = ttk.Entry(frm, width=36); e_disc.grid(row=0, column=1, pady=6)
    ttk.Label(frm, text="Descricao:").grid(row=1, column=0, sticky=W)
    e_desc = ttk.Entry(frm, width=36); e_desc.grid(row=1, column=1, pady=6)
    def enviar():
        disc = e_disc.get().strip(); desc = e_desc.get().strip()
        if not (disc and desc):
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return
        if not messagebox.askyesno("Confirmar", "Confirmar envio da atividade?"):
            return
        with open(ARQ_ATIVIDADES, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([cpf_aluno, disc, desc, "Pendente", ""])
        messagebox.showinfo("Sucesso", "Atividade enviada.")
        win.destroy()
    ttk.Button(win, text="Enviar", command=enviar, bootstyle="success").pack(pady=10)
    ttk.Button(win, text="Cancelar", command=win.destroy, bootstyle="danger").pack()

def ui_ver_notas(cpf_aluno):
    win = ttk.Toplevel(app)
    win.title("Boletim")
    win.geometry("520x360")
    ttk.Label(win, text="Boletim do Aluno", font=("Helvetica", 14, "bold")).pack(pady=8)
    tree = ttk.Treeview(win, columns=("disciplina","nota1","nota2"), show="headings")
    for c in ("disciplina","nota1","nota2"):
        tree.heading(c, text=c.upper())
        tree.column(c, width=150, anchor="center")
    tree.pack(fill=BOTH, expand=YES, padx=10, pady=8)
    notas = ler_notas()
    for n in notas:
        if n["cpf_aluno"] == cpf_aluno:
            tree.insert("", "end", values=(n["disciplina"], n["nota1"], n["nota2"]))
    ttk.Button(win, text="Fechar", command=win.destroy, bootstyle="secondary").pack(pady=8)

# -------------------- FUNCOES DO PROFESSOR --------------------
def ui_postar_atividade():
    win = ttk.Toplevel(app)
    win.title("Postar Atividade (professor)")
    win.geometry("460x320")
    ttk.Label(win, text="Postar Atividade", font=("Helvetica", 14, "bold")).pack(pady=8)
    frm = ttk.Frame(win); frm.pack(padx=10, pady=6)
    ttk.Label(frm, text="Disciplina:").grid(row=0, column=0, sticky=W)
    e_disc = ttk.Entry(frm, width=36); e_disc.grid(row=0, column=1, pady=6)
    ttk.Label(frm, text="Descricao:").grid(row=1, column=0, sticky=W)
    e_desc = ttk.Entry(frm, width=36); e_desc.grid(row=1, column=1, pady=6)
    def salvar():
        disc = e_disc.get().strip(); desc = e_desc.get().strip()
        if not (disc and desc):
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return
        # postamos uma atividade "modelo" para os alunos; em muitos cenarios, professor postaria em outro CSV
        if not messagebox.askyesno("Confirmar", "Confirmar publicacao da atividade?"):
            return
        # aqui apenas notifica (atividade "publicada") - professores normalmente adicionariam em conteudos/atividades globais
        messagebox.showinfo("Sucesso", "Atividade publicada (visivel aos alunos via formulario).")
        win.destroy()
    ttk.Button(win, text="Publicar", command=salvar, bootstyle="success").pack(pady=10)
    ttk.Button(win, text="Cancelar", command=win.destroy, bootstyle="danger").pack()

def ui_listar_atividades_para_avaliacao():
    # mostra atividades em ARQ_ATIVIDADES para o professor selecionar e avaliar
    atividades = ler_atividades()
    win = ttk.Toplevel(app)
    win.title("Avaliar Atividades")
    win.geometry("760x420")
    ttk.Label(win, text="Submissoes de Atividades", font=("Helvetica", 14, "bold")).pack(pady=8)
    cols = ("cpf_aluno","disciplina","descricao","status","nota")
    tree = ttk.Treeview(win, columns=cols, show="headings", height=14)
    for c in cols:
        tree.heading(c, text=c.upper()); tree.column(c, width=140, anchor="center")
    tree.pack(fill=BOTH, expand=YES, padx=10, pady=8)
    for a in atividades:
        tree.insert("", "end", values=(a["cpf_aluno"], a["disciplina"], a["descricao"], a["status"], a["nota"]))
    def avaliar():
        sel = tree.focus()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione uma submissao para avaliar.")
            return
        vals = tree.item(sel)["values"]
        cpf_aluno, disc = vals[0], vals[1]
        nota = simpledialog.askstring("Nota", f"Informe a nota para {cpf_aluno} - {disc}:")
        if nota is None:
            return
        if not messagebox.askyesno("Confirmar", "Confirmar avaliacao e atribuicao da nota?"):
            return
        # atualizar lista e reescrever CSV
        for a in atividades:
            if a["cpf_aluno"] == cpf_aluno and a["disciplina"] == disc and a["descricao"] == vals[2]:
                a["nota"] = nota
                a["status"] = "Avaliada"
        sobrescrever_atividades(atividades)
        messagebox.showinfo("Sucesso", "Atividade avaliada.")
        win.destroy()
    ttk.Button(win, text="Avaliar Selecionada", command=avaliar, bootstyle="success").pack(pady=6)
    ttk.Button(win, text="Fechar", command=win.destroy, bootstyle="secondary").pack(pady=4)

def ui_lancar_notas():
    win = ttk.Toplevel(app)
    win.title("Lancar Notas (professor)")
    win.geometry("460x380")
    ttk.Label(win, text="Lancar Notas (NP1 / NP2)", font=("Helvetica", 14, "bold")).pack(pady=8)
    frm = ttk.Frame(win); frm.pack(padx=10, pady=6)
    ttk.Label(frm, text="CPF do Aluno:").grid(row=0, column=0, sticky=W); e_cpf = ttk.Entry(frm, width=30); e_cpf.grid(row=0, column=1, pady=4)
    ttk.Label(frm, text="Disciplina:").grid(row=1, column=0, sticky=W); e_disc = ttk.Entry(frm, width=30); e_disc.grid(row=1, column=1, pady=4)
    ttk.Label(frm, text="Nota 1:").grid(row=2, column=0, sticky=W); e_n1 = ttk.Entry(frm, width=30); e_n1.grid(row=2, column=1, pady=4)
    ttk.Label(frm, text="Nota 2:").grid(row=3, column=0, sticky=W); e_n2 = ttk.Entry(frm, width=30); e_n2.grid(row=3, column=1, pady=4)
    def salvar():
        cpf = e_cpf.get().strip(); disc = e_disc.get().strip(); n1 = e_n1.get().strip(); n2 = e_n2.get().strip()
        if not (cpf and disc and n1 and n2):
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return
        if not messagebox.askyesno("Confirmar", "Confirmar lancamento das notas?"):
            return
        salvar_nota_row({"cpf_aluno":cpf,"disciplina":disc,"nota1":n1,"nota2":n2})
        messagebox.showinfo("Sucesso", "Notas lancadas.")
        win.destroy()
    ttk.Button(win, text="Salvar", command=salvar, bootstyle="success").pack(pady=8)
    ttk.Button(win, text="Cancelar", command=win.destroy, bootstyle="danger").pack()

# -------------------- MENUS (apos login) --------------------
def abrir_menu(usuario):
    tipo = usuario["tipo"]
    nome = usuario["nome"]
    cpf = usuario["cpf"]

    win = ttk.Toplevel(app)
    win.title(f"Menu - {nome}")
    win.geometry("520x360")
    ttk.Label(win, text=f"Bem-vindo(a), {nome}!", font=("Helvetica", 16, "bold")).pack(pady=10)

    if tipo == "aluno":
        ttk.Button(win, text="Ver Boletim", command=lambda: ui_ver_notas(cpf), bootstyle="info").pack(pady=6)
        ttk.Button(win, text="Enviar Atividade", command=lambda: ui_enviar_atividade(cpf), bootstyle="success").pack(pady=6)

    elif tipo == "professor":
        ttk.Button(win, text="Postar Atividade", command=ui_postar_atividade, bootstyle="primary").pack(pady=6)
        ttk.Button(win, text="Listar/Avaliar Submissoes", command=ui_listar_atividades_para_avaliacao, bootstyle="info").pack(pady=6)
        ttk.Button(win, text="Lancar Notas (NP1/NP2)", command=ui_lancar_notas, bootstyle="warning").pack(pady=6)

    elif tipo == "admin":
        ttk.Button(win, text="Cadastrar Usuario", command=lambda: ui_cadastrar_usuario(win), bootstyle="success").pack(pady=8)
        ttk.Button(win, text="Listar/Excluir/Editar Usuarios", command=lambda: ui_listar_usuarios(win), bootstyle="info").pack(pady=6)

    ttk.Button(win, text="Fechar Menu", command=win.destroy, bootstyle="danger").pack(pady=12)

# -------------------- LOGIN PRINCIPAL --------------------
def fazer_login():
    cpf = entry_cpf.get().strip()
    senha = entry_senha.get().strip()
    if not (cpf and senha):
        messagebox.showwarning("Aviso", "Preencha todos os campos!")
        return
    usuario = validar_login(cpf, senha)
    if usuario is None:
        messagebox.showerror("Erro", "CPF ou senha incorretos!")
        return
    messagebox.showinfo("Sucesso", f"Logado como {usuario['tipo']}")
    abrir_menu(usuario)

# -------------------- TELA PRINCIPAL --------------------
frame = ttk.Frame(app, padding=18); frame.pack(expand=YES)
ttk.Label(frame, text="SISTEMA EDUCACIONAL PIM", font=("Helvetica", 20, "bold")).pack(pady=6)
ttk.Label(frame, text="Login por CPF", font=("Helvetica", 10)).pack(pady=2)
f = ttk.Frame(frame); f.pack(pady=8)
ttk.Label(f, text="CPF:").grid(row=0, column=0, sticky=W, padx=6, pady=6)
entry_cpf = ttk.Entry(f, width=36); entry_cpf.grid(row=0, column=1, pady=6)
ttk.Label(f, text="Senha:").grid(row=1, column=0, sticky=W, padx=6, pady=6)
entry_senha = ttk.Entry(f, width=36, show="*"); entry_senha.grid(row=1, column=1, pady=6)
ttk.Button(frame, text="Entrar", command=fazer_login, bootstyle="primary").pack(pady=10)
ttk.Button(frame, text="Sair", command=app.destroy, bootstyle="danger").pack()

# -------------------- EXEC --------------------
app.mainloop()
