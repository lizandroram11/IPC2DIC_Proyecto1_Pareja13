from core.estructuras.lista_circular import ListaCircular

class GestorCentros:
    def __init__(self):
        # Lista circular que almacena todos los centros de datos
        self.centros = ListaCircular()

    #Agregar centro a lista circular
    def agregar_centro(self, centro):
        """
        Inserta un centro de datos en la lista circular.
        El lector XML llama a este método por cada <centro>.
        """
        self.centros.insertar(centro)

    #Buscar centro por ID
    def buscar(self, id):
        """
        Retorna el centro cuyo ID coincida con el parámetro.
        Si no existe, retorna None.
        """
        return self.centros.buscar(id)

   #Centro con mas recursos disponibles
    def obtener_centro_con_mas_recursos(self):

        # Si no hay centros registrados
        if self.centros.primero is None:
            return None

        # Empezamos desde el primer nodo
        actual = self.centros.primero
        mejor = actual.valor  # Suponemos que el primero es el mejor

        while True:
            centro = actual.valor

            # Recursos libres del centro actual
            libres_centro = (
                (centro.cpu_total - centro.cpu_usado) +
                (centro.ram_total - centro.ram_usado) +
                (centro.alm_total - centro.alm_usado)
            )

            # Recursos libres del mejor centro encontrado hasta ahora
            libres_mejor = (
                (mejor.cpu_total - mejor.cpu_usado) +
                (mejor.ram_total - mejor.ram_usado) +
                (mejor.alm_total - mejor.alm_usado)
            )

            # Si el centro actual tiene más recursos libres, lo actualizamos
            if libres_centro > libres_mejor:
                mejor = centro

            # Avanzamos al siguiente nodo de la lista circular
            actual = actual.siguiente

            # Si regresamos al inicio, terminamos el recorrido
            if actual == self.centros.primero:
                break

        return mejor  
