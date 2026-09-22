def Horario():
    def __init__(self, data, hora):
        self.data = data
        self.hora = hora

    def __str__(self):
        return f"Data: {self.data}, Hora: {self.hora}"