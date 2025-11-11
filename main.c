#include <stdio.h>
#include <string.h>
#include "usuario.h"

int main() {
    Usuario user;
    int opcao;

    printf("=== Sistema Educacional PIM ===\n");

    do {
        printf("\n--- MENU PRINCIPAL ---\n");
        printf("1 - Fazer login (CPF)\n");
        printf("2 - Cadastrar usuario\n");
        printf("0 - Sair\n");
        printf("Escolha: ");
        if (scanf("%d", &opcao) != 1) {
            limparBuffer();
            opcao = -1;
        }
        limparBuffer();

        switch (opcao) {
            case 1:
                if (loginUsuario(&user)) {
                    if (strcmp(user.tipo, "aluno") == 0) menuAluno(&user);
                    else if (strcmp(user.tipo, "professor") == 0) menuProfessor(&user);
                    else menuAdministrador(&user);
                } else {
                    printf("CPF ou senha incorretos.\n");
                }
                break;
            case 2:
                cadastrarUsuario();
                break;
            case 0:
                printf("Encerrando sistema. Ate mais.\n");
                break;
            default:
                printf("Opcao invalida.\n");
        }
    } while (opcao != 0);

    return 0;
}
