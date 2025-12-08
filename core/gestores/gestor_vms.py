# core/gestores/gestor_vms.py

from core.modelos.maquina_virtual import MaquinaVirtual

class GestorVMs:
    def __init__(self, gestor_centros):
        self.centros = gestor_centros

    def agregar_vm(self, vm, id_centro):
        centro = self.centros.buscar(id_centro)
        if centro:
            centro.vms.insertar(vm)

    def crear_vm_instruccion(self, vm, id_centro):
        centro = self.centros.buscar(id_centro)
        if centro is None:
            return False

        if (centro.cpu_usado + vm.cpu > centro.cpu_total or
            centro.ram_usado + vm.ram > centro.ram_total or
            centro.alm_usado + vm.almacenamiento > centro.alm_total):
            return False

        centro.cpu_usado += vm.cpu
        centro.ram_usado += vm.ram
        centro.alm_usado += vm.almacenamiento

        centro.vms.insertar(vm)
        return True

    def migrar_vm(self, vm_id, origen_id, destino_id):
        centro_origen = self.centros.buscar(origen_id)
        centro_destino = self.centros.buscar(destino_id)

        if centro_origen is None or centro_destino is None:
            return False

        nodo = centro_origen.vms.primero
        vm_encontrada = None

        while nodo:
            if nodo.valor.id == vm_id:
                vm_encontrada = nodo.valor
                break
            nodo = nodo.siguiente

        if vm_encontrada is None:
            return False

        if (centro_destino.cpu_usado + vm_encontrada.cpu > centro_destino.cpu_total or
            centro_destino.ram_usado + vm_encontrada.ram > centro_destino.ram_total or
            centro_destino.alm_usado + vm_encontrada.almacenamiento > centro_destino.alm_total):
            return False

        centro_origen.cpu_usado -= vm_encontrada.cpu
        centro_origen.ram_usado -= vm_encontrada.ram
        centro_origen.alm_usado -= vm_encontrada.almacenamiento

        self._eliminar_vm_de_centro(centro_origen, vm_id)

        centro_destino.cpu_usado += vm_encontrada.cpu
        centro_destino.ram_usado += vm_encontrada.ram
        centro_destino.alm_usado += vm_encontrada.almacenamiento

        centro_destino.vms.insertar(vm_encontrada)
        vm_encontrada.centro = destino_id

        return True

    def _eliminar_vm_de_centro(self, centro, vm_id):
        actual = centro.vms.primero

        while actual:
            if actual.valor.id == vm_id:
                if actual == centro.vms.primero:
                    centro.vms.primero = actual.siguiente
                    if centro.vms.primero:
                        centro.vms.primero.anterior = None
                elif actual == centro.vms.ultimo:
                    centro.vms.ultimo = actual.anterior
                    centro.vms.ultimo.siguiente = None
                else:
                    actual.anterior.siguiente = actual.siguiente
                    actual.siguiente.anterior = actual.anterior
                return
            actual = actual.siguiente