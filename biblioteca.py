import sqlite3
from datetime import datetime

BANCO = "biblioteca.db"


def conectar():
    conexao = sqlite3.connect(BANCO)
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao


def criar_tabelas():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS autores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS editoras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS livros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor_id INTEGER NOT NULL,
            editora_id INTEGER NOT NULL,
            ano_publicacao INTEGER NOT NULL,
            edicao INTEGER NOT NULL,
            disponivel INTEGER NOT NULL,
            FOREIGN KEY (autor_id) REFERENCES autores(id),
            FOREIGN KEY (editora_id) REFERENCES editoras(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS emprestimos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            data TEXT NOT NULL,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS emprestimos_livros (
            emprestimo_id INTEGER NOT NULL,
            livro_id INTEGER NOT NULL,
            data_devolucao TEXT,
            PRIMARY KEY (emprestimo_id, livro_id),
            FOREIGN KEY (emprestimo_id) REFERENCES emprestimos(id),
            FOREIGN KEY (livro_id) REFERENCES livros(id)
        )
    """)

    conexao.commit()
    conexao.close()


def ler_inteiro(mensagem):
    while True:
        try:
            return int(input(mensagem))
        except ValueError:
            print("Digite um número válido!")


def ler_data(mensagem):
    while True:
        data = input(mensagem)
        try:
            datetime.strptime(data, "%d/%m/%Y")
            return data
        except ValueError:
            print("Data inválida! Use o formato dd/mm/aaaa.")


def confirmar_disponibilidade():
    while True:
        resposta = input("Livro disponível? (S/N): ").upper()
        if resposta == "S":
            return 1
        elif resposta == "N":
            return 0
        else:
            print("Digite apenas S ou N.")


def cadastrar_usuario():
    nome = input("Nome do usuário: ")

    conexao = conectar()
    conexao.execute("INSERT INTO usuarios (nome) VALUES (?)", (nome,))
    conexao.commit()
    conexao.close()
    print("Usuário cadastrado com sucesso!")


def listar_usuarios():
    conexao = conectar()
    usuarios = conexao.execute(
        "SELECT id, nome FROM usuarios ORDER BY id"
    ).fetchall()
    conexao.close()

    print("\n--- Usuários ---")
    if len(usuarios) == 0:
        print("Nenhum usuário cadastrado.")
    else:
        for usuario in usuarios:
            print(f"ID: {usuario[0]} | Nome: {usuario[1]}")


def cadastrar_autor():
    nome = input("Nome do autor: ")

    conexao = conectar()
    conexao.execute("INSERT INTO autores (nome) VALUES (?)", (nome,))
    conexao.commit()
    conexao.close()
    print("Autor cadastrado com sucesso!")


def listar_autores():
    conexao = conectar()
    autores = conexao.execute(
        "SELECT id, nome FROM autores ORDER BY id"
    ).fetchall()
    conexao.close()

    print("\n--- Autores ---")
    if len(autores) == 0:
        print("Nenhum autor cadastrado.")
    else:
        for autor in autores:
            print(f"ID: {autor[0]} | Nome: {autor[1]}")


def cadastrar_editora():
    nome = input("Nome da editora: ")

    conexao = conectar()
    conexao.execute("INSERT INTO editoras (nome) VALUES (?)", (nome,))
    conexao.commit()
    conexao.close()
    print("Editora cadastrada com sucesso!")


def listar_editoras():
    conexao = conectar()
    editoras = conexao.execute(
        "SELECT id, nome FROM editoras ORDER BY id"
    ).fetchall()
    conexao.close()

    print("\n--- Editoras ---")
    if len(editoras) == 0:
        print("Nenhuma editora cadastrada.")
    else:
        for editora in editoras:
            print(f"ID: {editora[0]} | Nome: {editora[1]}")


def cadastrar_livro():
    titulo = input("Título do livro: ")

    print("\nAutores cadastrados:")
    listar_autores()
    autor_id = ler_inteiro("ID do autor: ")

    print("\nEditoras cadastradas:")
    listar_editoras()
    editora_id = ler_inteiro("ID da editora: ")

    ano_publicacao = ler_inteiro("Ano de publicação: ")
    edicao = ler_inteiro("Edição: ")
    disponivel = confirmar_disponibilidade()

    conexao = conectar()
    try:
        conexao.execute("""
            INSERT INTO livros
            (titulo, autor_id, editora_id, ano_publicacao, edicao, disponivel)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (titulo, autor_id, editora_id, ano_publicacao, edicao, disponivel))
        conexao.commit()
        print("Livro cadastrado com sucesso!")
    except sqlite3.IntegrityError:
        print("Erro: o ID do autor ou da editora não existe.")
    finally:
        conexao.close()


