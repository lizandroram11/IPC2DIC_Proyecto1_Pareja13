from .nodo_doble import NodoDoble

class ListaDoble:
    def __init__(self):
        self.primero = None
        self.ultimo = None

   #Insertar al Final
    def insertar(self, valor):
        nuevo = NodoDoble(valor)

        if self.primero is None:
            self.primero = nuevo
            self.ultimo = nuevo
            return

        self.ultimo.siguiente = nuevo
        nuevo.anterior = self.ultimo
        self.ultimo = nuevo

   #Buscar por ID
    def buscar(self, id):
        actual = self.primero
        while actual:
            if actual.valor.id == id:
                return actual.valor
            actual = actual.siguiente
        return None

    #Eliminar por ID
    def eliminar(self, id):
        actual = self.primero

        while actual:
            if actual.valor.id == id:

                # Caso: eliminar primero
                if actual == self.primero:
                    self.primero = actual.siguiente
                    if self.primero:
                        self.primero.anterior = None
                    else:
                        self.ultimo = None
                    return True

                # Caso: eliminar último
                if actual == self.ultimo:
                    self.ultimo = actual.anterior
                    self.ultimo.siguiente = None
                    return True

                # Caso general
                actual.anterior.siguiente = actual.siguiente
                actual.siguiente.anterior = actual.anterior
                return True

            actual = actual.siguiente

        return False

    # Recorrer
   
    def recorrer(self):
        actual = self.primero
        while actual:
            yield actual.valor
            actual = actual.siguiente

   #Verificar si esta vacia
    def esta_vacia(self):
        return self.primero is None