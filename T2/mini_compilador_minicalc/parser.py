import token_types as TT
import ast_nodes

class ErroSintatico(Exception):
    pass


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.erros = []

    def _atual(self):
        return self.tokens[self.pos]

    def _avancar(self):
        token = self.tokens[self.pos]
        if self._atual().tipo != TT.EOF:
            self.pos += 1
        return token

    def _verifica(self, tipo):
        return self._atual().tipo == tipo

    def _consumir(self, tipo, mensagem):
        if self._verifica(tipo):
            return self._avancar()
        raise ErroSintatico(
            f"Erro sintático na linha {self._atual().linha}: {mensagem}"
        )

    def parse(self):
        comandos = []
        while not self._verifica(TT.EOF):
            try:
                comandos.append(self._stmt())
            except ErroSintatico as erro:
                self.erros.append(str(erro))
                self._modo_panico()
        return ast_nodes.Program(comandos)

    def _modo_panico(self):
        while not self._verifica(TT.EOF):
            if self._verifica(TT.SEMICOLON):
                self._avancar()
                return
            if self._verifica(TT.LET) or self._verifica(TT.PRINT):
                return
            self._avancar()

    def _stmt(self):
        if self._verifica(TT.LET):
            return self._decl()
        if self._verifica(TT.PRINT):
            return self._print_stmt()
        raise ErroSintatico(
            f"Erro sintático na linha {self._atual().linha}: "
            f"comando inválido, esperado 'let' ou 'print'"
        )

    def _decl(self):
        self._consumir(TT.LET, "esperado 'let'")
        nome = self._consumir(TT.ID, "esperado nome de variável após 'let'")
        self._consumir(TT.ASSIGN, "esperado '=' na declaração")
        expressao = self._expr()
        self._consumir(TT.SEMICOLON, "esperado ';' ao final da declaração")
        return ast_nodes.Declaration(nome.lexema, expressao)

    def _print_stmt(self):
        self._consumir(TT.PRINT, "esperado 'print'")
        expressao = self._expr()
        self._consumir(TT.SEMICOLON, "esperado ';' ao final do print")
        return ast_nodes.PrintStatement(expressao)

    def _expr(self):
        no = self._term()
        while self._verifica(TT.PLUS) or self._verifica(TT.MINUS):
            operador = self._avancar().lexema
            direita = self._term()
            no = ast_nodes.BinaryExpression(no, operador, direita)
        return no

    def _term(self):
        no = self._factor()
        while self._verifica(TT.TIMES) or self._verifica(TT.DIV):
            operador = self._avancar().lexema
            direita = self._factor()
            no = ast_nodes.BinaryExpression(no, operador, direita)
        return no

    def _factor(self):
        token = self._atual()

        if token.tipo == TT.INT or token.tipo == TT.REAL:
            self._avancar()
            return ast_nodes.NumberLiteral(token.lexema)

        if token.tipo == TT.ID:
            self._avancar()
            return ast_nodes.Identifier(token.lexema)

        if token.tipo == TT.LPAREN:
            self._avancar()
            expressao = self._expr()
            self._consumir(TT.RPAREN, "esperado ')' para fechar o parêntese")
            return expressao

        raise ErroSintatico(
            f"Erro sintático na linha {token.linha}: "
            f"esperado número, variável ou '(' em uma expressão"
        )
