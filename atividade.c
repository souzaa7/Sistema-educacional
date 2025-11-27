#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "atividade.h"

#define ATIVIDADES_FILE "atividades.csv"


/* --------------------------------------
        GERAÇÃO DE IDs
---------------------------------------*/

static int nextId() {
    if (!file_exists(ATIVIDADES_FILE)) return 1;

    FILE *f = fopen(ATIVIDADES_FILE, "r");
    char linha[LINE_BUF];
    int maxID = 0;

    while (fgets(linha, sizeof(linha), f)) {
        int id;
        if (sscanf(linha, "%d,", &id) == 1)
            if (id > maxID) maxID = id;
    }
    fclose(f);
    return maxID + 1;
}

/* --------------------------------------
        PROFESSOR – POSTAR ATIVIDADE
---------------------------------------*/

void postarAtividade(const char *cpfProfessor) {
    FILE *f;
    int existe = file_exists(ATIVIDADES_FILE);
    f = fopen(ATIVIDADES_FILE, "a");

    if (!f) { printf("Erro ao abrir arquivo.\n"); return; }

    if (!existe) {
        fprintf(f, "id,tipo,atividade_id,cpf_autor,disciplina,descricao,arquivo,data,nota,status\n");
    }

    RegistroAtividade r;
    r.id = nextId();
    strcpy(r.tipo, "publicada");
    r.atividade_id = 0;
    strcpy(r.cpf_autor, cpfProfessor);

    printf("\n=== POSTAR ATIVIDADE ===\n");
    printf("Disciplina: ");
    fgets(r.disciplina, sizeof(r.disciplina), stdin);
    r.disciplina[strcspn(r.disciplina, "\n")] = 0;

    printf("Descricao: ");
    fgets(r.descricao, sizeof(r.descricao), stdin);
    r.descricao[strcspn(r.descricao, "\n")] = 0;

    printf("Data entrega (AAAA-MM-DD): ");
    fgets(r.data, sizeof(r.data), stdin);
    r.data[strcspn(r.data, "\n")] = 0;

    fprintf(f, "%d,publicada,0,%s,%s,%s,,%s,,Pendente\n",
        r.id, r.cpf_autor, r.disciplina, r.descricao, r.data);

    fclose(f);
    printf("Atividade publicada com sucesso.\n");
}

/* --------------------------------------
        PROFESSOR – LISTAR ATIVIDADES
---------------------------------------*/

void listarAtividadesProfessor() {
    if (!file_exists(ATIVIDADES_FILE)) {
        printf("Nenhuma atividade publicada.\n");
        return;
    }

    FILE *f = fopen(ATIVIDADES_FILE, "r");
    char linha[LINE_BUF];

    printf("\n=== ATIVIDADES PUBLICADAS ===\n");

    while (fgets(linha, sizeof(linha), f)) {
        int id, atividade_id;
        char tipo[20], cpf[20], disc[100], desc[300], arquivo[200], data[40], nota[16], status[20];

        sscanf(linha, "%d,%[^,],%d,%[^,],%[^,],%[^,],%[^,],%[^,],%[^,],%s",
            &id, tipo, &atividade_id, cpf, disc, desc, arquivo, data, nota, status);

        if (strcmp(tipo, "publicada") == 0) {
            printf("\nID: %d | Disciplina: %s | Entrega: %s\n%s\n", id, disc, data, desc);
        }
    }
    fclose(f);
}

/* --------------------------------------
        ALUNO – LISTAR ATIVIDADES DISPONÍVEIS
---------------------------------------*/

void listarAtividadesAluno() {
    if (!file_exists(ATIVIDADES_FILE)) {
        printf("Nenhuma atividade encontrada.\n");
        return;
    }

    FILE *f = fopen(ATIVIDADES_FILE, "r");
    char linha[LINE_BUF];

    printf("\n=== ATIVIDADES DISPONÍVEIS ===\n");

    while (fgets(linha, sizeof(linha), f)) {
        int id, atividade_id;
        char tipo[20], cpf[20], disc[100], desc[300], arquivo[200], data[40], nota[16], status[20];

        sscanf(linha, "%d,%[^,],%d,%[^,],%[^,],%[^,],%[^,],%[^,],%[^,],%s",
            &id, tipo, &atividade_id, cpf, disc, desc, arquivo, data, nota, status);

        if (strcmp(tipo, "publicada") == 0) {
            printf("\nID: %d\nDisciplina: %s\nDescricao: %s\nEntrega: %s\n",
                id, disc, desc, data);
        }
    }
    fclose(f);
}

/* --------------------------------------
        ALUNO – ENVIAR SUBMISSÃO
---------------------------------------*/

