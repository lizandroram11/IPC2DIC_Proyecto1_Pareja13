from .nodo_simple import NodoSimple
class ListaSimple:
    def __init__(self):
        self.primero = None

    # Insertar al final
    def insertar(self, valor):
        nuevo = NodoSimple(valor)

        if self.primero is None:
            self.primero = nuevo
            return

        actual = self.primero
        while actual.siguiente:
            actual = actual.siguiente

        actual.siguiente = nuevo

    # Buscar por ID
    def buscar(self, id):
        actual = self.primero
        while actual:
            if actual.valor.id == id:
                return actual.valor
            actual = actual.siguiente
        return None

    # Eliminar por ID
    def eliminar(self, id):
        if self.primero is None:
            return False

        # Caso especial: eliminar el primero
        if self.primero.valor.id == id:
            self.primero = self.primero.siguiente
            return True

        actual = self.primero
        while actual.siguiente:
            if actual.siguiente.valor.id == id:
                actual.siguiente = actual.siguiente.siguiente
                return True
            actual = actual.siguiente

        return False

    # Recorrer (útil para reportes)
    def recorrer(self):
        actual = self.primero
        while actual:
            yield actual.valor
            actual = actual.siguiente


    # Verificar si está vacía
    def esta_vacia(self):
        return self.primero is None