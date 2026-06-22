class Program:
    def __init__(self, comandos):
        self.comandos = comandos

    def to_str(self):
        linhas = ["Programa"]
        for comando in self.comandos:
            linhas.append(" " + comando.to_str())
        return "\n".join(linhas)


class Declaration:
    def __init__(self, nome, expressao):
        self.nome = nome
        self.expressao = expressao

    def to_str(self):
        return f"Decl: {self.nome} = {self.expressao.to_str()}"


class PrintStatement:
    def __init__(self, expressao):
        self.expressao = expressao

    def to_str(self):
        return f"Print: {self.expressao.to_str()}"


class BinaryExpression:
    def __init__(self, esquerda, operador, direita):
        self.esquerda = esquerda
        self.operador = operador
        self.direita = direita

    def to_str(self):
        return f"({self.esquerda.to_str()} {self.operador} {self.direita.to_str()})"


class NumberLiteral:

    def __init__(self, valor):
        self.valor = valor

    def to_str(self):
        return self.valor


class Identifier:

    def __init__(self, nome):
        self.nome = nome

    def to_str(self):
        return self.nome