void enviarSubmissao(const char *cpfAluno) {
    FILE *f;
    int existe = file_exists(ATIVIDADES_FILE);
    f = fopen(ATIVIDADES_FILE, "a");

    if (!f) { printf("Erro ao abrir arquivo.\n"); return; }

    if (!existe) {
        fprintf(f, "id,tipo,atividade_id,cpf_autor,disciplina,descricao,arquivo,data,nota,status\n");
    }

    RegistroAtividade r;
    r.id = nextId();
    strcpy(r.tipo, "submissao");

    printf("\n=== ENVIAR SUBMISSAO ===\nID da atividade: ");
    scanf("%d", &r.atividade_id);
    limparBuffer();

    strcpy(r.cpf_autor, cpfAluno);

    printf("Arquivo (nome): ");
    fgets(r.arquivo, sizeof(r.arquivo), stdin);
    r.arquivo[strcspn(r.arquivo, "\n")] = 0;

    printf("Data envio (AAAA-MM-DD): ");
    fgets(r.data, sizeof(r.data), stdin);
    r.data[strcspn(r.data, "\n")] = 0;

    fprintf(f, "%d,submissao,%d,%s,,,,%s,,Pendente\n",
        r.id, r.atividade_id, r.cpf_autor, r.data);

    fclose(f);
    printf("Submissao enviada!\n");
}

/* --------------------------------------
        ALUNO – LISTAR SUAS SUBMISSÕES
---------------------------------------*/

void listarMinhasSubmissoes(const char *cpfAluno) {
    if (!file_exists(ATIVIDADES_FILE)) {
        printf("Nenhuma submissao encontrada.\n");
        return;
    }

    FILE *f = fopen(ATIVIDADES_FILE, "r");
    char linha[LINE_BUF];

    printf("\n=== MINHAS SUBMISSOES ===\n");

    while (fgets(linha, sizeof(linha), f)) {
        int id, atividade_id;
        char tipo[20], cpf[20], disc[100], desc[300], arquivo[200], data[40], nota[16], status[20];

        sscanf(linha, "%d,%[^,],%d,%[^,],%[^,],%[^,],%[^,],%[^,],%[^,],%s",
            &id, tipo, &atividade_id, cpf, disc, desc, arquivo, data, nota, status);

        if (strcmp(tipo, "submissao") == 0 && strcmp(cpf, cpfAluno) == 0) {

            printf("\nAtividade: %d | Arquivo: %s\nEnviado: %s | Nota: %s | Status: %s\n",
                atividade_id, arquivo, data, nota, status);
        }
    }
    fclose(f);
}

/* --------------------------------------
        PROFESSOR – AVALIAR SUBMISSÃO
---------------------------------------*/

void avaliarSubmissao() {
    if (!file_exists(ATIVIDADES_FILE)) {
        printf("Nenhuma submissao encontrada.\n");
        return;
    }

    int idAvaliar;
    printf("ID da submissao: ");
    scanf("%d", &idAvaliar);
    limparBuffer();

    FILE *f = fopen(ATIVIDADES_FILE, "r");
    FILE *tmp = fopen("temp.csv", "w");

    char linha[LINE_BUF];
    int encontrado = 0;

    fprintf(tmp, "id,tipo,atividade_id,cpf_autor,disciplina,descricao,arquivo,data,nota,status\n");

    while (fgets(linha, sizeof(linha), f)) {
        int id, atividade_id;
        char tipo[20], cpf[20], disc[100], desc[300], arquivo[200], data[40], nota[16], status[20];

        sscanf(linha, "%d,%[^,],%d,%[^,],%[^,],%[^,],%[^,],%[^,],%[^,],%s",
            &id, tipo, &atividade_id, cpf, disc, desc, arquivo, data, nota, status);

        if (id == idAvaliar && strcmp(tipo, "submissao") == 0) {
            float notaF;
            printf("Digite a nota: ");
            scanf("%f", &notaF);
            limparBuffer();

            char notaStr[16];
            snprintf(notaStr, sizeof(notaStr), "%.2f", notaF);

            fprintf(tmp, "%d,%s,%d,%s,%s,%s,%s,%s,%s,Avaliada\n",
                id, tipo, atividade_id, cpf, disc, desc, arquivo, data, notaStr);

            encontrado = 1;
        }
        else {
            fputs(linha, tmp);
        }
    }

    fclose(f);
    fclose(tmp);

    remove(ATIVIDADES_FILE);
    rename("temp.csv", ATIVIDADES_FILE);

    if (encontrado)
        printf("Avaliacao concluida.\n");
    else
        printf("Submissao nao encontrada.\n");
}
