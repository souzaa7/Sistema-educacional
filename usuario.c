#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "usuario.h"

#define USUARIOS_FILE "usuarios.csv"
#define LINE_BUF 512

/* ------------------ Funções utilitárias ------------------ */

int file_exists(const char *path) {
    FILE *f = fopen(path, "r");
    if (f) {
        fclose(f);
        return 1;
    }
    return 0;
}

void limparBuffer() {
    int c;
    while ((c = getchar()) != '\n' && c != EOF);
}

/* ------------------ Funções de Usuário ------------------ */

void cadastrarUsuario() {
    Usuario u;
    FILE *f;
    int arquivo_existe;

    printf("\n=== CADASTRO DE USUARIO ===\n");
    printf("CPF: ");
    scanf("%s", u.cpf);
    limparBuffer();

    printf("Senha: ");
    scanf("%s", u.senha);
    limparBuffer();

    printf("Nome (sem virgula): ");
    fgets(u.nome, MAX_NOME, stdin);
    u.nome[strcspn(u.nome, "\n")] = '\0';

    printf("Tipo (aluno/professor/admin): ");
    scanf("%s", u.tipo);
    limparBuffer();

    // Verifica duplicidade
    f = fopen(USUARIOS_FILE, "r");
    if (f) {
        char linha[LINE_BUF];
        while (fgets(linha, sizeof(linha), f)) {
            char cpf[MAX_CPF], senha[MAX_SENHA], nome[MAX_NOME], tipo[MAX_TIPO];
            if (sscanf(linha, "%[^,],%[^,],%[^,],%[^\n]", cpf, senha, nome, tipo) == 4) {
                if (strcmp(cpf, u.cpf) == 0) {
                    printf("Erro: CPF ja cadastrado.\n");
                    fclose(f);
                    return;
                }
            }
        }
        fclose(f);
    }

    // Verifica se o arquivo existe
    arquivo_existe = file_exists(USUARIOS_FILE);

    // Abre para escrita (modo w se for novo, modo a se ja existir)
    f = fopen(USUARIOS_FILE, arquivo_existe ? "a" : "w");
    if (!f) {
        printf("Erro ao abrir usuarios.csv!\n");
        return;
    }

    // Se for um novo arquivo, escreve o cabeçalho na ordem correta
    if (!arquivo_existe) {
        fprintf(f, "cpf,senha,nome,tipo\n");
    }

    // Grava o usuário na ordem correta
    fprintf(f, "%s,%s,%s,%s\n", u.cpf, u.senha, u.nome, u.tipo);

    fclose(f);
    printf("Usuario cadastrado com sucesso!\n");
}

void listarUsuarios() {
    FILE *f = fopen(USUARIOS_FILE, "r");
    if (!f) {
        printf("Nenhum usuario cadastrado ainda.\n");
        return;
    }

    char linha[LINE_BUF];
    printf("\n=== LISTA DE USUARIOS ===\n");

    // pula cabeçalho
    fgets(linha, sizeof(linha), f);

    while (fgets(linha, sizeof(linha), f)) {
        char cpf[MAX_CPF], senha[MAX_SENHA], nome[MAX_NOME], tipo[MAX_TIPO];
        if (sscanf(linha, "%[^,],%[^,],%[^,],%[^\n]", cpf, senha, nome, tipo) == 4) {
            printf("CPF: %s | Nome: %s | Tipo: %s\n", cpf, nome, tipo);
        }
    }

    fclose(f);
}

void removerUsuario() {
    char cpfRemover[MAX_CPF];
    printf("\n=== REMOVER USUARIO ===\n");
    printf("Digite o CPF do usuario: ");
    scanf("%s", cpfRemover);
    limparBuffer();

    FILE *f = fopen(USUARIOS_FILE, "r");
    if (!f) {
        printf("Arquivo usuarios.csv nao encontrado.\n");
        return;
    }

    FILE *tmp = fopen("usuarios_tmp.csv", "w");
    if (!tmp) {
        printf("Erro ao criar arquivo temporario.\n");
        fclose(f);
        return;
    }

    char linha[LINE_BUF];
    int removido = 0;

    // cabeçalho
    fprintf(tmp, "cpf,senha,nome,tipo\n");

    // processar o resto
    fgets(linha, sizeof(linha), f);
    while (fgets(linha, sizeof(linha), f)) {
        char cpf[MAX_CPF], senha[MAX_SENHA], nome[MAX_NOME], tipo[MAX_TIPO];
        if (sscanf(linha, "%[^,],%[^,],%[^,],%[^\n]", cpf, senha, nome, tipo) == 4) {
            if (strcmp(cpf, cpfRemover) != 0)
                fprintf(tmp, "%s,%s,%s,%s\n", cpf, senha, nome, tipo);
            else
                removido = 1;
        }
    }

    fclose(f);
    fclose(tmp);

    remove(USUARIOS_FILE);
    rename("usuarios_tmp.csv", USUARIOS_FILE);

    if (removido)
        printf("Usuario removido com sucesso.\n");
    else
        printf("Usuario nao encontrado.\n");
}

