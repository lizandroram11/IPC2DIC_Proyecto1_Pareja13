from core.modelos.contenedor import Contenedor

class GestorContenedores:
    def __init__(self, gestor_vms):
        # gestor_vms es una instancia de GestorVMs
        self.vms = gestor_vms


    def buscar_contenedor(self, vm_id, cont_id):
        vm = self.vms.buscar(vm_id)
        if vm is None:
            return None

        nodo = vm.contenedores.primero
        while nodo:
            if nodo.valor.id == cont_id:
                return nodo.valor
            nodo = nodo.siguiente
        return None

    # 1. Desplegar contenedor en VM
    def desplegar_contenedor(self, vm_id, nombre, imagen, cpu, ram, puerto):
        vm = self.vms.buscar(vm_id)
        if vm is None:
            print("Error: VM no encontrada.")
            return False

        # Validar recursos de la VM
        if vm.cpu + cpu > vm.centro.cpu_total or vm.ram + ram > vm.centro.ram_total:
            print("Error: La VM no tiene recursos suficientes.")
            return False

        # Crear contenedor
        cont_id = f"CNT{len(vm.contenedores)+1:03d}"
        cont = Contenedor(cont_id, nombre, imagen, cpu, ram, puerto)

        # Insertar en la lista de contenedores
        vm.contenedores.insertar(cont)

        # Actualizar recursos usados de la VM
        vm.cpu += cpu
        vm.ram += ram

        print(f"Contenedor {cont_id} desplegado en VM {vm_id} exitosamente.")
        return True

    # 2. Listar contenedores de una VM
    def listar_contenedores(self, vm_id):
        vm = self.vms.buscar(vm_id)
        if vm is None:
            print("Error: VM no encontrada.")
            return

        print(f"\n=== Contenedores en VM {vm_id} ===")
        nodo = vm.contenedores.primero
        if nodo is None:
            print("No hay contenedores en esta VM.")
            return

        while nodo:
            c = nodo.valor
            print(f"Contenedor: {c.id} - {c.nombre} ({c.imagen}) - Puerto: {c.puerto}")
            print(f"Estado: {c.estado}")
            print(f"CPU: {c.cpu}% | RAM: {c.ram} MB\n")
            nodo = nodo.siguiente

    
    def cambiar_estado_contenedor(self, vm_id, cont_id, nuevo_estado):
        cont = self.buscar_contenedor(vm_id, cont_id)
        if cont is None:
            print("Error: Contenedor no encontrado.")
            return False

       
        if cont.estado == "Stopped" and nuevo_estado == "Paused":
            print("Error: No se puede pausar un contenedor detenido.")
            return False

        cont.estado = nuevo_estado
        print(f"Estado del contenedor {cont_id} cambiado a {nuevo_estado}.")
        return True


    def eliminar_contenedor(self, vm_id, cont_id):
        vm = self.vms.buscar(vm_id)
        if vm is None:
            print("Error: VM no encontrada.")
            return False

        actual = vm.contenedores.primero
        anterior = None
        while actual:
            if actual.valor.id == cont_id:
                cont = actual.valor
                # Liberar recursos
                vm.cpu -= cont.cpu
                vm.ram -= cont.ram

                # Eliminar de la lista
                if anterior is None:
                    vm.contenedores.primero = actual.siguiente
                else:
                    anterior.siguiente = actual.siguiente

                print(f"Contenedor {cont_id} eliminado de VM {vm_id}.")
                return True
            anterior = actual
            actual = actual.siguiente

        print("Error: Contenedor no encontrado.")
        return False
    
