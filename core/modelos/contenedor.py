#Contenedor dentro de la VM
class Contenedor:
    def __init__(self, id, nombre, imagen, cpu, ram, puerto):
        self.id = id
        self.nombre = nombre
        self.imagen = imagen
        self.cpu = cpu
        self.ram = ram
        self.puerto = puerto
        self.estado = "Running"