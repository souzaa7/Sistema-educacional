#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "atividade.h"
#include "usuario.h"

#define ATIVIDADES_FILE "atividades.csv"
#define SUBMISSOES_FILE "submissoes.csv"

extern int file_exists(const char *path);
extern void limparBuffer();

/* geradores de id simples */
static int nextAtividadeId() {
    FILE *f = fopen(ATIVIDADES_FILE, "r");
    if (!f) return 1;
    char linha[LINE_BUF];
    int max = 0;
    while (fgets(linha, sizeof(linha), f)) {
        int id;
        if (sscanf(linha, "%d,%*[^,],%*[^,],%*[^,],%*[^,\n]", &id) == 1) if (id > max) max = id;
    }
    fclose(f);
    return max + 1;
}

static int nextSubId() {
    FILE *f = fopen(SUBMISSOES_FILE, "r");
    if (!f) return 1;
    char linha[LINE_BUF];
    int max = 0;
    while (fgets(linha, sizeof(linha), f)) {
        int id;
        if (sscanf(linha, "%d,%*d,%*[^,],%*[^,],%*[^,],%*[^,],%*s", &id) == 1) if (id > max) max = id;
    }
    fclose(f);
    return max + 1;
}

/* PROFESSOR - postar atividade (com id) */
void postarAtividade(const char *cpfProfessor) {
    FILE *f;
    int existe = file_exists(ATIVIDADES_FILE);
    f = fopen(ATIVIDADES_FILE, "a");
    if (!f) { printf("Erro ao abrir arquivo de atividades.\n"); return; }
    if (!existe) fprintf(f, "id,disciplina,descricao,autor_cpf,dataEntrega\n");

    int id = nextAtividadeId();
    char disciplina[MAX_DISCIPLINA], descricao[MAX_DESC], dataEntrega[30];

    printf("\n=== POSTAR ATIVIDADE ===\n");
    printf("Disciplina: ");
    fgets(disciplina, sizeof(disciplina), stdin); disciplina[strcspn(disciplina, "\n")] = '\0';
    printf("Descricao: ");
    fgets(descricao, sizeof(descricao), stdin); descricao[strcspn(descricao, "\n")] = '\0';
    printf("Data de entrega (ex: 2025-11-12): ");
    fgets(dataEntrega, sizeof(dataEntrega), stdin); dataEntrega[strcspn(dataEntrega, "\n")] = '\0';

    /* confirmacao */
    char conf;
    printf("Confirmar publicacao da atividade? (S/N): ");
    scanf(" %c", &conf); limparBuffer();
    if (conf != 'S' && conf != 's') { printf("Publicacao cancelada.\n"); fclose(f); return; }

    fprintf(f, "%d,%s,%s,%s,%s\n", id, disciplina, descricao, cpfProfessor, dataEntrega);
    fclose(f);
    printf("Atividade publicada com sucesso.\n");
}

/* ALUNO - enviar submissao para uma atividade */
void enviarAtividade(const char *cpfAluno) {
    FILE *f;
    int existe = file_exists(SUBMISSOES_FILE);
    f = fopen(SUBMISSOES_FILE, "a");
    if (!f) { printf("Erro ao abrir arquivo de submissoes.\n"); return; }
    if (!existe) fprintf(f, "id,atividade_id,aluno_cpf,arquivo,dataEnvio,nota,status\n");

    Submissao s;
    s.id = nextSubId();
    printf("\n=== ENVIAR SUBMISSAO ===\n");
    printf("ID da atividade: ");
    if (scanf("%d", &s.atividade_id) != 1) { limparBuffer(); printf("ID invalido.\n"); fclose(f); return; }
    limparBuffer();
    strncpy(s.aluno_cpf, cpfAluno, MAX_CPF-1); s.aluno_cpf[MAX_CPF-1] = '\0';
    printf("Resumo do arquivo/enlace: ");
    fgets(s.arquivo, sizeof(s.arquivo), stdin); s.arquivo[strcspn(s.arquivo, "\n")] = '\0';
    printf("Data envio (ex: 2025-11-10): ");
    fgets(s.dataEnvio, sizeof(s.dataEnvio), stdin); s.dataEnvio[strcspn(s.dataEnvio, "\n")] = '\0';
    strcpy(s.nota, "");
    strcpy(s.status, "Pendente");

    /* confirmacao */
    char conf;
    printf("Confirmar envio desta submissao? (S/N): ");
    scanf(" %c", &conf); limparBuffer();
    if (conf != 'S' && conf != 's') { printf("Envio cancelado.\n"); fclose(f); return; }

    fprintf(f, "%d,%d,%s,%s,%s,%s,%s\n", s.id, s.atividade_id, s.aluno_cpf, s.arquivo, s.dataEnvio, s.nota, s.status);
    fclose(f);
    printf("Submissao enviada com sucesso.\n");
}

