class NodoVM:
    """
    Nodo que representa una Máquina Virtual.
    Cada VM contiene una lista de contenedores.
    """
    def __init__(self, id, so, cpu, ram, almacenamiento, ip, centroAsignado):
        # Identificador de la máquina virtual
        self.id = id
        
        # Sistema operativo (Ubuntu, Windows, Debian, etc.)
        self.so = so
        
        # Recursos asignados a la VM
        self.cpu = cpu
        self.ram = ram
        self.almacenamiento = almacenamiento
        
        # Dirección IP
        self.ip = ip
        
        # ID del centro de datos donde está alojada
        self.centroAsignado = centroAsignado
        
        # LISTA DE CONTENEDORES (se asignará después)
        self.contenedores = None
        
        # Puntero siguiente para lista simple
        self.siguiente = None
