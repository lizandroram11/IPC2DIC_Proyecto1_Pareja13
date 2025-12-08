from .nodo_circular import NodoCircular

class ListaCircular:
    def __init__(self):
        self.primero = None

    #Insertar al Final
    def insertar(self, valor):
        nuevo = NodoCircular(valor)

        if self.primero is None:
            self.primero = nuevo
            return

        actual = self.primero
        while actual.siguiente != self.primero:
            actual = actual.siguiente

        actual.siguiente = nuevo
        nuevo.siguiente = self.primero

    #Buscar por ID
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

   #Eliminar por ID
    def eliminar(self, id):
        if self.primero is None:
            return False

        actual = self.primero
        anterior = None

        while True:
            if actual.valor.id == id:

                # Caso único: solo un nodo
                if actual.siguiente == actual:
                    self.primero = None
                    return True

                # Caso: eliminar el primero
                if actual == self.primero:
                    # Buscar último nodo
                    ultimo = self.primero
                    while ultimo.siguiente != self.primero:
                        ultimo = ultimo.siguiente

                    self.primero = actual.siguiente
                    ultimo.siguiente = self.primero
                    return True

                # Caso general
                anterior.siguiente = actual.siguiente
                return True

            anterior = actual
            actual = actual.siguiente

            if actual == self.primero:
                break

        return False

    #Recorrer Lista
    def recorrer(self):
        if self.primero is None:
            return

        actual = self.primero
        while True:
            yield actual.valor
            actual = actual.siguiente
            if actual == self.primero:
                break

    #Verificar si esta vacia
    def esta_vacia(self):
        return self.primero is None