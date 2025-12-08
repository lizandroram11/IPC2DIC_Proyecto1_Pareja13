# main.py

from core.gestores.gestor_centros import GestorCentros
from core.gestores.gestor_vms import GestorVMs
from core.gestores.gestor_contenedores import GestorContenedores
from core.gestores.gestor_solicitudes import GestorSolicitudes

from core.xml.lector_xml import LectorXML


class CloudSyncApp:
    def __init__(self):
        # ============================
        # Inicializar gestores
        # ============================
        self.centros = GestorCentros()
        self.vms = GestorVMs(self.centros)
        self.contenedores = GestorContenedores(self.vms)
        self.solicitudes = GestorSolicitudes()

        # Conectar gestores entre sí
        self.solicitudes.conectar_gestores(self.centros, self.vms)

        # ============================
        # Lector XML
        # ============================
        self.lector = LectorXML(
            self.centros,
            self.vms,
            self.contenedores,
            self.solicitudes
        )

    # ============================================================
    # MENÚ PRINCIPAL
    # ============================================================
    def iniciar(self):
        while True:
            print("\n=== CLOUDSYNC MANAGER - SISTEMA DE NUBE ===")
            print("1. Cargar Archivo XML")
            print("2. Gestión de Centros de Datos")
            print("3. Gestión de Máquinas Virtuales")
            print("4. Gestión de Contenedores")
            print("5. Gestión de Solicitudes")
            print("6. Reportes Graphviz")
            print("7. Generar XML de Salida")
            print("8. Historial de Operaciones")
            print("9. Salir")

            opcion = input("Selecciona una opción: ")

            if opcion == "1":
                self.menu_cargar_xml()

            elif opcion == "2":
                self.menu_centros()

            elif opcion == "3":
                self.menu_vms()

            elif opcion == "4":
                self.menu_contenedores()

            elif opcion == "5":
                self.menu_solicitudes()

            elif opcion == "9":
                print("Saliendo del sistema...")
                break

            else:
                print("Opción inválida")

    # ============================================================
    # OPCIÓN 1: CARGAR XML
    # ============================================================
    def menu_cargar_xml(self):
        print("\n=== CARGAR ARCHIVO XML ===")
        ruta = input("Ingresa la ruta del archivo XML: ")

        self.lector.cargar_archivo(ruta)

    # ============================================================
    # OPCIÓN 2: CENTROS DE DATOS
    # ============================================================
    def menu_centros(self):
        print("\n=== GESTIÓN DE CENTROS DE DATOS ===")
        print("1. Listar todos los centros")
        print("2. Buscar centro por ID")
        print("3. Ver centro con más recursos")
        print("4. Volver")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            self.listar_centros()

        elif opcion == "2":
            self.buscar_centro()

        elif opcion == "3":
            self.centro_mas_recursos()

    def listar_centros(self):
        actual = self.centros.centros.primero
        if actual is None:
            print("No hay centros registrados")
            return

        print("\n=== CENTROS DE DATOS REGISTRADOS ===")

        while True:
            c = actual.valor
            print(f"\nCentro: {c.nombre} ({c.id}) - {c.ciudad}, {c.pais}")
            print(f"CPU: {c.cpu_usado}/{c.cpu_total}")
            print(f"RAM: {c.ram_usado}/{c.ram_total}")
            print(f"Almacenamiento: {c.alm_usado}/{c.alm_total}")

            actual = actual.siguiente
            if actual == self.centros.centros.primero:
                break

    def buscar_centro(self):
        id = input("ID del centro: ")
        centro = self.centros.buscar(id)

        if centro is None:
            print("Centro no encontrado")
            return

        print(f"\nCentro encontrado: {centro.nombre} ({centro.id})")
        print(f"Ubicación: {centro.ciudad}, {centro.pais}")
        print(f"CPU: {centro.cpu_usado}/{centro.cpu_total}")
        print(f"RAM: {centro.ram_usado}/{centro.ram_total}")
        print(f"Almacenamiento: {centro.alm_usado}/{centro.alm_total}")

    def centro_mas_recursos(self):
        centro = self.centros.obtener_centro_con_mas_recursos()
        if centro is None:
            print("No hay centros registrados")
            return

        print("\n=== CENTRO CON MÁS RECURSOS ===")
        print(f"{centro.nombre} ({centro.id})")
        print(f"CPU libre: {centro.cpu_total - centro.cpu_usado}")
        print(f"RAM libre: {centro.ram_total - centro.ram_usado}")
        print(f"Almacenamiento libre: {centro.alm_total - centro.alm_usado}")

    # ============================================================
    # OPCIÓN 3: VMs
    # ============================================================
    def menu_vms(self):
        print("\n=== GESTIÓN DE MÁQUINAS VIRTUALES ===")
        print("1. Buscar VM por ID")
        print("2. Listar VMs de un centro")
        print("3. Migrar VM")
        print("4. Volver")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            self.buscar_vm()

        elif opcion == "2":
            self.listar_vms_centro()

        elif opcion == "3":
            self.migrar_vm()

    def buscar_vm(self):
        id_vm = input("ID de la VM: ")

        # Buscar en todos los centros
        actual = self.centros.centros.primero
        if actual is None:
            print("No hay centros registrados")
            return

        while True:
            nodo_vm = actual.valor.vms.primero
            while nodo_vm:
                if nodo_vm.valor.id == id_vm:
                    vm = nodo_vm.valor
                    print(f"\nVM encontrada: {vm.id}")
                    print(f"SO: {vm.so}")
                    print(f"CPU: {vm.cpu}")
                    print(f"RAM: {vm.ram}")
                    print(f"Centro: {vm.centro}")
                    return
                nodo_vm = nodo_vm.siguiente

            actual = actual.siguiente
            if actual == self.centros.centros.primero:
                break

        print("VM no encontrada")

    def listar_vms_centro(self):
        id_centro = input("ID del centro: ")
        centro = self.centros.buscar(id_centro)

        if centro is None:
            print("Centro no encontrado")
            return

        print(f"\n=== VMs en {centro.nombre} ===")

        nodo = centro.vms.primero
        if nodo is None:
            print("No hay VMs en este centro")
            return

        while nodo:
            vm = nodo.valor
            print(f"- {vm.id} ({vm.so}) CPU:{vm.cpu} RAM:{vm.ram}")
            nodo = nodo.siguiente

    def migrar_vm(self):
        vm_id = input("ID de la VM: ")
        origen = input("Centro origen: ")
        destino = input("Centro destino: ")

        if self.vms.migrar_vm(vm_id, origen, destino):
            print("VM migrada exitosamente")
        else:
            print("No se pudo migrar la VM")

    # ============================================================
    # OPCIÓN 4: CONTENEDORES
    # ============================================================
    def menu_contenedores(self):
        print("\n=== GESTIÓN DE CONTENEDORES ===")
        print("Esta sección se implementará más adelante.")

    # ============================================================
    # OPCIÓN 5: SOLICITUDES
    # ============================================================
    def menu_solicitudes(self):
        print("\n=== GESTIÓN DE SOLICITUDES ===")
        print("Esta sección se implementará más adelante.")


# ============================================================
# EJECUCIÓN DEL PROGRAMA
# ============================================================
if __name__ == "__main__":
    app = CloudSyncApp()
    app.iniciar()