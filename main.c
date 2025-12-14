#include <stdio.h>
#include <string.h>
#include "usuario.h"
#include "atividade.h"

int main() {
    Usuario user;
    int opcao;

    printf("=== Sistema Educacional PIM ===\n");

    do {
        printf("\n--- MENU PRINCIPAL ---\n");
        printf("1 - Fazer login\n");
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

                    /* MENU DE ALUNO */
                    if (strcmp(user.tipo, "aluno") == 0) {
                        int op;
                        do {
                            printf("\n--- MENU ALUNO ---\n");
                            printf("1 - Ver atividades\n");
                            printf("2 - Enviar submissao\n");
                            printf("3 - Ver minhas submissões/notas\n");
                            printf("0 - Sair\nEscolha: ");
                            scanf("%d", &op);
                            limparBuffer();

                            if (op == 1) listarAtividadesAluno();
                            else if (op == 2) enviarSubmissao(user.cpf);
                            else if (op == 3) listarMinhasSubmissoes(user.cpf);

                        } while (op != 0);
                    }

                    /* MENU DE PROFESSOR */
                    else if (strcmp(user.tipo, "professor") == 0) {
                        int op;
                        do {
                            printf("\n--- MENU PROFESSOR ---\n");
                            printf("1 - Postar atividade\n");
                            printf("2 - Listar atividades\n");
                            printf("3 - Avaliar submissão\n");
                            printf("0 - Sair\nEscolha: ");
                            scanf("%d", &op);
                            limparBuffer();

                            if (op == 1) postarAtividade(user.cpf);
                            else if (op == 2) listarAtividadesProfessor();
                            else if (op == 3) avaliarSubmissao();

                        } while (op != 0);
                    }

                    /* ADMIN */
                    else {
                        printf("Administrador conectado.\n");
                    }

                } else {
                    printf("CPF ou senha incorretos.\n");
                }
                break;

            case 2:
                cadastrarUsuario();
                break;

            case 0:
                printf("Finalizando...\n");
                break;

            default:
                printf("Opcao invalida.\n");
        }

    } while (opcao != 0);

    return 0;
}
