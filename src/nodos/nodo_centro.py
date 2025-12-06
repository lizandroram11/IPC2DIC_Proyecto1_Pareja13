class NodoCentro:
    """
    Nodo que representa un Centro de Datos dentro del sistema.
    Cada centro puede contener una lista de máquinas virtuales (VMs).
    Se utiliza una lista doble para poder mover VMs fácilmente.
    """
    def __init__(self, id, nombre, cpu, ram, almacenamiento, ubicacion):
        # Identificador único del centro
        self.id = id
        
        # Nombre del centro (ej. "DataCenter Principal")
        self.nombre = nombre
        
        # Recursos totales del centro de datos
        self.cpu = cpu
        self.ram = ram
        self.almacenamiento = almacenamiento
        
        # Información de ubicación (pais, ciudad)
        self.ubicacion = ubicacion
        
        # LISTA DE MÁQUINAS VIRTUALES (se inicializa vacía)
        # Luego se asignará una lista doblemente enlazada
        self.vms = None
        
        # Punteros para lista doble
        self.siguiente = None
        self.anterior = None
