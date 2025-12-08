from core.estructuras.lista_simple import ListaSimple

class MaquinaVirtual:
    def __init__(self, id, so, cpu, ram, almacenamiento, ip, centro):
        self.id = id
        self.so = so
        self.cpu = cpu
        self.ram = ram
        self.almacenamiento = almacenamiento
        self.ip = ip
        self.centro = centro
        self.estado = "Activa"

        self.contenedores = ListaSimple()