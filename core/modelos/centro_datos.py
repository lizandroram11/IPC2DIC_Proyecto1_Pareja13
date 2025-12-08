from core.estructuras.lista_doble import ListaDoble

class CentroDatos:
    def __init__(self, id, nombre, pais, ciudad, cpu, ram, almacenamiento):
        self.id = id
        self.nombre = nombre
        self.pais = pais
        self.ciudad = ciudad

        self.cpu_total = cpu
        self.ram_total = ram
        self.alm_total = almacenamiento

        self.cpu_usado = 0
        self.ram_usado = 0
        self.alm_usado = 0

        self.vms = ListaDoble()