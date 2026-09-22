class Cliente:
    def __init__(self, nome, email, telefone):
        self.nome = nome
        self.email = email
        self.telefone = telefone

    def __str__(self):
        return f"Cliente: {self.nome}, Email: {self.email}, Telefone: {self.telefone}"