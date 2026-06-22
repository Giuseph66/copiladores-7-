LET = "LET"
PRINT = "PRINT"
ID = "ID"
INT = "INT"
REAL = "REAL"
PLUS = "PLUS"
MINUS = "MINUS"
TIMES = "TIMES"
DIV = "DIV"
LPAREN = "LPAREN"
RPAREN = "RPAREN"
ASSIGN = "ASSIGN"
SEMICOLON = "SEMICOLON"
EOF = "EOF"
PALAVRAS_RESERVADAS = {
    "let": LET,
    "print": PRINT,
}


class Token:
    def __init__(self, tipo, lexema, linha):
        self.tipo = tipo
        self.lexema = lexema
        self.linha = linha

    def __repr__(self):
        return f'{self.tipo}"{self.lexema}"L{self.linha}'
