#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "nota.h"
#include "usuario.h"

#define NOTAS_FILE "notas.csv"

extern void limparBuffer();
extern int file_exists(const char *path);

float calcularMedia(float a, float b) {
    return (a + b) / 2.0f;
}

void lancarNota() {
    Nota n;
    if (!file_exists("notas.csv")) {
        FILE *f = fopen(NOTAS_FILE, "a");
        if (f) {
            fprintf(f, "cpf_aluno,disciplina,np1,np2,media\n");
            fclose(f);
        }
    }

    printf("\n=== LANCAR NOTAS ===\n");
    printf("CPF do aluno: ");
    scanf("%19s", n.cpf_aluno); limparBuffer();
    printf("Disciplina: ");
    fgets(n.disciplina, MAX_DISCIPLINA, stdin); n.disciplina[strcspn(n.disciplina, "\n")] = '\0';
    printf("NP1: ");
    if (scanf("%f", &n.np1) != 1) { limparBuffer(); printf("Entrada invalida.\n"); return; }
    limparBuffer();
    printf("NP2: ");
    if (scanf("%f", &n.np2) != 1) { limparBuffer(); printf("Entrada invalida.\n"); return; }
    limparBuffer();

    n.media = calcularMedia(n.np1, n.np2);

    char conf;
    printf("Confirmar lancamento das notas (S/N): ");
    scanf(" %c", &conf); limparBuffer();
    if (conf != 'S' && conf != 's') { printf("Lancamento cancelado.\n"); return; }

    FILE *f = fopen(NOTAS_FILE, "a");
    if (!f) { printf("Erro ao abrir notas.csv\n"); return; }
    fprintf(f, "%s,%s,%.2f,%.2f,%.2f\n", n.cpf_aluno, n.disciplina, n.np1, n.np2, n.media);
    fclose(f);
    printf("Notas lancadas. Media: %.2f\n", n.media);
}

void editarNota() {
    char cpfBusca[MAX_CPF], disciplinaBusca[MAX_DISCIPLINA];
    printf("\n=== EDITAR NOTA ===\n");
    printf("CPF do aluno: ");
    scanf("%19s", cpfBusca); limparBuffer();
    printf("Disciplina: ");
    fgets(disciplinaBusca, MAX_DISCIPLINA, stdin); disciplinaBusca[strcspn(disciplinaBusca, "\n")] = '\0';

    if (!file_exists(NOTAS_FILE)) { printf("Arquivo de notas nao encontrado.\n"); return; }

    FILE *f = fopen(NOTAS_FILE, "r");
    FILE *tmp = fopen("notas_tmp.csv", "w");
    if (!f || !tmp) { if (f) fclose(f); if (tmp) fclose(tmp); printf("Erro ao abrir arquivos.\n"); return; }

    char linha[LINE_BUF];
    int alterado = 0;
    /* copia cabecalho se houver */
    if (fgets(linha, sizeof(linha), f)) {
        if (strstr(linha, "cpf_aluno") && strchr(linha, ',')) fprintf(tmp, "%s", linha);
    }
    while (fgets(linha, sizeof(linha), f)) {
        Nota t;
        if (sscanf(linha, "%[^,],%[^,],%f,%f,%f", t.cpf_aluno, t.disciplina, &t.np1, &t.np2, &t.media) == 5) {
            if (!alterado && strcmp(t.cpf_aluno, cpfBusca) == 0 && strcmp(t.disciplina, disciplinaBusca) == 0) {
                printf("Notas atuais NP1: %.2f NP2: %.2f Media: %.2f\n", t.np1, t.np2, t.media);
                printf("Nova NP1: ");
                if (scanf("%f", &t.np1) != 1) { limparBuffer(); printf("Entrada invalida.\n"); fprintf(tmp, "%s", linha); continue; }
                limparBuffer();
                printf("Nova NP2: ");
                if (scanf("%f", &t.np2) != 1) { limparBuffer(); printf("Entrada invalida.\n"); fprintf(tmp, "%s", linha); continue; }
                limparBuffer();
                t.media = calcularMedia(t.np1, t.np2);
                char conf;
                printf("Confirmar alteracao das notas (S/N): ");
                scanf(" %c", &conf); limparBuffer();
                if (conf == 'S' || conf == 's') {
                    fprintf(tmp, "%s,%s,%.2f,%.2f,%.2f\n", t.cpf_aluno, t.disciplina, t.np1, t.np2, t.media);
                    alterado = 1;
                    printf("Alteracao salva.\n");
                } else {
                    fprintf(tmp, "%s", linha);
                    printf("Alteracao cancelada.\n");
                }
            } else {
                fprintf(tmp, "%s", linha);
            }
        } else {
            fprintf(tmp, "%s", linha);
        }
    }
    fclose(f); fclose(tmp);
    remove(NOTAS_FILE);
    rename("notas_tmp.csv", NOTAS_FILE);
    if (!alterado) printf("Registro nao encontrado.\n");
}

