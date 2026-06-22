import sys
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from lexer import Lexer
from parser import Parser


def ler_codigo_fonte(caminho):
    try:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            return arquivo.read(), caminho
    except OSError as erro:
        print(f"Não foi possível abrir o arquivo '{caminho}': {erro}")
        sys.exit(1)


def executar_compilador(codigo, origem):
    print(f"Arquivo de entrada: {origem}\n")

    lexer = Lexer(codigo)
    tokens = lexer.tokenizar()

    print("=== TOKENS RECONHECIDOS ===")
    for token in tokens:
        print(token)
    print()

    if lexer.erros:
        print("=== ERROS LÉXICOS ===")
        for erro in lexer.erros:
            print(erro)
        print()

    parser = Parser(tokens)
    arvore = parser.parse()

    print("=== ÁRVORE SINTÁTICA ===")
    print(arvore.to_str())
    print()

    if parser.erros:
        print("=== ERROS SINTÁTICOS ===")
        for erro in parser.erros:
            print(erro)
        print()

    if lexer.erros or parser.erros:
        print("Compilação finalizada com erros.")
    else:
        print("Compilação finalizada com sucesso.")


def obter_caminho_saida(caminho_arquivo):
    entrada = Path(caminho_arquivo)
    return entrada.with_name(f"{entrada.stem}_saida.txt")


def main():
    caminho_arquivo = "examples/exemplo_valido.mc"
    if len(sys.argv) >= 2:
        caminho_arquivo = sys.argv[1]

    codigo, origem = ler_codigo_fonte(caminho_arquivo)
    buffer = StringIO()

    with redirect_stdout(buffer):
        executar_compilador(codigo, origem)

    saida = buffer.getvalue()
    print(saida, end="")

    caminho_saida = obter_caminho_saida(caminho_arquivo)
    try:
        caminho_saida.write_text(saida, encoding="utf-8")
    except OSError as erro:
        print(f"Não foi possível salvar a saída em '{caminho_saida}': {erro}")
        sys.exit(1)

    print(f"\nSaída salva em: {caminho_saida}")


if __name__ == "__main__":
    main()
