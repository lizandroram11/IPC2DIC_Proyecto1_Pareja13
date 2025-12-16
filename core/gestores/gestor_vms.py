from core.modelos.maquina_virtual import MaquinaVirtual


class GestorVMs:
    def __init__(self, gestor_centros):
        # Referencia al gestor de centros para acceder a los recursos
        self.centros = gestor_centros

    # Agregar VM desde el lector XML
    def agregar_vm(self, vm, id_centro):
        centro = self.centros.buscar(id_centro)
        if centro:
            centro.vms.insertar(vm)

    # Crear VM desde una instrucción <crearVM>
    def crear_vm_instruccion(self, vm, id_centro):
        centro = self.centros.buscar(id_centro)
        if centro is None:
            return False

        # Validación de recursos
        if (centro.cpu_usado + vm.cpu > centro.cpu_total or
            centro.ram_usado + vm.ram > centro.ram_total or
            centro.alm_usado + vm.almacenamiento > centro.alm_total):
            return False

        # Asignar recursos
        centro.cpu_usado += vm.cpu
        centro.ram_usado += vm.ram
        centro.alm_usado += vm.almacenamiento

        # Insertar VM
        centro.vms.insertar(vm)
        return True

    # Migrar VM entre centros
    def migrar_vm(self, vm_id, origen_id, destino_id):
        centro_origen = self.centros.buscar(origen_id)
        centro_destino = self.centros.buscar(destino_id)

        if centro_origen is None or centro_destino is None:
            return False

        # Buscar la VM dentro del centro origen
        nodo = centro_origen.vms.primero
        vm_encontrada = None

        while nodo:
            if nodo.valor.id == vm_id:
                vm_encontrada = nodo.valor
                break
            nodo = nodo.siguiente

        if vm_encontrada is None:
            return False

        # Validar recursos en el centro destino
        if (centro_destino.cpu_usado + vm_encontrada.cpu > centro_destino.cpu_total or
            centro_destino.ram_usado + vm_encontrada.ram > centro_destino.ram_total or
            centro_destino.alm_usado + vm_encontrada.almacenamiento > centro_destino.alm_total):
            return False

        # Liberar recursos del centro origen
        centro_origen.cpu_usado -= vm_encontrada.cpu
        centro_origen.ram_usado -= vm_encontrada.ram
        centro_origen.alm_usado -= vm_encontrada.almacenamiento

        # Eliminar VM del centro origen
        self._eliminar_vm_de_centro(centro_origen, vm_id)

        # Asignar recursos al centro destino
        centro_destino.cpu_usado += vm_encontrada.cpu
        centro_destino.ram_usado += vm_encontrada.ram
        centro_destino.alm_usado += vm_encontrada.almacenamiento

        # Insertar VM en el centro destino
        centro_destino.vms.insertar(vm_encontrada)
        vm_encontrada.centro = destino_id

        return True

    # Eliminar VM de un centro (ListaDoble)
    def _eliminar_vm_de_centro(self, centro, vm_id):
        actual = centro.vms.primero
        anterior = None

        while actual:
            if actual.valor.id == vm_id:

                # Caso: eliminar el primero
                if anterior is None:
                    centro.vms.primero = actual.siguiente
                else:
                    anterior.siguiente = actual.siguiente

                return  # Eliminación exitosa

            anterior = actual
            actual = actual.siguiente