/* ------------------ Função de Login ------------------ */

int loginUsuario(Usuario *u) {
    char cpf[MAX_CPF], senha[MAX_SENHA];
    printf("\n=== LOGIN ===\n");
    printf("CPF: ");
    scanf("%s", cpf);
    limparBuffer();

    printf("Senha: ");
    scanf("%s", senha);
    limparBuffer();

    FILE *f = fopen(USUARIOS_FILE, "r");
    if (!f) {
        printf("Arquivo usuarios.csv nao encontrado.\n");
        return 0;
    }

    char linha[LINE_BUF];
    fgets(linha, sizeof(linha), f); // pula cabeçalho

    while (fgets(linha, sizeof(linha), f)) {
        char c[MAX_CPF], s[MAX_SENHA], n[MAX_NOME], t[MAX_TIPO];
        if (sscanf(linha, "%[^,],%[^,],%[^,],%[^\n]", c, s, n, t) == 4) {
            if (strcmp(c, cpf) == 0 && strcmp(s, senha) == 0) {
                strcpy(u->cpf, c);
                strcpy(u->senha, s);
                strcpy(u->nome, n);
                strcpy(u->tipo, t);
                fclose(f);
                return 1;
            }
        }
    }

    fclose(f);
    return 0;
}

/* ------------------ Menus ------------------ */

void menuAluno(Usuario *u) {
    int opcao;
    do {
        printf("\n=== MENU ALUNO ===\n");
        printf("1. Enviar atividade\n");
        printf("2. Ver boletim\n");
        printf("0. Sair\n");
        printf("Escolha: ");
        scanf("%d", &opcao);

        switch (opcao) {
            case 1:
                printf("Funcao de envio de atividade ainda nao implementada.\n");
                break;
            case 2:
                printf("Funcao de visualizacao de boletim ainda nao implementada.\n");
                break;
            case 0:
                printf("Saindo...\n");
                break;
            default:
                printf("Opcao invalida!\n");
        }
    } while (opcao != 0);
}

void menuProfessor(Usuario *u) {
    int opcao;
    do {
        printf("\n=== MENU PROFESSOR ===\n");
        printf("1. Postar atividade\n");
        printf("2. Avaliar atividade\n");
        printf("3. Lancar notas\n");
        printf("0. Sair\n");
        printf("Escolha: ");
        scanf("%d", &opcao);

        switch (opcao) {
            case 1:
                printf("Funcao de postar atividade ainda nao implementada.\n");
                break;
            case 2:
                printf("Funcao de avaliar atividade ainda nao implementada.\n");
                break;
            case 3:
                printf("Funcao de lancar notas ainda nao implementada.\n");
                break;
            case 0:
                printf("Saindo...\n");
                break;
            default:
                printf("Opcao invalida!\n");
        }
    } while (opcao != 0);
}

void menuAdministrador(Usuario *u) {
    int opcao;
    do {
        printf("\n=== MENU ADMINISTRADOR ===\n");
        printf("1. Cadastrar usuario\n");
        printf("2. Listar usuarios\n");
        printf("3. Remover usuario\n");
        printf("0. Sair\n");
        printf("Escolha: ");
        scanf("%d", &opcao);

        switch (opcao) {
            case 1:
                cadastrarUsuario();
                break;
            case 2:
                listarUsuarios();
                break;
            case 3:
                removerUsuario();
                break;
            case 0:
                printf("Saindo...\n");
                break;
            default:
                printf("Opcao invalida!\n");
        }
    } while (opcao != 0);
}