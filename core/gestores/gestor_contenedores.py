class GestorContenedores:
    def __init__(self, gestor_vms):
        # gestor_vms es una instancia de GestorVMs
        self.vms = gestor_vms

    def agregar_contenedor(self, contenedor, id_vm):
        """
        Agrega un contenedor a la VM con id = id_vm.
        Recorre todos los centros y sus VMs hasta encontrar la VM.
        """
        # Accedemos al gestor de centros a través del gestor de VMs
        gestor_centros = self.vms.centros
        actual_centro = gestor_centros.centros.primero

        if actual_centro is None:
            return False

        while True:
            centro = actual_centro.valor
            nodo_vm = centro.vms.primero

            while nodo_vm:
                vm = nodo_vm.valor
                if vm.id == id_vm:
                    vm.contenedores.insertar(contenedor)
                    return True
                nodo_vm = nodo_vm.siguiente

            actual_centro = actual_centro.siguiente
            if actual_centro == gestor_centros.centros.primero:
                break

        return False