from .nodo_simple import NodoSimple

class ListaSimple:
    def __init__(self):
        self.primero = None

    def insertar(self, valor):
        nuevo = NodoSimple(valor)
        if self.primero is None:
            self.primero = nuevo
        else:
            actual = self.primero
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo

    def buscar(self, id):
        actual = self.primero
        while actual:
            if actual.valor.id == id:
                return actual.valor
            actual = actual.siguiente
        return None