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
    # OPCIONES RESTANTES (FUNCIONES VACÍAS TEMPORALMENTE)
    # ==================================================

    def menu_vms(self):
        print("Submenú VMs: por implementar")

    def menu_contenedores(self):
        print("Submenú contenedores: por implementar")

    def menu_solicitudes(self):
        print("Submenú solicitudes: por implementar")
