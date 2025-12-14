import os
import csv
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox, simpledialog

# CONFIG
ARQ_USUARIOS = "usuarios.csv"
ARQ_ATIVIDADES = "atividades.csv"
THEME = "cyborg"

# CAMPOS DO CSV UNIFICADO
ATIV_FIELDS = ["id","tipo","cpf_aluno","disciplina","descricao","status","nota","sub_id"]

# -----------------------
# INICIALIZACAO E MIGRACAO
# -----------------------
def inicializar_arquivos():
    # usuarios.csv
    if not os.path.exists(ARQ_USUARIOS):
        with open(ARQ_USUARIOS, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["cpf","senha","nome","tipo"])
            w.writerow(["11111111111","1234","Aluno Exemplo","aluno"])
            w.writerow(["22222222222","abcd","Professor Exemplo","professor"])
            w.writerow(["33333333333","admin","Administrador","admin"])

    # atividades.csv
    if not os.path.exists(ARQ_ATIVIDADES):
        with open(ARQ_ATIVIDADES, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(ATIV_FIELDS)
    else:
        validar_migrar_csv()

def validar_migrar_csv():
    """Verifica cabecalho e migra se necessario."""
    try:
        with open(ARQ_ATIVIDADES, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            header = reader.fieldnames
    except UnicodeDecodeError:
        with open(ARQ_ATIVIDADES, newline="", encoding="latin-1") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            header = reader.fieldnames

    if header is None:
        # arquivo vazio -> escrever cabecalho padrao
        with open(ARQ_ATIVIDADES, "w", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, fieldnames=ATIV_FIELDS).writeheader()
        return

    header_low = [h.strip().lower() for h in header]
    # se faltar qualquer campo importante, migrar
    if "id" not in header_low or "tipo" not in header_low or "sub_id" not in header_low:
        migrar_csv_antigo(rows, header_low)

def migrar_csv_antigo(rows, header_low):
    """
    Converte formatos antigos pro padrao com sub_id.
    Se o arquivo antigo for do tipo:
      cpf_aluno,disciplina,descricao,status,nota
    entao transformamos cada linha numa submissao com sub_id incremental.
    Se existir id/tipo parcialmente, adaptamos o maximo possivel.
    """
    new = []
    # detectar maior id ja presente
    max_id = 0
    for r in rows:
        try:
            val = r.get("id") or r.get("Id") or r.get("ID")
            if val:
                max_id = max(max_id, int(val))
        except:
            pass

    sub_counter = 1
    for r in rows:
        # tenta mapear campos padrao antigos
        cpf = r.get("cpf_aluno") or r.get("cpf") or r.get("CPF") or ""
        disc = r.get("disciplina") or r.get("disc") or r.get("Disciplina") or ""
        desc = r.get("descricao") or r.get("resposta") or r.get("Descricao") or ""
        status = r.get("status") or r.get("Status") or "Pendente"
        nota = r.get("nota") or r.get("Nota") or ""
        # se existir id em linha antiga, usa, senao atribui 0 temporario
        id_old = r.get("id") or r.get("Id") or ""
        if not id_old:
            id_old = str(max_id + 1)
            max_id += 1
        new.append({
            "id": str(id_old),
            "tipo": "submissao",
            "cpf_aluno": cpf,
            "disciplina": disc,
            "descricao": desc,
            "status": status,
            "nota": nota,
            "sub_id": str(sub_counter)
        })
        sub_counter += 1

    # gravar novo arquivo padrao
    with open(ARQ_ATIVIDADES, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=ATIV_FIELDS)
        w.writeheader()
        w.writerows(new)

# -----------------------
# LEITURA / ESCRITA UTIL
# -----------------------
def ler_atividades():
    try:
        with open(ARQ_ATIVIDADES, newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))
    except UnicodeDecodeError:
        with open(ARQ_ATIVIDADES, newline="", encoding="latin-1") as f:
            return list(csv.DictReader(f))

def sobrescrever_atividades(lista):
    with open(ARQ_ATIVIDADES, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=ATIV_FIELDS)
        w.writeheader()
        w.writerows(lista)

def gerar_novo_id(ativs):
    ids = []
    for a in ativs:
        try:
            ids.append(int(a.get("id", 0)))
        except:
            pass
    return max(ids) + 1 if ids else 1

def gerar_novo_sub_id(ativs):
    subs = []
    for a in ativs:
        try:
            subs.append(int(a.get("sub_id", 0)))
        except:
            pass
    return max(subs) + 1 if subs else 1

# -----------------------
# USUARIOS
# -----------------------
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

# -----------------------
# INICIALIZAR APP
# -----------------------
inicializar_arquivos()
app = ttk.Window(themename=THEME)
app.title("Sistema Educacional PIM")
app.geometry("880x560")

# -----------------------
# ADMIN: cadastrar, listar, editar, excluir
# -----------------------
def ui_cadastrar_usuario(parent=None):
    win = ttk.Toplevel(parent or app)
    win.title("Cadastrar Usuario")
    win.geometry("460x340")
    ttk.Label(win, text="Cadastrar Usuario", font=("Helvetica",14,"bold")).pack(pady=10)
    f = ttk.Frame(win); f.pack(padx=10, pady=6)
    ttk.Label(f, text="CPF:").grid(row=0,column=0,sticky=W,pady=4)
    e_cpf = ttk.Entry(f, width=32); e_cpf.grid(row=0,column=1)
    ttk.Label(f, text="Senha:").grid(row=1,column=0,sticky=W,pady=4)
    e_senha = ttk.Entry(f, width=32, show="*"); e_senha.grid(row=1,column=1)
    ttk.Label(f, text="Nome:").grid(row=2,column=0,sticky=W,pady=4)
    e_nome = ttk.Entry(f, width=32); e_nome.grid(row=2,column=1)
    ttk.Label(f, text="Tipo:").grid(row=3,column=0,sticky=W,pady=4)
    var = ttk.StringVar(value="aluno")
    cb = ttk.Combobox(f, textvariable=var, values=["aluno","professor","admin"], width=30); cb.grid(row=3,column=1)
    def salvar():
        cpf = e_cpf.get().strip(); senha = e_senha.get().strip(); nome = e_nome.get().strip(); tipo = var.get().strip()
        if not (cpf and senha and nome and tipo):
            messagebox.showwarning("Aviso","Preencha todos os campos.")
            return
        if usuario_existe(cpf):
            messagebox.showerror("Erro","CPF ja cadastrado.")
            return
        salvar_usuario({"cpf":cpf,"senha":senha,"nome":nome,"tipo":tipo})
        messagebox.showinfo("OK","Usuario cadastrado.")
        win.destroy()
    ttk.Button(win, text="Salvar", command=salvar, bootstyle="success").pack(pady=8)
    ttk.Button(win, text="Cancelar", command=win.destroy, bootstyle="danger").pack()

def ui_listar_usuarios(parent=None):
    usuarios = ler_usuarios()
    win = ttk.Toplevel(parent or app)
    win.title("Usuarios")
    win.geometry("720x440")
    ttk.Label(win, text="Usuarios Cadastrados", font=("Helvetica",14,"bold")).pack(pady=10)
    cols = ("cpf","nome","tipo")
    tree = ttk.Treeview(win, columns=cols, show="headings", height=14)
    for c in cols:
        tree.heading(c, text=c.upper()); tree.column(c, width=220, anchor="center")
    tree.pack(fill=BOTH, expand=YES, padx=10, pady=6)
    for u in usuarios:
        tree.insert("", "end", values=(u["cpf"], u["nome"], u["tipo"]))

    def excluir():
        sel = tree.focus()
        if not sel:
            messagebox.showwarning("Aviso","Selecione um usuario.")
            return
        cpf = tree.item(sel)["values"][0]
        nome = tree.item(sel)["values"][1]
        if not messagebox.askyesno("Confirmar", f"Excluir usuario {nome} ({cpf})?"):
            return
        novos = [x for x in usuarios if x["cpf"] != cpf]
        sobrescrever_usuarios(novos)
        messagebox.showinfo("OK","Usuario excluido.")
        win.destroy()

    def editar():
        sel = tree.focus()
        if not sel:
            messagebox.showwarning("Aviso","Selecione um usuario.")
            return
        cpf_sel = tree.item(sel)["values"][0]
        usuarios_all = ler_usuarios()
        usuario = next((x for x in usuarios_all if x["cpf"] == cpf_sel), None)
        if not usuario:
            messagebox.showerror("Erro","Usuario nao encontrado.")
            return
        ew = ttk.Toplevel(win); ew.title("Editar Usuario"); ew.geometry("460x340")
        ttk.Label(ew, text="Editar Usuario", font=("Helvetica",14,"bold")).pack(pady=8)
        f2 = ttk.Frame(ew); f2.pack(padx=10, pady=6)
        ttk.Label(f2, text="CPF:").grid(row=0,column=0); ecpf = ttk.Entry(f2, width=28); ecpf.grid(row=0,column=1); ecpf.insert(0, usuario["cpf"]); ecpf.config(state="disabled")
        ttk.Label(f2, text="Senha:").grid(row=1,column=0); esenha = ttk.Entry(f2, width=28); esenha.grid(row=1,column=1); esenha.insert(0, usuario["senha"])
        ttk.Label(f2, text="Nome:").grid(row=2,column=0); enome = ttk.Entry(f2, width=28); enome.grid(row=2,column=1); enome.insert(0, usuario["nome"])
        ttk.Label(f2, text="Tipo:").grid(row=3,column=0); var2 = ttk.StringVar(value=usuario["tipo"]); cb2 = ttk.Combobox(f2, textvariable=var2, values=["aluno","professor","admin"], width=26); cb2.grid(row=3,column=1)
        def salvar_edicao():
            usuario["senha"] = esenha.get().strip(); usuario["nome"] = enome.get().strip(); usuario["tipo"] = var2.get().strip()
            sobrescrever_usuarios(usuarios_all)
            messagebox.showinfo("OK","Usuario atualizado.")
            ew.destroy(); win.destroy()
        ttk.Button(ew, text="Salvar", command=salvar_edicao, bootstyle="success").pack(pady=8)
        ttk.Button(ew, text="Cancelar", command=ew.destroy, bootstyle="danger").pack()

    btns = ttk.Frame(win); btns.pack(pady=8)
    ttk.Button(btns, text="Excluir", command=excluir, bootstyle="danger").grid(row=0,column=0,padx=8)
    ttk.Button(btns, text="Editar", command=editar, bootstyle="warning").grid(row=0,column=1,padx=8)
    ttk.Button(btns, text="Fechar", command=win.destroy, bootstyle="secondary").grid(row=0,column=2,padx=8)

# -----------------------
# PROFESSOR: postar atividade
# -----------------------
def ui_postar_atividade(user):
    win = ttk.Toplevel(app); win.title("Postar Atividade"); win.geometry("520x340")
    ttk.Label(win, text="Postar Atividade", font=("Helvetica",14,"bold")).pack(pady=10)
    f = ttk.Frame(win); f.pack(padx=10, pady=6)
    ttk.Label(f, text="Disciplina:").grid(row=0,column=0,sticky=W,pady=6); e_disc = ttk.Entry(f, width=40); e_disc.grid(row=0,column=1)
    ttk.Label(f, text="Descricao:").grid(row=1,column=0,sticky=W,pady=6); e_desc = ttk.Entry(f, width=40); e_desc.grid(row=1,column=1)
    def salvar():
        disc = e_disc.get().strip(); desc = e_desc.get().strip()
        if not (disc and desc):
            messagebox.showwarning("Aviso","Preencha todos os campos.")
            return
        ativs = ler_atividades(); novo_id = gerar_novo_id(ativs)
        ativs.append({
            "id": str(novo_id),
            "tipo": "publicada",
            "cpf_aluno": "",
            "disciplina": disc,
            "descricao": desc,
            "status": "Publicada",
            "nota": "",
            "sub_id": ""
        })
        sobrescrever_atividades(ativs)
        messagebox.showinfo("OK","Atividade publicada.")
        win.destroy()
    ttk.Button(win, text="Publicar", command=salvar, bootstyle="success").pack(pady=10)
    ttk.Button(win, text="Cancelar", command=win.destroy, bootstyle="danger").pack()

# -----------------------
# ALUNO: ver atividades publicadas e enviar submissao
# -----------------------
def ui_ver_atividades(user):
    cpf = user.get("cpf","")
    ativs = ler_atividades()
    publicadas = [a for a in ativs if a.get("tipo","") == "publicada"]
    win = ttk.Toplevel(app); win.title("Atividades Disponiveis"); win.geometry("840x480")
    ttk.Label(win, text="Atividades Disponiveis", font=("Helvetica",14,"bold")).pack(pady=8)
    cols = ("id","disciplina","descricao","status")
    tree = ttk.Treeview(win, columns=cols, show="headings")
    for c in cols:
        tree.heading(c, text=c.upper()); tree.column(c, width=200, anchor="center")
    tree.pack(fill=BOTH, expand=YES, padx=10, pady=10)
    for a in publicadas:
        tree.insert("", "end", values=(a.get("id",""), a.get("disciplina",""), a.get("descricao",""), a.get("status","")))
    def enviar():
        sel = tree.focus()
        if not sel:
            messagebox.showwarning("Aviso","Selecione uma atividade.")
            return
        vals = tree.item(sel)["values"]
        atividade_id = str(vals[0]); disciplina = vals[1]
        resp = simpledialog.askstring("Resposta","Digite sua resposta (texto):")
        if resp is None or resp.strip() == "":
            return
        ativs2 = ler_atividades()
        new_sub_id = gerar_novo_sub_id(ativs2)
        ativs2.append({
            "id": atividade_id,
            "tipo": "submissao",
            "cpf_aluno": cpf,
            "disciplina": disciplina,
            "descricao": resp.strip(),
            "status": "Pendente",
            "nota": "",
            "sub_id": str(new_sub_id)
        })
        sobrescrever_atividades(ativs2)
        messagebox.showinfo("OK","Submissao enviada.")
        win.destroy()
    ttk.Button(win, text="Enviar Submissao", command=enviar, bootstyle="success").pack(pady=8)
    ttk.Button(win, text="Fechar", command=win.destroy, bootstyle="secondary").pack(pady=6)

# -----------------------
# ALUNO: minhas submissões
# -----------------------
def ui_minhas_submissoes(user):
    cpf = user.get("cpf","")
    ativs = ler_atividades()
    minhas = [a for a in ativs if a.get("tipo","") == "submissao" and a.get("cpf_aluno","") == cpf]
    win = ttk.Toplevel(app); win.title("Minhas Submissoes"); win.geometry("840x480")
    ttk.Label(win, text="Minhas Submissoes", font=("Helvetica",14,"bold")).pack(pady=8)
    cols = ("id","sub_id","disciplina","descricao","status","nota")
    tree = ttk.Treeview(win, columns=cols, show="headings")
    for c in cols:
        tree.heading(c, text=c.upper()); tree.column(c, width=140, anchor="center")
    tree.pack(fill=BOTH, expand=YES, padx=10, pady=10)
    for a in minhas:
        tree.insert("", "end", values=(a.get("id",""), a.get("sub_id",""), a.get("disciplina",""), a.get("descricao",""), a.get("status",""), a.get("nota","")))
    ttk.Button(win, text="Fechar", command=win.destroy, bootstyle="secondary").pack(pady=6)

# -----------------------
# PROFESSOR: listar e avaliar submissões
# -----------------------

def ui_listar_e_avaliar(user):
    ativs = ler_atividades()
    subs = [a for a in ativs if a.get("tipo","").strip() == "submissao"]

    win = ttk.Toplevel(app)
    win.title("Avaliar Submissoes")
    win.geometry("920x520")

    ttk.Label(win, text="Submissoes Registradas", font=("Helvetica",14,"bold")).pack(pady=8)

    cols = ("cpf_aluno","id","sub_id","disciplina","descricao","status","nota")
    tree = ttk.Treeview(win, columns=cols, show="headings")

    for c in cols:
        tree.heading(c, text=c.upper())
        tree.column(c, width=130, anchor="center")
    tree.pack(fill=BOTH, expand=YES, padx=10, pady=10)

    for a in subs:
        tree.insert("", "end", values=(
            a.get("cpf_aluno","").strip(),
            a.get("id","").strip(),
            a.get("sub_id","").strip(),
            a.get("disciplina","").strip(),
            a.get("descricao","").strip(),
            a.get("status","").strip(),
            a.get("nota","").strip()
        ))

    def avaliar():
        sel = tree.focus()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione uma submissao.")
            return

        vals = tree.item(sel)["values"]

        cpf_aluno = str(vals[0]).strip()
        atividade_id = str(vals[1]).strip()
        sub_id = str(vals[2]).strip()
        disciplina = str(vals[3]).strip()

        ativs2 = ler_atividades()

        # BUSCA FINAL CORRIGIDA (SEM FALHAR)
        target = None
        for x in ativs2:
            if (
                x.get("tipo","").strip() == "submissao" and
                x.get("id","").strip() == atividade_id and
                x.get("cpf_aluno","").strip() == cpf_aluno and
                x.get("sub_id","").strip() == sub_id
            ):
                target = x
                break

        if not target:
            messagebox.showerror("Erro", "Submissao nao encontrada.\n(O problema era espaco oculto no CSV, agora resolvido.)")
            return

        aw = ttk.Toplevel(win)
        aw.title("Avaliar Submissao")
        aw.geometry("520x420")

        ttk.Label(aw, text="Avaliar Submissao", font=("Helvetica",14,"bold")).pack(pady=8)
        ttk.Label(aw, text=f"Aluno: {cpf_aluno}").pack()
        ttk.Label(aw, text=f"Atividade ID: {atividade_id} | Sub ID: {sub_id}").pack()

        ttk.Label(aw, text="Resposta:").pack(pady=6)
        ttk.Label(aw, text=target.get("descricao",""), wraplength=480).pack()

        ttk.Label(aw, text="Nota:").pack(pady=6)
        e_nota = ttk.Entry(aw, width=20)
        e_nota.pack()

        def salvar():
            nota = e_nota.get().strip()
            if nota == "":
                messagebox.showwarning("Aviso", "Informe a nota.")
                return

            for x in ativs2:
                if (
                    x.get("tipo","").strip() == "submissao" and
                    x.get("id","").strip() == atividade_id and
                    x.get("cpf_aluno","").strip() == cpf_aluno and
                    x.get("sub_id","").strip() == sub_id
                ):
                    x["nota"] = nota
                    x["status"] = "Avaliada"

            sobrescrever_atividades(ativs2)
            messagebox.showinfo("OK", "Submissao avaliada.")
            aw.destroy()
            win.destroy()

        ttk.Button(aw, text="Salvar", command=salvar, bootstyle="success").pack(pady=10)
        ttk.Button(aw, text="Cancelar", command=aw.destroy, bootstyle="danger").pack()

    ttk.Button(win, text="Avaliar Selecionada", command=avaliar, bootstyle="success").pack(pady=8)
    ttk.Button(win, text="Fechar", command=win.destroy, bootstyle="secondary").pack(pady=6)


# -----------------------
# MENU apos login
# -----------------------
def abrir_menu(usuario):
    win = ttk.Toplevel(app); win.title("Menu"); win.geometry("460x460")
    nome = usuario.get("nome",""); tipo = usuario.get("tipo",""); cpf = usuario.get("cpf","")
    ttk.Label(win, text=f"Bem-vindo, {nome}", font=("Helvetica",16,"bold")).pack(pady=12)
    if tipo == "aluno":
        ttk.Button(win, text="Ver Atividades", command=lambda: ui_ver_atividades(usuario), bootstyle="info").pack(pady=6)
        ttk.Button(win, text="Minhas Submissoes", command=lambda: ui_minhas_submissoes(usuario), bootstyle="success").pack(pady=6)
    elif tipo == "professor":
        ttk.Button(win, text="Postar Atividade", command=lambda: ui_postar_atividade(usuario), bootstyle="primary").pack(pady=6)
        ttk.Button(win, text="Listar e Avaliar Submissoes", command=lambda: ui_listar_e_avaliar(usuario), bootstyle="danger").pack(pady=6)
    elif tipo == "admin":
        ttk.Button(win, text="Cadastrar Usuario", command=lambda: ui_cadastrar_usuario(win), bootstyle="success").pack(pady=6)
        ttk.Button(win, text="Listar / Editar / Excluir Usuarios", command=lambda: ui_listar_usuarios(win), bootstyle="info").pack(pady=6)
    ttk.Button(win, text="Fechar", command=win.destroy, bootstyle="secondary").pack(pady=12)

# -----------------------
# LOGIN
# -----------------------
def fazer_login():
    cpf = entry_cpf.get().strip(); senha = entry_senha.get().strip()
    if not cpf or not senha:
        messagebox.showwarning("Aviso","Preencha CPF e senha.")
        return
    user = validar_login(cpf, senha)
    if user is None:
        messagebox.showerror("Erro","CPF ou senha incorretos.")
        return
    abrir_menu(user)

# -----------------------
# TELA PRINCIPAL
# -----------------------
frame = ttk.Frame(app, padding=20); frame.pack(expand=YES)
ttk.Label(frame, text="SISTEMA EDUCACIONAL PIM", font=("Helvetica",20,"bold")).pack(pady=12)
f = ttk.Frame(frame); f.pack(pady=6)
ttk.Label(f, text="CPF:").grid(row=0,column=0,pady=8)
entry_cpf = ttk.Entry(f, width=44); entry_cpf.grid(row=0,column=1)
ttk.Label(f, text="Senha:").grid(row=1,column=0,pady=8)
entry_senha = ttk.Entry(f, width=44, show="*"); entry_senha.grid(row=1,column=1)
ttk.Button(frame, text="Entrar", command=fazer_login, bootstyle="primary").pack(pady=10)
ttk.Button(frame, text="Sair", command=app.destroy, bootstyle="danger").pack()

app.mainloop()
