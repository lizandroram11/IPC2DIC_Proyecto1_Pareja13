from .nodo_simple import NodoSimple

class ColaPrioridad:
    def __init__(self):
        self.primero = None

    def insertar(self, solicitud):
        nuevo = NodoSimple(solicitud)

        if self.primero is None:
            self.primero = nuevo
            return

        if solicitud.prioridad > self.primero.valor.prioridad:
            nuevo.siguiente = self.primero
            self.primero = nuevo
            return

        actual = self.primero
        while actual.siguiente and actual.siguiente.valor.prioridad >= solicitud.prioridad:
            actual = actual.siguiente

        nuevo.siguiente = actual.siguiente
        actual.siguiente = nuevo

    def extraer(self):
        if self.primero is None:
            return None
        valor = self.primero.valor
        self.primero = self.primero.siguiente
        return valor