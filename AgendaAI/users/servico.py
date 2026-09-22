class Servico():
    def __init__(self, nome, descricao, tempo, valor):
        self.nome = nome
        self.descricao = descricao
        self.tempo = tempo
        self.valor = valor

    def __str__(self):
        return f"Serviço: {self.nome}, Descrição: {self.descricao}, Tempo: {self.tempo}, Valor: {self.valor}"