class ListaCircular:
    """
    Implementación de lista circular simplemente enlazada.
    Útil para:
    - Recorridos infinitos
    - Listas rotativas
    """
    def __init__(self):
        self.primero = None
    
    def insertar(self, nodo):
        """
        Inserta un nodo preservando estructura circular.
        """
        if self.primero is None:
            self.primero = nodo
            nodo.siguiente = nodo  # apunta a sí mismo
        else:
            aux = self.primero
            while aux.siguiente != self.primero:
                aux = aux.siguiente
            aux.siguiente = nodo
            nodo.siguiente = self.primero
