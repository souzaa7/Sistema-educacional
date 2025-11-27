#ifndef ATIVIDADE_H
#define ATIVIDADE_H

#define MAX_CPF 20
#define MAX_DISCIPLINA 100
#define MAX_DESC 300
#define LINE_BUF 512

typedef struct {
    int id;
    char tipo[20];            // "publicada" ou "submissao"
    int atividade_id;
    char cpf_autor[MAX_CPF];
    char disciplina[MAX_DISCIPLINA];
    char descricao[MAX_DESC];
    char arquivo[200];
    char data[40];
    char nota[16];
    char status[20];
} RegistroAtividade;

void postarAtividade(const char *cpfProfessor);
void listarAtividadesProfessor();
void listarAtividadesAluno();
void enviarSubmissao(const char *cpfAluno);
void listarMinhasSubmissoes(const char *cpfAluno);
void avaliarSubmissao();
int file_exists(const char *path);
void limparBuffer();

#endif
