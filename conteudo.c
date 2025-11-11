#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "conteudo.h"

#define CONTEUDOS_FILE "conteudos.csv"

/* auxiliar: verifica se arquivo existe (usa file_exists de usuario.c) */
extern int file_exists(const char *path);
extern void limparBuffer();

static int nextConteudoId() {
    FILE *f = fopen(CONTEUDOS_FILE, "r");
    if (!f) return 1;
    char linha[LINE_BUF];
    int max = 0;
    while (fgets(linha, sizeof(linha), f)) {
        int id;
        if (sscanf(linha, "%d,%*[^,],%*[^,],%*[^,],%*s", &id) == 1) {
            if (id > max) max = id;
        }
    }
    fclose(f);
    return max + 1;
}

void postarConteudo(const char *cpfProfessor) {
    FILE *f;
    int existe = file_exists(CONTEUDOS_FILE);
    f = fopen(CONTEUDOS_FILE, "a");
    if (!f) { printf("Erro ao abrir conteudos.csv\n"); return; }
    if (!existe) fprintf(f, "id,titulo,descricao,disciplina,autor_cpf\n");

    int id = nextConteudoId();
    char titulo[MAX_NOME], descricao[MAX_DESC], disciplina[MAX_DISCIPLINA];

    printf("\n=== POSTAR CONTEUDO ===\n");
    printf("Titulo: ");
    fgets(titulo, sizeof(titulo), stdin); titulo[strcspn(titulo, "\n")] = '\0';
    printf("Descricao: ");
    fgets(descricao, sizeof(descricao), stdin); descricao[strcspn(descricao, "\n")] = '\0';
    printf("Disciplina: ");
    fgets(disciplina, sizeof(disciplina), stdin); disciplina[strcspn(disciplina, "\n")] = '\0';

    fprintf(f, "%d,%s,%s,%s,%s\n", id, titulo, descricao, disciplina, cpfProfessor);
    fclose(f);
    printf("Conteudo postado com sucesso.\n");
}

void listarConteudos() {
    if (!file_exists(CONTEUDOS_FILE)) {
        printf("Nenhum conteudo disponivel.\n");
        return;
    }
    FILE *f = fopen(CONTEUDOS_FILE, "r");
    if (!f) { printf("Erro ao abrir conteudos.csv\n"); return; }
    char linha[LINE_BUF];
    printf("\n=== CONTEUDOS ===\n");
    /* pular possivel cabecalho */
    while (fgets(linha, sizeof(linha), f)) {
        int id;
        char titulo[MAX_NOME], descricao[MAX_DESC], disciplina[MAX_DISCIPLINA], autor[MAX_CPF];
        if (sscanf(linha, "%d,%[^,],%[^,],%[^,],%[^\n]", &id, titulo, descricao, disciplina, autor) == 5) {
            printf("ID:%d | %s (%s) - autor:%s\n  %s\n", id, titulo, disciplina, autor, descricao);
        } else {
            /* pula linhas que nao seguem o padrao (por exemplo cabecalho) */
        }
    }
    fclose(f);
}

void editarConteudo() {
    if (!file_exists(CONTEUDOS_FILE)) {
        printf("Nenhum conteudo disponivel.\n");
        return;
    }
    int idBusca;
    printf("ID do conteudo a editar: ");
    if (scanf("%d", &idBusca) != 1) { limparBuffer(); printf("Entrada invalida.\n"); return; }
    limparBuffer();

    FILE *f = fopen(CONTEUDOS_FILE, "r");
    FILE *tmp = fopen("conteudos_tmp.csv", "w");
    if (!f || !tmp) { if (f) fclose(f); if (tmp) fclose(tmp); printf("Erro ao abrir arquivos.\n"); return; }

    char linha[LINE_BUF];
    int alterado = 0;
    while (fgets(linha, sizeof(linha), f)) {
        int id;
        char titulo[MAX_NOME], descricao[MAX_DESC], disciplina[MAX_DISCIPLINA], autor[MAX_CPF];
        if (sscanf(linha, "%d,%[^,],%[^,],%[^,],%[^\n]", &id, titulo, descricao, disciplina, autor) == 5) {
            if (id == idBusca) {
                //Conteudo tmpC; /* usando a struct implicitamente */
                char novoTitulo[MAX_NOME], novaDesc[MAX_DESC], novaDisc[MAX_DISCIPLINA];
                printf("Novo titulo: ");
                fgets(novoTitulo, sizeof(novoTitulo), stdin); novoTitulo[strcspn(novoTitulo, "\n")] = '\0';
                printf("Nova descricao: ");
                fgets(novaDesc, sizeof(novaDesc), stdin); novaDesc[strcspn(novaDesc, "\n")] = '\0';
                printf("Nova disciplina: ");
                fgets(novaDisc, sizeof(novaDisc), stdin); novaDisc[strcspn(novaDisc, "\n")] = '\0';
                fprintf(tmp, "%d,%s,%s,%s,%s\n", id, novoTitulo, novaDesc, novaDisc, autor);
                alterado = 1;
            } else {
                fprintf(tmp, "%s", linha);
            }
        } else {
            fprintf(tmp, "%s", linha);
        }
    }
    fclose(f); fclose(tmp);
    remove(CONTEUDOS_FILE);
    rename("conteudos_tmp.csv", CONTEUDOS_FILE);
    if (alterado) printf("Conteudo atualizado.\n"); else printf("Conteudo nao encontrado.\n");
}

void removerConteudo() {
    if (!file_exists(CONTEUDOS_FILE)) {
        printf("Nenhum conteudo disponivel.\n");
        return;
    }
    int idBusca;
    printf("ID do conteudo a remover: ");
    if (scanf("%d",&idBusca) != 1) { limparBuffer(); printf("Entrada invalida.\n"); return; }
    limparBuffer();

    FILE *f = fopen(CONTEUDOS_FILE, "r");
    FILE *tmp = fopen("conteudos_tmp.csv", "w");
    if (!f || !tmp) { if (f) fclose(f); if (tmp) fclose(tmp); printf("Erro ao abrir arquivos.\n"); return; }

    char linha[LINE_BUF];
    int removido = 0;
    while (fgets(linha, sizeof(linha), f)) {
        int id; char titulo[MAX_NOME], descricao[MAX_DESC], disciplina[MAX_DISCIPLINA], autor[MAX_CPF];
        if (sscanf(linha, "%d,%[^,],%[^,],%[^,],%[^\n]", &id, titulo, descricao, disciplina, autor) == 5) {
            if (id == idBusca) { removido = 1; continue; }
            fprintf(tmp, "%s", linha);
        } else fprintf(tmp, "%s", linha);
    }
    fclose(f); fclose(tmp);
    remove(CONTEUDOS_FILE);
    rename("conteudos_tmp.csv", CONTEUDOS_FILE);
    if (removido) printf("Conteudo removido.\n"); else printf("Conteudo nao encontrado.\n");
}
