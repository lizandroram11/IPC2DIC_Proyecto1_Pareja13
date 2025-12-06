class ColaPrioridad:
    """
    Implementación de una cola de prioridad SIN listas nativas.
    Se inserta ordenado de mayor a menor prioridad.
    """
    def __init__(self):
        self.primero = None
    
    def insertar(self, nodo):
        """
        Inserta el nodo manteniendo el orden por prioridad.
        Mayor prioridad = más arriba en la lista.
        """
        # caso: cola vacía
        if self.primero is None:
            self.primero = nodo
            return
        
        # caso: insertar como primero
        if nodo.prioridad > self.primero.prioridad:
            nodo.siguiente = self.primero
            self.primero = nodo
            return
        
        # recorrer buscando lugar correcto
        aux = self.primero
        while aux.siguiente is not None and aux.siguiente.prioridad >= nodo.prioridad:
            aux = aux.siguiente
        
        # insertar
        nodo.siguiente = aux.siguiente
        aux.siguiente = nodo
    
    def extraer(self):
        """
        Extrae el elemento con mayor prioridad (primer nodo).
        """
        if self.primero is None:
            return None
        
        nodo = self.primero
        self.primero = self.primero.siguiente
        nodo.siguiente = None
        return nodo
