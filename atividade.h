#ifndef ATIVIDADE_H
#define ATIVIDADE_H

#include "usuario.h"

typedef struct {
    char cpf_aluno[MAX_CPF];
    char disciplina[MAX_DISCIPLINA];
    char descricao[MAX_DESC];
    char nota[16];
    char status[20];
} Atividade;

typedef struct {
    int id;
    int atividade_id;
    char aluno_cpf[MAX_CPF];
    char arquivo[200];
    char dataEnvio[30];
    char nota[16];
    char status[20];
} Submissao;

void enviarAtividade(const char *cpfAluno);
void listarAtividades();
void postarAtividade(const char *cpfProfessor);
void listarSubmissoes();
void avaliarAtividade();

#endif
