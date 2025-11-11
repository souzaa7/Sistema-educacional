#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "usuario.h"
#include "conteudo.h"
#include "atividade.h"
#include "nota.h"

#define USUARIOS_FILE "usuarios.csv"

/* utilitarios */
void limparBuffer() {
    int c;
    while ((c = getchar()) != '\n' && c != EOF) ;
}

int file_exists(const char *path) {
    FILE *f = fopen(path, "r");
    if (f) { fclose(f); return 1; }
    return 0;
}

/* cadastrar usuario (append) */
void cadastrarUsuario() {
    Usuario u;
    FILE *f;

    printf("\n=== CADASTRO DE USUARIO ===\n");
    printf("Tipo (aluno/professor/adm): ");
    scanf("%19s", u.tipo); limparBuffer();

    printf("Nome: ");
    fgets(u.nome, MAX_NOME, stdin);
    u.nome[strcspn(u.nome, "\n")] = '\0';

    printf("CPF (apenas numeros): ");
    scanf("%19s", u.cpf); limparBuffer();

    printf("Senha: ");
    scanf("%49s", u.senha); limparBuffer();

    /* checar duplicado */
    if (file_exists(USUARIOS_FILE)) {
        f = fopen(USUARIOS_FILE, "r");
        if (!f) { printf("Erro ao abrir arquivo de usuarios.\n"); return; }
        char linha[LINE_BUF];
        while (fgets(linha, sizeof(linha), f)) {
            char tipo[MAX_TIPO], cpf[MAX_CPF], senha[MAX_SENHA], nome[MAX_NOME];
            if (sscanf(linha, "%[^,],%[^,],%[^,],%[^\n]", tipo, cpf, senha, nome) == 4) {
                if (strcmp(cpf, u.cpf) == 0) {
                    printf("CPF ja cadastrado. Cadastro cancelado.\n");
                    fclose(f);
                    return;
                }
            }
        }
        fclose(f);
    }

    f = fopen(USUARIOS_FILE, "a");
    if (!f) { printf("Erro ao abrir arquivo para escrita.\n"); return; }
    /* se o arquivo estava vazio, adicionar cabecalho - vamos checar posicao */
    if (ftell(f) == 0 && !file_exists(USUARIOS_FILE)) {
        /* se for um novo arquivo criado por fopen, escreve cabecalho */
        fprintf(f, "tipo,cpf,senha,nome\n");
    }
    /* appende */
    fprintf(f, "%s,%s,%s,%s\n", u.tipo, u.cpf, u.senha, u.nome);
    fclose(f);

    printf("Usuario cadastrado com sucesso.\n");
}

/* login por CPF+senha */
int loginUsuario(Usuario *u) {
    char cpf_busca[MAX_CPF];
    char senha_busca[MAX_SENHA];

    if (!file_exists(USUARIOS_FILE)) {
        printf("Nenhum usuario cadastrado ainda.\n");
        return 0;
    }

    printf("\n=== LOGIN ===\n");
    printf("CPF: ");
    scanf("%19s", cpf_busca); limparBuffer();
    printf("Senha: ");
    scanf("%49s", senha_busca); limparBuffer();

    FILE *f = fopen(USUARIOS_FILE, "r");
    if (!f) { printf("Erro ao abrir usuarios.\n"); return 0; }

    char linha[LINE_BUF];
    while (fgets(linha, sizeof(linha), f)) {
        char tipo[MAX_TIPO], cpf[MAX_CPF], senha[MAX_SENHA], nome[MAX_NOME];
        if (sscanf(linha, "%[^,],%[^,],%[^,],%[^\n]", tipo, cpf, senha, nome) == 4) {
            if (strcmp(cpf, cpf_busca) == 0 && strcmp(senha, senha_busca) == 0) {
                strncpy(u->tipo, tipo, MAX_TIPO-1); u->tipo[MAX_TIPO-1] = '\0';
                strncpy(u->cpf, cpf, MAX_CPF-1); u->cpf[MAX_CPF-1] = '\0';
                strncpy(u->senha, senha, MAX_SENHA-1); u->senha[MAX_SENHA-1] = '\0';
                strncpy(u->nome, nome, MAX_NOME-1); u->nome[MAX_NOME-1] = '\0';
                fclose(f);
                return 1;
            }
        }
    }

    fclose(f);
    return 0;
}

