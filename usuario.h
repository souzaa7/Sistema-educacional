#ifndef USUARIO_H
#define USUARIO_H

#define MAX_TIPO 20
#define MAX_CPF 20
#define MAX_SENHA 50
#define MAX_NOME 100
#define MAX_DISCIPLINA 100
#define MAX_DESC 300
#define LINE_BUF 512

typedef struct {
    char tipo[MAX_TIPO];   // "aluno", "professor", "adm"
    char cpf[MAX_CPF];
    char senha[MAX_SENHA];
    char nome[MAX_NOME];
} Usuario;

/* utilitarios compartidos */
void limparBuffer();
int file_exists(const char *path);

/* usuario */
void cadastrarUsuario();
int loginUsuario(Usuario *u);
void listarUsuarios();
void removerUsuario();

/* menus */
void menuAluno(Usuario *u);
void menuProfessor(Usuario *u);
void menuAdministrador(Usuario *u);

#endif
