class NodoSolicitud:
    """
    Nodo para la cola de prioridad de solicitudes.
    Representa una petición del sistema (Deploy, Backup, etc.).
    """
    def __init__(self, id, cliente, tipo, prioridad, cpu, ram, almacenamiento, tiempo):
        # Identificador único de la solicitud
        self.id = id
        
        # Nombre del cliente que envía la solicitud
        self.cliente = cliente
        
        # Tipo de operación (Deploy, Backup, etc.)
        self.tipo = tipo
        
        # Prioridad (valor de 1 a 10)
        self.prioridad = prioridad
        
        # Recursos necesarios para ejecutar la solicitud
        self.cpu = cpu
        self.ram = ram
        self.almacenamiento = almacenamiento
        
        # Tiempo estimado de ejecución
        self.tiempo = tiempo
        
        # Punteros para lista doble (útiles al extraer y reordenar)
        self.siguiente = None
        self.anterior = None