def listar_livros():
    conexao = conectar()
    livros = conexao.execute("""
        SELECT livros.id, livros.titulo, autores.nome, editoras.nome,
               livros.ano_publicacao, livros.edicao, livros.disponivel
        FROM livros
        INNER JOIN autores ON autores.id = livros.autor_id
        INNER JOIN editoras ON editoras.id = livros.editora_id
        ORDER BY livros.id
    """).fetchall()
    conexao.close()

    print("\n--- Livros ---")
    if len(livros) == 0:
        print("Nenhum livro cadastrado.")
    else:
        for livro in livros:
            disponivel = "Sim" if livro[6] == 1 else "Não"
            print(
                f"ID: {livro[0]} | Título: {livro[1]} | Autor: {livro[2]} | "
                f"Editora: {livro[3]} | Ano: {livro[4]} | Edição: {livro[5]} | "
                f"Disponível: {disponivel}"
            )


def cadastrar_emprestimo():
    listar_usuarios()
    usuario_id = ler_inteiro("ID do usuário: ")
    data = ler_data("Data do empréstimo (dd/mm/aaaa): ")

    conexao = conectar()
    try:
        conexao.execute(
            "INSERT INTO emprestimos (usuario_id, data) VALUES (?, ?)",
            (usuario_id, data)
        )
        conexao.commit()
        print("Empréstimo cadastrado com sucesso!")
    except sqlite3.IntegrityError:
        print("Erro: o ID do usuário não existe.")
    finally:
        conexao.close()


def listar_emprestimos():
    conexao = conectar()
    emprestimos = conexao.execute("""
        SELECT emprestimos.id, usuarios.nome, emprestimos.data
        FROM emprestimos
        INNER JOIN usuarios ON usuarios.id = emprestimos.usuario_id
        ORDER BY emprestimos.id
    """).fetchall()
    conexao.close()

    print("\n--- Empréstimos ---")
    if len(emprestimos) == 0:
        print("Nenhum empréstimo cadastrado.")
    else:
        for emprestimo in emprestimos:
            print(
                f"ID: {emprestimo[0]} | Usuário: {emprestimo[1]} | "
                f"Data: {emprestimo[2]}"
            )


def cadastrar_emprestimo_livro():
    listar_emprestimos()
    emprestimo_id = ler_inteiro("ID do empréstimo: ")

    listar_livros()
    livro_id = ler_inteiro("ID do livro: ")

    resposta = input(
        "Data de devolução (dd/mm/aaaa) ou Enter se ainda não devolveu: "
    )

    data_devolucao = None
    if resposta != "":
        try:
            datetime.strptime(resposta, "%d/%m/%Y")
            data_devolucao = resposta
        except ValueError:
            print("Data de devolução inválida!")
            return

    conexao = conectar()
    try:
        conexao.execute("""
            INSERT INTO emprestimos_livros
            (emprestimo_id, livro_id, data_devolucao)
            VALUES (?, ?, ?)
        """, (emprestimo_id, livro_id, data_devolucao))
        conexao.commit()
        print("Livro relacionado ao empréstimo com sucesso!")
    except sqlite3.IntegrityError:
        print(
            "Erro: verifique se o empréstimo e o livro existem "
            "ou se a relação já foi cadastrada."
        )
    finally:
        conexao.close()


def listar_emprestimos_livros():
    conexao = conectar()
    itens = conexao.execute("""
        SELECT emprestimos_livros.emprestimo_id,
               usuarios.nome,
               livros.titulo,
               emprestimos_livros.data_devolucao
        FROM emprestimos_livros
        INNER JOIN emprestimos
            ON emprestimos.id = emprestimos_livros.emprestimo_id
        INNER JOIN usuarios
            ON usuarios.id = emprestimos.usuario_id
        INNER JOIN livros
            ON livros.id = emprestimos_livros.livro_id
        ORDER BY emprestimos_livros.emprestimo_id
    """).fetchall()
    conexao.close()

    print("\n--- Empréstimos e livros ---")
    if len(itens) == 0:
        print("Nenhum livro relacionado a empréstimo.")
    else:
        for item in itens:
            devolucao = item[3] if item[3] is not None else "Em aberto"
            print(
                f"Empréstimo: {item[0]} | Usuário: {item[1]} | "
                f"Livro: {item[2]} | Devolução: {devolucao}"
            )
