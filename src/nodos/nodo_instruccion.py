class NodoInstruccion:
    """
    Nodo para almacenar instrucciones leídas desde el XML.
    Ejemplo: crearVM, migrarVM, procesarSolicitudes, etc.
    """
    def __init__(self, tipo, parametros):
        # Tipo de instrucción (string)
        self.tipo = tipo
        
        # Parámetros asociados (se almacenan como texto o estructura propia)
        self.parametros = parametros
        
        # Puntero siguiente para lista simple
        self.siguiente = None
