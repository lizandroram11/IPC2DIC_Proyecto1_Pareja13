from core.gestores.gestor_centros import GestorCentros
from core.gestores.gestor_vms import GestorVMs
from core.gestores.gestor_contenedores import GestorContenedores
from core.gestores.gestor_solicitudes import GestorSolicitudes
from core.report.generador_xml import GeneradorXML
from core.xml.lector_xml import LectorXML
from core.report.gestor_reportes import GestorReportes
from core.estructuras.pila import Pila
from core.modelos.solicitud import Solicitud  # <-- IMPORTANTE


class CloudSyncApp:
    def __init__(self):

        # Inicializar gestores
        self.centros = GestorCentros()
        self.vms = GestorVMs(self.centros)
        self.contenedores = GestorContenedores(self.vms)
        self.solicitudes = GestorSolicitudes()

        # Conectar gestores entre sí
        self.solicitudes.conectar_gestores(self.centros, self.vms)

        # Lector XML
        self.lector = LectorXML(
            self.centros,
            self.vms,
            self.contenedores,
            self.solicitudes
        )

        # Gestor de Reportes
        self.reportes = GestorReportes(
            self.centros,
            self.vms,
            self.contenedores,
            self.solicitudes
        )

        # Historial de operaciones (Pila)
        self.historial = Pila()

    # ============================
    # MENÚ PRINCIPAL
    # ============================
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

            elif opcion == "6":
                self.menu_reportes()

            elif opcion == "7":
                # Pedir nombre del archivo al usuario
                nombre = input("Ingrese el nombre del archivo XML de salida (sin extensión): ").strip()
                if not nombre:
                    nombre = "salida"
                gen = GeneradorXML(self.centros, self.vms, self.contenedores, self.solicitudes)
                gen.generar_xml(nombre + ".xml")

            elif opcion == "8":
                self.menu_historial()

            elif opcion == "9":
                print("Saliendo del sistema...")
                break

            else:
                print("Opción inválida")

    # ============================
    # CARGAR XML
    # ============================
    def menu_cargar_xml(self):
        print("\n=== CARGAR ARCHIVO XML ===")
        ruta = input("Ingresa la ruta del archivo XML: ")
        self.lector.cargar_archivo(ruta)

    # ============================
    # CENTROS DE DATOS
    # ============================
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

    # ============================
    # MÁQUINAS VIRTUALES
    # ============================
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
            self.historial.push(f"Migración: VM {vm_id} de {origen} a {destino}")
        else:
            print("No se pudo migrar la VM")

    # ============================
    # CONTENEDORES
    # ============================
    def menu_contenedores(self):
        while True:
            print("\n=== GESTIÓN DE CONTENEDORES ===")
            print("1. Crear contenedor")
            print("2. Listar contenedores de una VM")
            print("3. Eliminar contenedor")
            print("4. Volver")

            sub = input("Selecciona una opción: ")

            if sub == "1":
                from core.modelos.contenedor import Contenedor
                vm_id = input("ID de la VM: ")
                id_cont = input("ID del contenedor: ")
                nombre = input("Nombre del contenedor: ")
                imagen = input("Imagen (ej: python:3.10): ")
                cpu = int(input("CPU del contenedor: "))
                ram = int(input("RAM del contenedor: "))
                puerto = int(input("Puerto: "))

                cont = Contenedor(id_cont, nombre, imagen, cpu, ram, puerto)
                ok = self.contenedores.agregar_contenedor(cont, vm_id)
                if ok:
                    print(f"Contenedor {id_cont} creado en VM {vm_id}")
                    self.historial.push(f"Contenedor {id_cont} creado en VM {vm_id}")
                else:
                    print("No se pudo crear el contenedor (VM no encontrada)")
                input("Presiona Enter para continuar...")

            elif sub == "2":
                vm_id = input("ID de la VM: ")
                self.contenedores.listar_contenedores(vm_id)
                input("Presiona Enter para continuar...")

            elif sub == "3":
                vm_id = input("ID de la VM: ")
                id_cont = input("ID del contenedor a eliminar: ")
                self.contenedores.eliminar_contenedor(vm_id, id_cont)
                self.historial.push(f"Contenedor {id_cont} eliminado de VM {vm_id}")
                input("Presiona Enter para continuar...")

            elif sub == "4":
                break
            else:
                print("Opción inválida")
                input("Presiona Enter para continuar...")

    # ============================
    # SOLICITUDES
    # ============================
    def menu_solicitudes(self):
        while True:
            print("\n=== GESTIÓN DE SOLICITUDES ===")
            print("1. Agregar nueva solicitud")
            print("2. Listar solicitudes en cola")
            print("3. Procesar N solicitudes")
            print("4. Volver")

            opcion = input("Selecciona una opción: ")

            if opcion == "1":
                id = input("ID de la solicitud: ")
                cliente = input("Cliente: ")
                tipo = input("Tipo (deploy/backup): ").strip().lower()

                # Normalizar a lo que espera GestorSolicitudes: "Deploy" / "Backup"
                if tipo == "deploy":
                    tipo = "Deploy"
                elif tipo == "backup":
                    tipo = "Backup"
                else:
                    print("Tipo no válido, usando 'Deploy' por defecto")
                    tipo = "Deploy"

                prioridad = int(input("Prioridad (1-5): "))
                cpu = int(input("CPU requerida: "))
                ram = int(input("RAM requerida: "))
                alm = int(input("Almacenamiento requerido: "))
                tiempo = int(input("Tiempo estimado: "))

                solicitud = Solicitud(id, cliente, tipo, prioridad, cpu, ram, alm, tiempo)
                self.solicitudes.agregar(solicitud)
                self.historial.push(f"Solicitud {id} agregada (cliente: {cliente}, tipo: {tipo})")
                print("✓ Solicitud agregada exitosamente")

            elif opcion == "2":
                self.solicitudes.listar()
                input("Presiona Enter para continuar...")

            elif opcion == "3":
                cantidad = int(input("¿Cuántas solicitudes deseas procesar?: "))
                procesadas, completadas, fallidas = self.solicitudes.procesar_n(cantidad)
                self.historial.push(f"Procesadas {procesadas}, completadas {completadas}, fallidas {fallidas}")
                print(f"✓ Procesadas: {procesadas}, Completadas: {completadas}, Fallidas: {fallidas}")
                input("Presiona Enter para continuar...")

            elif opcion == "4":
                break
            else:
                print("Opción inválida")

    # ============================
    # REPORTES GRAPHVIZ
    # ============================
    def menu_reportes(self):
        print("\n=== REPORTES GRAPHVIZ ===")
        print("1. Reporte de Centros de Datos")
        print("2. Reporte de VMs por Centro")
        print("3. Reporte de Contenedores por VM")
        print("4. Reporte de Solicitudes")
        print("5. Volver")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            self.reportes.reporte_centros()

        elif opcion == "2":
            self.reportes.reporte_vms_por_centro()

        elif opcion == "3":
            self.reportes.reporte_contenedores_por_vm()

        elif opcion == "4":
            self.reportes.reporte_solicitudes()

    # ============================
    # HISTORIAL
    # ============================
    def menu_historial(self):
        print("\n=== HISTORIAL DE OPERACIONES ===")
        self.historial.mostrar()
        input("Presiona Enter para continuar...")


# Ejecución del programa
if __name__ == "__main__":
    app = CloudSyncApp()
    app.iniciar()