from biblioteca import (
    criar_tabelas,
    cadastrar_usuario, listar_usuarios,
    cadastrar_autor, listar_autores,
    cadastrar_editora, listar_editoras,
    cadastrar_livro, listar_livros,
    cadastrar_emprestimo, listar_emprestimos,
    cadastrar_emprestimo_livro, listar_emprestimos_livros
)

criar_tabelas()

while (True):
    print("\n--- BIBLIOTECA ---")
    print("1 - Cadastrar usuário")
    print("2 - Listar usuários")
    print("3 - Cadastrar autor")
    print("4 - Listar autores")
    print("5 - Cadastrar editora")
    print("6 - Listar editoras")
    print("7 - Cadastrar livro")
    print("8 - Listar livros")
    print("9 - Cadastrar empréstimo")
    print("10 - Listar empréstimos")
    print("11 - Cadastrar empréstimo/livro")
    print("12 - Listar empréstimos/livros")
    print("13 - Sair")

    opcao = input("Digite a opção: ")

    if opcao == '1':
        cadastrar_usuario()
    elif opcao == '2':
        listar_usuarios()
    elif opcao == '3':
        cadastrar_autor()
    elif opcao == '4':
        listar_autores()
    elif opcao == '5':
        cadastrar_editora()
    elif opcao == '6':
        listar_editoras()
    elif opcao == '7':
        cadastrar_livro()
    elif opcao == '8':
        listar_livros()
    elif opcao == '9':
        cadastrar_emprestimo()
    elif opcao == '10':
        listar_emprestimos()
    elif opcao == '11':
        cadastrar_emprestimo_livro()
    elif opcao == '12':
        listar_emprestimos_livros()
    elif opcao == '13':
        print("Programa encerrado.")
        break
    else:
        print("Opção inválida!")
