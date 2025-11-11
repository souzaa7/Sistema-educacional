#ifndef NOTA_H
#define NOTA_H

#include "usuario.h"

typedef struct {
    char cpf_aluno[MAX_CPF];
    char disciplina[MAX_DISCIPLINA];
    float np1;
    float np2;
    float media;
} Nota;

void lancarNota();
void editarNota();
void verNotas(const char *cpfAluno);
void gerarRelatorio();

#endif