/* listar usuarios (oculta senha) */
void listarUsuarios() {
    if (!file_exists(USUARIOS_FILE)) {
        printf("Nenhum usuario cadastrado.\n");
        return;
    }
    FILE *f = fopen(USUARIOS_FILE, "r");
    if (!f) { printf("Erro ao abrir arquivo.\n"); return; }

    char linha[LINE_BUF];
    printf("\n=== LISTA DE USUARIOS ===\n");
    while (fgets(linha, sizeof(linha), f)) {
        char tipo[MAX_TIPO], cpf[MAX_CPF], senha[MAX_SENHA], nome[MAX_NOME];
        if (sscanf(linha, "%[^,],%[^,],%[^,],%[^\n]", tipo, cpf, senha, nome) == 4) {
            /* ocultar senha com asteriscos */
            int len = (int)strlen(senha);
            char oculto[60] = {0};
            for (int i = 0; i < len && i < 58; i++) oculto[i] = '*';
            oculto[(len<58)?len:58] = '\0';
            printf("Tipo: %s | CPF: %s | Senha: %s | Nome: %s\n", tipo, cpf, oculto, nome);
        }
    }
    fclose(f);
}

/* remover usuario por CPF */
void removerUsuario() {
    char cpf_busca[MAX_CPF];
    printf("\nCPF do usuario a remover: ");
    scanf("%19s", cpf_busca); limparBuffer();

    if (!file_exists(USUARIOS_FILE)) {
        printf("Arquivo de usuarios nao encontrado.\n");
        return;
    }

    FILE *f = fopen(USUARIOS_FILE, "r");
    FILE *tmp = fopen("usuarios_tmp.csv", "w");
    if (!f || !tmp) { printf("Erro ao abrir arquivos.\n"); if (f) fclose(f); if (tmp) fclose(tmp); return; }

    char linha[LINE_BUF];
    int removido = 0;

    while (fgets(linha, sizeof(linha), f)) {
        char tipo[MAX_TIPO], cpf[MAX_CPF], senha[MAX_SENHA], nome[MAX_NOME];
        if (sscanf(linha, "%[^,],%[^,],%[^,],%[^\n]", tipo, cpf, senha, nome) == 4) {
            if (strcmp(cpf, cpf_busca) == 0) { removido = 1; continue; }
            fprintf(tmp, "%s,%s,%s,%s\n", tipo, cpf, senha, nome);
        }
    }

    fclose(f); fclose(tmp);
    remove(USUARIOS_FILE);
    rename("usuarios_tmp.csv", USUARIOS_FILE);

    if (removido) printf("Usuario removido com sucesso.\n");
    else printf("Usuario nao encontrado.\n");
}

/* MENUS */
void menuAluno(Usuario *u) {
    int opc;
    do {
        printf("\n=== MENU ALUNO (%s) ===\n", u->nome);
        printf("1 - Listar conteudos\n");
        printf("2 - Enviar atividade\n");
        printf("3 - Ver notas\n");
        printf("0 - Sair\n");
        printf("Opcao: ");
        if (scanf("%d", &opc) != 1) { limparBuffer(); opc = -1; }
        limparBuffer();
        switch (opc) {
            case 1: listarConteudos(); break;
            case 2: enviarAtividade(u->cpf); break;
            case 3: verNotas(u->cpf); break;
            case 0: printf("Saindo do menu do aluno.\n"); break;
            default: printf("Opcao invalida.\n");
        }
    } while (opc != 0);
}

void menuProfessor(Usuario *u) {
    int opc;
    do {
        printf("\n=== MENU PROFESSOR (%s) ===\n", u->nome);
        printf("1 - Postar conteudo\n");
        printf("2 - Postar atividade\n");
        printf("3 - Listar atividades\n");
        printf("4 - Avaliar atividade\n");
        printf("5 - Lancar notas (NP1/NP2)\n");
        printf("0 - Sair\n");
        printf("Opcao: ");
        if (scanf("%d", &opc) != 1) { limparBuffer(); opc = -1; }
        limparBuffer();
        switch (opc) {
            case 1: postarConteudo(u->cpf); break;
            case 2: postarAtividade(u->cpf); break;
            case 3: listarAtividades(); break;
            case 4: avaliarAtividade(); break;
            case 5: lancarNota(); break;
            case 0: printf("Saindo do menu do professor.\n"); break;
            default: printf("Opcao invalida.\n");
        }
    } while (opc != 0);
}

void menuAdministrador(Usuario *u) {
    int opc;
    do {
        printf("\n=== MENU ADMINISTRADOR (%s) ===\n", u->nome);
        printf("1 - Cadastrar usuario\n");
        printf("2 - Remover usuario\n");
        printf("3 - Listar usuarios\n");
        printf("4 - Gerar relatorio de medias\n");
        printf("0 - Sair\n");
        printf("Opcao: ");
        if (scanf("%d", &opc) != 1) { limparBuffer(); opc = -1; }
        limparBuffer();
        switch (opc) {
            case 1: cadastrarUsuario(); break;
            case 2: removerUsuario(); break;
            case 3: listarUsuarios(); break;
            case 4: gerarRelatorio(); break;
            case 0: printf("Saindo do menu do administrador.\n"); break;
            default: printf("Opcao invalida.\n");
        }
    } while (opc != 0);
}
