class ListaSimple:
    """
    Implementación de una lista simplemente enlazada.
    Útil para:
    - Contenedores
    - Máquinas virtuales
    - Instrucciones
    """
    def __init__(self):
        # Puntero al primer nodo de la lista
        self.primero = None
    
    def insertar(self, nodo):
        """
        Inserta un nuevo nodo al final de la lista.
        Recorrido hasta encontrar el último nodo.
        """
        if self.primero is None:
            self.primero = nodo
        else:
            aux = self.primero
            while aux.siguiente is not None:
                aux = aux.siguiente
            aux.siguiente = nodo
    
    def buscar(self, id):
        """
        Busca un nodo por ID.
        Retorna el nodo si lo encuentra, de lo contrario None.
        """
        aux = self.primero
        while aux is not None:
            if aux.id == id:
                return aux
            aux = aux.siguiente
        return None
    
    def eliminar(self, id):
        """
        Elimina un nodo de la lista simple.
        Se maneja el caso de eliminar el primero y nodos intermedios.
        """
        aux = self.primero
        anterior = None
        
        while aux is not None:
            if aux.id == id:
                # eliminar el primero
                if anterior is None:
                    self.primero = aux.siguiente
                else:
                    # eliminar nodo intermedio
                    anterior.siguiente = aux.siguiente
                return True
            anterior = aux
            aux = aux.siguiente
        
        return False
