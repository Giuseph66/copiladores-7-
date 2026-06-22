import token_types as TT
from token_types import Token


class Lexer:
    def __init__(self, codigo_fonte):
        self.codigo = codigo_fonte
        self.pos = 0
        self.linha = 1
        self.tokens = []
        self.erros = []

    def _fim(self):
        return self.pos >= len(self.codigo)

    def _atual(self):
        if self._fim():
            return ""
        return self.codigo[self.pos]

    def _proximo(self):
        if self.pos + 1 >= len(self.codigo):
            return ""
        return self.codigo[self.pos + 1]

    def _avancar(self):
        caractere = self.codigo[self.pos]
        self.pos += 1
        return caractere

    def tokenizar(self):
        while not self._fim():
            caractere = self._atual()

            if caractere in " \t\r":
                self._avancar()
                continue

            if caractere == "\n":
                self._avancar()
                self.linha += 1
                continue

            if caractere == "/" and self._proximo() == "/":
                self._consumir_comentario()
                continue

            if caractere.isdigit():
                self._ler_numero()
                continue

            if caractere.isalpha() or caractere == "_":
                self._ler_identificador()
                continue

            if self._ler_simbolo():
                continue

            self.erros.append(
                f"Erro léxico na linha {self.linha}: caractere inválido '{caractere}'"
            )
            self._avancar()

        self.tokens.append(Token(TT.EOF, "", self.linha))
        return self.tokens

    def _consumir_comentario(self):
        while not self._fim() and self._atual() != "\n":
            self._avancar()

    def _ler_numero(self):
        inicio_linha = self.linha
        digitos = ""

        while not self._fim() and self._atual().isdigit():
            digitos += self._avancar()

        if self._atual() == "." and self._proximo().isdigit():
            digitos += self._avancar()
            while not self._fim() and self._atual().isdigit():
                digitos += self._avancar()
            self.tokens.append(Token(TT.REAL, digitos, inicio_linha))
        else:
            self.tokens.append(Token(TT.INT, digitos, inicio_linha))

    def _ler_identificador(self):
        inicio_linha = self.linha
        texto = ""
        while not self._fim() and (self._atual().isalnum() or self._atual() == "_"):
            texto += self._avancar()

        tipo = TT.PALAVRAS_RESERVADAS.get(texto, TT.ID)
        self.tokens.append(Token(tipo, texto, inicio_linha))

    def _ler_simbolo(self):
        caractere = self._atual()
        simbolos = {
            "+": TT.PLUS,
            "-": TT.MINUS,
            "*": TT.TIMES,
            "/": TT.DIV,
            "(": TT.LPAREN,
            ")": TT.RPAREN,
            "=": TT.ASSIGN,
            ";": TT.SEMICOLON,
        }
        if caractere in simbolos:
            self.tokens.append(Token(simbolos[caractere], caractere, self.linha))
            self._avancar()
            return True
        return False
