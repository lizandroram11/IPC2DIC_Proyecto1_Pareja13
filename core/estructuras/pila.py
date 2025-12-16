class Pila:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if self.items:
            return self.items.pop()
        return None

    def mostrar(self):
        print("\n=== HISTORIAL DE OPERACIONES ===")
        if not self.items:
            print("No hay operaciones registradas")
            return
        for item in reversed(self.items):
            print(item)

