from .nodo_circular import NodoCircular

class ListaCircular:
    def __init__(self):
        self.primero = None

    def insertar(self, valor):
        nuevo = NodoCircular(valor)
        if self.primero is None:
            self.primero = nuevo
        else:
            actual = self.primero
            while actual.siguiente != self.primero:
                actual = actual.siguiente
            actual.siguiente = nuevo
            nuevo.siguiente = self.primero

    def buscar(self, id):
        if self.primero is None:
            return None

        actual = self.primero
        while True:
            if actual.valor.id == id:
                return actual.valor
            actual = actual.siguiente
            if actual == self.primero:
                break
        return None