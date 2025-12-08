from xml_handler import XMLHandler

class MenuPrincipal:
    """
    Clase que controla el menú de opciones del sistema.
    """

    def __init__(self):
        self.sistema = XMLHandler()


    def mostrar_menu(self):
        """
        Muestra el menú principal en pantalla.
        """
        while True:
            print("\n=======================")
            print("   CLOUDSYNC - MENÚ    ")
            print("=======================\n")
            print("1) Cargar archivo XML")
            print("2) Gestión de Centros de Datos")
            print("3) Gestión de Máquinas Virtuales")
            print("4) Gestión de Contenedores")
            print("5) Gestión de Solicitudes (Cola de Prioridad)")
            print("6) Salir")

            opcion = input("\nSeleccione una opción: ")

            if opcion == "1":
                self.menu_cargar_archivo()
            elif opcion == "2":
                self.menu_centros()
            elif opcion == "3":
                self.menu_vms()
            elif opcion == "4":
                self.menu_contenedores()
            elif opcion == "5":
                self.menu_solicitudes()
            elif opcion == "6":
                print("Saliendo del programa...")
                break
            else:
                print("Opción no válida, intente de nuevo.")


    # ==================================================
    # OPCIÓN 1: Cargar archivo
    # ==================================================
    def menu_cargar_archivo(self):
        ruta = input("Ingrese la ruta del archivo XML: ")
        self.sistema.cargar_archivo(ruta)


    # ==================================================
    # OPCIÓN 2: Centros (submenú)
    # ==================================================
    def menu_centros(self):
        while True:
            print("\n=== Gestión de Centros ===")
            print("1) Listar todos los centros")
            print("2) Buscar centro por ID")
            print("3) Ver centro con más recursos")
            print("4) Volver al menú principal")

            opcion = input("\nSeleccione una opción: ")

            if opcion == "1":
                self.listar_centros()
            elif opcion == "2":
                self.buscar_centro()
            elif opcion == "3":
                self.ver_centro_mas_recursos()
            elif opcion == "4":
                break
            else:
                print("Opción inválida.")


    # ==================================================
    # ACCIONES CENTROS
    # ==================================================
    def listar_centros(self):
        print("\n--- LISTA DE CENTROS ---")

        aux = self.sistema.centros.primero
        if aux is None:
            print("No hay centros cargados.")
            return
        
        while aux is not None:
            print(f"{aux.id} - {aux.nombre} | CPU:{aux.cpu} RAM:{aux.ram} ALM:{aux.almacenamiento}")
            aux = aux.siguiente


    def buscar_centro(self):
        id = input("Ingrese ID del centro a buscar: ")
        nodo = self.sistema.centros.buscar(id)

        if nodo is None:
            print("Centro no encontrado.")
        else:
            print(f"\nCentro encontrado:")
            print(f"ID: {nodo.id}")
            print(f"Nombre: {nodo.nombre}")
            print(f"CPU: {nodo.cpu}")
            print(f"RAM: {nodo.ram}")
            print(f"Almacenamiento: {nodo.almacenamiento}")


    def ver_centro_mas_recursos(self):
        print("\nCentro con más CPU disponible:")
        
        aux = self.sistema.centros.primero
        if aux is None:
            print("No hay centros cargados.")
            return
        
        mayor = aux
        aux = aux.siguiente

        while aux is not None:
            # Comparación simple SOLO CPU (por ahora)
            if aux.cpu > mayor.cpu:
                mayor = aux
            aux = aux.siguiente
        
        print(f"{mayor.id} - {mayor.nombre} (CPU:{mayor.cpu})")



    # ==================================================
    # OPCIÓN 3: Máquinas Virtuales
    # ==================================================
    def menu_vms(self):
        while True:
            print("\n=== Gestión de Máquinas Virtuales ===")
            print("1) Buscar VM por ID")
            print("2) Listar VMs de un centro")
            print("3) Migrar una VM entre centros")
            print("4) Volver al menú principal")

            opcion = input("\nSeleccione una opción: ")

            if opcion == "1":
                self.buscar_vm()
            elif opcion == "2":
                self.listar_vms_centro()
            elif opcion == "3":
                self.migrar_vm()
            elif opcion == "4":
                break
            else:
                print("Opción inválida.")
    

    def buscar_vm(self):
        """
        Busca una VM en la lista global por su ID
        """
        vmId = input("\nIngrese el ID de la VM: ")

        nodo = self.sistema.vms.buscar(vmId)

        if nodo is None:
            print("VM no encontrada.")
            return

        # Mostrar detalles
        print("\n--- DATOS DE LA VM ---")
        print(f"ID: {nodo.id}")
        print(f"Sistema: {nodo.so}")
        print(f"CPU: {nodo.cpu}")
        print(f"RAM: {nodo.ram}")
        print(f"ALM: {nodo.almacenamiento}")
        print(f"IP: {nodo.ip}")
        print(f"Centro asignado: {nodo.centroAsignado}")

        # Mostrar contenedores
        print("\nContenedores:")
        aux = nodo.contenedores.primero
        if aux is None:
            print("  (Sin contenedores)")
        else:
            while aux is not None:
                print(f"  {aux.id} - {aux.nombre} ({aux.imagen})")
                aux = aux.siguiente

    def listar_vms_centro(self):
        """
        Muestra todas las VMs asignadas a un centro específico
        """
        id = input("\nIngrese ID del centro: ")
        
        centro = self.sistema.centros.buscar(id)

        if centro is None:
            print("Centro no encontrado.")
            return

        print(f"\n--- VMs del centro {centro.nombre} ---")

        aux = centro.vms.primero

        if aux is None:
            print("No hay VMs registradas en este centro.")
            return

        while aux is not None:
            print(f"{aux.id} - {aux.so} | CPU:{aux.cpu} RAM:{aux.ram} ALM:{aux.almacenamiento}")
            aux = aux.siguiente


    def migrar_vm(self):
        """
        Traslada una VM de un centro a otro.
        """
        vmId = input("\nIngrese ID de la VM a migrar: ")
        vm = self.sistema.vms.buscar(vmId)

        if vm is None:
            print("VM no encontrada.")
            return

        origenId = vm.centroAsignado
        origen = self.sistema.centros.buscar(origenId)

        print(f"VM {vmId} se encuentra en el centro {origenId}")

        destinoId = input("Ingrese ID del centro destino: ")
        destino = self.sistema.centros.buscar(destinoId)

        if destino is None:
            print("Centro destino no existe.")
            return
        
        # ======== VALIDAR RECURSOS ========
        if vm.cpu > destino.cpu or vm.ram > destino.ram or vm.almacenamiento > destino.almacenamiento:
            print("ERROR: El centro destino NO tiene recursos suficientes.")
            return

        # ======== ELIMINAR VM DEL ORIGEN ========
        origen.vms.eliminar(vmId)

        # ======== INSERTAR VM EN DESTINO ========
        destino.vms.insertar(vm)

        # ======== ACTUALIZAR DATO ========
        vm.centroAsignado = destinoId

        print(f"\nVM {vmId} migrada exitosamente de {origenId} a {destinoId}")




    def menu_contenedores(self):
        print("Submenú contenedores: por implementar")

    def menu_solicitudes(self):
        print("Submenú solicitudes: por implementar")
