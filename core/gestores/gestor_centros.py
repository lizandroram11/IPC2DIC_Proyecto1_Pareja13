# core/gestores/gestor_centros.py

from core.estructuras.lista_circular import ListaCircular

class GestorCentros:
    def __init__(self):
        self.centros = ListaCircular()

    def agregar_centro(self, centro):
        self.centros.insertar(centro)

    def buscar(self, id):
        return self.centros.buscar(id)

    def obtener_centro_con_mas_recursos(self):
        if self.centros.primero is None:
            return None

        actual = self.centros.primero
        mejor = actual.valor

        while True:
            centro = actual.valor

            libres_centro = (
                (centro.cpu_total - centro.cpu_usado) +
                (centro.ram_total - centro.ram_usado) +
                (centro.alm_total - centro.alm_usado)
            )

            libres_mejor = (
                (mejor.cpu_total - mejor.cpu_usado) +
                (mejor.ram_total - mejor.ram_usado) +
                (mejor.alm_total - mejor.alm_usado)
            )

            if libres_centro > libres_mejor:
                mejor = centro

            actual = actual.siguiente
            if actual == self.centros.primero:
                break

        return mejor