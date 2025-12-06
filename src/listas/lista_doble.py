class ListaDoble:
    """
    Implementación de una lista doblemente enlazada.
    Útil para:
    - Centros de datos
    - Solicitudes (cuando necesitemos recorrer hacia atrás)
    """
    def __init__(self):
        self.primero = None
    
    def insertar(self, nodo):
        """
        Inserta un nodo al final de la lista doble.
        """
        if self.primero is None:
            self.primero = nodo
        else:
            aux = self.primero
            while aux.siguiente is not None:
                aux = aux.siguiente
            aux.siguiente = nodo
            nodo.anterior = aux
    
    def buscar(self, id):
        """
        Busca un nodo por ID recorriendo la lista doble.
        """
        aux = self.primero
        while aux is not None:
            if aux.id == id:
                return aux
            aux = aux.siguiente
        return None