/* PROFESSOR - listar atividades postadas (para consulta) */
void listarAtividades() {
    if (!file_exists(ATIVIDADES_FILE)) { printf("Nenhuma atividade publica.\n"); return; }
    FILE *f = fopen(ATIVIDADES_FILE, "r");
    if (!f) { printf("Erro ao abrir atividades.csv\n"); return; }
    char linha[LINE_BUF];
    printf("\n=== ATIVIDADES PUBLICADAS ===\n");
    while (fgets(linha, sizeof(linha), f)) {
        int id; char disciplina[MAX_DISCIPLINA], descricao[MAX_DESC], autor[MAX_CPF], dataEntrega[30];
        if (sscanf(linha, "%d,%[^,],%[^,],%[^,],%[^\n]", &id, disciplina, descricao, autor, dataEntrega) == 5) {
            printf("ID:%d | Disciplina:%s | Autor:%s | Entrega:%s\n  %s\n", id, disciplina, autor, dataEntrega, descricao);
        }
    }
    fclose(f);
}

/* PROFESSOR - listar e avaliar submissao */
void listarSubmissoes() {
    if (!file_exists(SUBMISSOES_FILE)) { printf("Nenhuma submissao registrada.\n"); return; }
    FILE *f = fopen(SUBMISSOES_FILE, "r");
    if (!f) { printf("Erro ao abrir submissoes.csv\n"); return; }
    char linha[LINE_BUF];
    printf("\n=== SUBMISSOES ===\n");
    while (fgets(linha, sizeof(linha), f)) {
        int id, aid; char aluno[MAX_CPF], arquivo[200], data[30], nota[16], status[20];
        if (sscanf(linha, "%d,%d,%[^,],%[^,],%[^,],%[^,],%[^\n]", &id, &aid, aluno, arquivo, data, nota, status) >= 4) {
            printf("SubID:%d AtivID:%d Aluno:%s Status:%s Nota:%s\n  %s (enviado:%s)\n", id, aid, aluno, status, (strlen(nota)?nota:"-"), arquivo, data);
        }
    }
    fclose(f);
}

/* PROFESSOR - avaliar submissao (procura por id de submissao) */
void avaliarAtividade() {
    if (!file_exists(SUBMISSOES_FILE)) { printf("Nenhuma submissao registrada.\n"); return; }
    int subId;
    printf("ID da submissao a avaliar: ");
    if (scanf("%d", &subId) != 1) { limparBuffer(); printf("ID invalido.\n"); return; }
    limparBuffer();

    FILE *f = fopen(SUBMISSOES_FILE, "r");
    FILE *tmp = fopen("submissoes_tmp.csv", "w");
    if (!f || !tmp) { if (f) fclose(f); if (tmp) fclose(tmp); printf("Erro ao abrir arquivos.\n"); return; }

    char linha[LINE_BUF];
    int avaliado = 0;
    while (fgets(linha, sizeof(linha), f)) {
        int id, aid; char aluno[MAX_CPF], arquivo[200], data[30], nota[16], status[20];
        if (sscanf(linha, "%d,%d,%[^,],%[^,],%[^,],%[^,],%[^\n]",
                   &id, &aid, aluno, arquivo, data, nota, status) >= 4) {
            if (!avaliado && id == subId && strcmp(status, "Avaliada") != 0) {
                printf("Submissao: %s\nAluno: %s\n", arquivo, aluno);
                float notaF;
                printf("Informe a nota (ex: 8.5): ");
                if (scanf("%f", &notaF) != 1) { limparBuffer(); printf("Entrada invalida.\n"); fprintf(tmp, "%s", linha); continue; }
                limparBuffer();
                /* confirmacao */
                char conf;
                printf("Confirmar avaliacao? (S/N): ");
                scanf(" %c", &conf); limparBuffer();
                if (conf != 'S' && conf != 's') {
                    printf("Avaliacao cancelada.\n");
                    fprintf(tmp, "%s", linha);
                } else {
                    char notaS[16];
                    snprintf(notaS, sizeof(notaS), "%.2f", notaF);
                    fprintf(tmp, "%d,%d,%s,%s,%s,%s,%s\n", id, aid, aluno, arquivo, data, notaS, "Avaliada");
                    avaliado = 1;
                    printf("Submissao avaliada e registrada.\n");
                }
            } else {
                fprintf(tmp, "%s", linha);
            }
        } else {
            fprintf(tmp, "%s", linha);
        }
    }

    fclose(f); fclose(tmp);
    remove(SUBMISSOES_FILE);
    rename("submissoes_tmp.csv", SUBMISSOES_FILE);
    if (!avaliado) printf("Submissao nao encontrada ou ja avaliada.\n");
}
