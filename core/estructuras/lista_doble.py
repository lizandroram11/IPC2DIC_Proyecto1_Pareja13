from .nodo_doble import NodoDoble

class ListaDoble:
    def __init__(self):
        self.primero = None
        self.ultimo = None

    def insertar(self, valor):
        nuevo = NodoDoble(valor)
        if self.primero is None:
            self.primero = nuevo
            self.ultimo = nuevo
        else:
            self.ultimo.siguiente = nuevo
            nuevo.anterior = self.ultimo
            self.ultimo = nuevo

    def buscar(self, id):
        actual = self.primero
        while actual:
            if actual.valor.id == id:
                return actual.valor
            actual = actual.siguiente
        return None