void verNotas(const char *cpfAluno) {
    if (!file_exists(NOTAS_FILE)) { printf("Nenhuma nota registrada.\n"); return; }
    FILE *f = fopen(NOTAS_FILE, "r");
    if (!f) { printf("Erro ao abrir notas.csv\n"); return; }
    char linha[LINE_BUF];
    printf("\n=== BOLETIM DO ALUNO (%s) ===\n", cpfAluno);
    while (fgets(linha, sizeof(linha), f)) {
        Nota t;
        if (sscanf(linha, "%[^,],%[^,],%f,%f,%f", t.cpf_aluno, t.disciplina, &t.np1, &t.np2, &t.media) == 5) {
            if (strcmp(t.cpf_aluno, cpfAluno) == 0) {
                printf("Disciplina: %s | NP1: %.2f | NP2: %.2f | Media: %.2f\n", t.disciplina, t.np1, t.np2, t.media);
            }
        }
    }
    fclose(f);
}

void gerarRelatorio() {
    if (!file_exists(NOTAS_FILE)) { printf("Nenhuma nota registrada.\n"); return; }
    FILE *f = fopen(NOTAS_FILE, "r");
    if (!f) { printf("Erro ao abrir notas.csv\n"); return; }
    char linha[LINE_BUF];
    char **cpfs = NULL;
    float *somas = NULL;
    int *conts = NULL;
    int count = 0;
    /* pular cabecalho se houver */
    if (fgets(linha, sizeof(linha), f)) {
        if (strstr(linha, "cpf_aluno") && strchr(linha, ',')) { /* pula */ }
        else { /* se primeira linha for dado, processa abaixo */ }
    }
    while (fgets(linha, sizeof(linha), f)) {
        Nota t;
        if (sscanf(linha, "%[^,],%[^,],%f,%f,%f", t.cpf_aluno, t.disciplina, &t.np1, &t.np2, &t.media) == 5) {
            int i, found = 0;
            for (i = 0; i < count; i++) if (strcmp(cpfs[i], t.cpf_aluno) == 0) { found = 1; break; }
            if (!found) {
                cpfs = realloc(cpfs, (count+1) * sizeof(char*));
                somas = realloc(somas, (count+1) * sizeof(float));
                conts = realloc(conts, (count+1) * sizeof(int));
                cpfs[count] = malloc(strlen(t.cpf_aluno)+1);
                strcpy(cpfs[count], t.cpf_aluno);
                somas[count] = t.media;
                conts[count] = 1;
                count++;
            } else {
                somas[i] += t.media;
                conts[i]++;
            }
        }
    }
    fclose(f);
    if (count == 0) { printf("Nenhuma nota para gerar relatorio.\n"); return; }
    FILE *r = fopen("relatorio.csv", "w");
    if (!r) { printf("Erro ao criar relatorio.csv\n"); return; }
    fprintf(r, "cpf_aluno,media_geral\n");
    for (int i = 0; i < count; i++) {
        fprintf(r, "%s,%.2f\n", cpfs[i], somas[i] / conts[i]);
        free(cpfs[i]);
    }
    free(cpfs); free(somas); free(conts);
    fclose(r);
    printf("Relatorio gerado: relatorio.csv\n");
}
