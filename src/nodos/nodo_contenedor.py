class NodoContenedor:
    """
    Nodo que representa un contenedor dentro de una VM.
    Cada contenedor usa recursos y tiene un estado.
    """
    def __init__(self, id, nombre, imagen, cpu, ram, puerto):
        # Identificador del contenedor (ej. CNT001)
        self.id = id
        
        # Nombre simbólico (ej. "WebServer")
        self.nombre = nombre
        
        # Imagen utilizada (ej. nginx:latest)
        self.imagen = imagen
        
        # Recursos consumidos
        self.cpu = cpu
        self.ram = ram
        
        # Puerto asignado en la VM
        self.puerto = puerto
        
        # Estado inicial del contenedor
        self.estado = "Activo"
        
        # Puntero siguiente para lista simple
        self.siguiente = None
