import xml.etree.ElementTree as ET
from core.modelos.centro_datos import CentroDatos
from core.modelos.maquina_virtual import MaquinaVirtual
from core.modelos.contenedor import Contenedor
from core.modelos.solicitud import Solicitud


def safe_text(node, path, etiqueta, objeto_id):
    tag = node.find(path)
    if tag is None or tag.text is None:
        print(f"ERROR: Falta la etiqueta <{etiqueta}> en el objeto {objeto_id}")
        return None
    return tag.text.strip()


class LectorXML:
    def __init__(self, gestor_centros, gestor_vms, gestor_contenedores, gestor_solicitudes):
        # Gestores conectados desde main.py
        self.centros = gestor_centros
        self.vms = gestor_vms
        self.contenedores = gestor_contenedores
        self.solicitudes = gestor_solicitudes

    # MÉTODO PRINCIPAL: CARGAR ARCHIVO XML
    def cargar_archivo(self, ruta):

        try:
            tree = ET.parse(ruta)
            root = tree.getroot()

            print("\n=== CARGANDO ARCHIVO XML ===")

            # Orden correcto de carga
            self._cargar_centros(root)
            self._cargar_vms(root)
            self._cargar_solicitudes(root)
            self._ejecutar_instrucciones(root)

            print("\nArchivo XML cargado exitosamente\n")

        except Exception as e:
            print(f"Error al cargar el archivo XML: {e}")

   
    # CARGA DE CENTROS DE DATOS
    def _cargar_centros(self, root):

        for nodo in root.findall("./configuracion/centrosDatos/centro"):
            id = nodo.get("id")
            nombre = nodo.get("nombre")

            pais = safe_text(nodo, "ubicacion/pais", "pais", id)
            ciudad = safe_text(nodo, "ubicacion/ciudad", "ciudad", id)

            cpu = int(safe_text(nodo, "capacidad/cpu", "cpu", id))
            ram = int(safe_text(nodo, "capacidad/ram", "ram", id))
            alm = int(safe_text(nodo, "capacidad/almacenamiento", "almacenamiento", id))

            centro = CentroDatos(id, nombre, pais, ciudad, cpu, ram, alm)
            self.centros.agregar_centro(centro)

            print(f"Centro {id} cargado")

    
    # CARGA DE MÁQUINAS VIRTUALES
    def _cargar_vms(self, root):

        for nodo in root.findall("./configuracion/maquinasVirtuales/vm"):
            id = nodo.get("id")
            centro_asignado = nodo.get("centroAsignado")

            so = safe_text(nodo, "sistemaOperativo", "sistemaOperativo", id)

            cpu = int(safe_text(nodo, "recursos/cpu", "cpu", id))
            ram = int(safe_text(nodo, "recursos/ram", "ram", id))
            almacenamiento = int(safe_text(nodo, "recursos/almacenamiento", "almacenamiento", id))

            ip = safe_text(nodo, "ip", "ip", id)

            vm = MaquinaVirtual(id, so, cpu, ram, almacenamiento, ip, centro_asignado)
            self.vms.agregar_vm(vm, centro_asignado)

            print(f"VM {id} cargada en {centro_asignado}")

            # Cargar contenedores dentro de esta VM
            self._cargar_contenedores(nodo, vm)

    
    # CARGA DE CONTENEDORES
    def _cargar_contenedores(self, nodo_vm, vm):
        for nodo in nodo_vm.findall("./contenedores/contenedor"):
            id = nodo.get("id")

            nombre = safe_text(nodo, "nombre", "nombre", id)
            imagen = safe_text(nodo, "imagen", "imagen", id)

            cpu = int(safe_text(nodo, "recursos/cpu", "cpu", id))
            ram = int(safe_text(nodo, "recursos/ram", "ram", id))
            puerto = int(safe_text(nodo, "puerto", "puerto", id))

            cont = Contenedor(id, nombre, imagen, cpu, ram, puerto)
            vm.contenedores.insertar(cont)

            print(f"   Contenedor {id} agregado a VM {vm.id}")

    
    # CARGA DE SOLICITUDES
    def _cargar_solicitudes(self, root):

        for nodo in root.findall("./configuracion/solicitudes/solicitud"):
            id = nodo.get("id")

            cliente = safe_text(nodo, "cliente", "cliente", id)
            tipo = safe_text(nodo, "tipo", "tipo", id)
            prioridad = int(safe_text(nodo, "prioridad", "prioridad", id))

            cpu = int(safe_text(nodo, "recursos/cpu", "cpu", id))
            ram = int(safe_text(nodo, "recursos/ram", "ram", id))
            almacenamiento = int(safe_text(nodo, "recursos/almacenamiento", "almacenamiento", id))

            tiempo = int(safe_text(nodo, "tiempoEstimado", "tiempoEstimado", id))

            solicitud = Solicitud(id, cliente, tipo, prioridad, cpu, ram, almacenamiento, tiempo)
            self.solicitudes.agregar(solicitud)

            print(f"Solicitud {id} cargada")

    #Ejecucion de instrucciones
    def _ejecutar_instrucciones(self, root):
        print("\n=== Ejecutando Instrucciones ===")

        for nodo in root.findall("./instrucciones/instruccion"):
            tipo = nodo.get("tipo")

            if tipo == "crearVM":
                self._instruccion_crear_vm(nodo)

            elif tipo == "migrarVM":
                self._instruccion_migrar_vm(nodo)

            elif tipo == "procesarSolicitudes":
                self._instruccion_procesar_solicitudes(nodo)

   
    # INSTRUCCIÓN: CREAR VM 
    def _instruccion_crear_vm(self, nodo):
        id_vm = safe_text(nodo, "id", "id", "crearVM")
        centro = safe_text(nodo, "centro", "centro", id_vm)
        so = safe_text(nodo, "so", "so", id_vm)

        cpu = int(safe_text(nodo, "cpu", "cpu", id_vm))
        ram = int(safe_text(nodo, "ram", "ram", id_vm))
        almacenamiento = int(safe_text(nodo, "almacenamiento", "almacenamiento", id_vm))

        vm = MaquinaVirtual(id_vm, so, cpu, ram, almacenamiento, "0.0.0.0", centro)

        resultado = self.vms.crear_vm_instruccion(vm, centro)

        if resultado:
            print("VM creada exitosamente")
        else:
            print("No se pudo crear la VM (recursos insuficientes)")

   #Migrar VM
    def _instruccion_migrar_vm(self, nodo):
        vm_id = safe_text(nodo, "vmId", "vmId", "migrarVM")
        origen = safe_text(nodo, "centroOrigen", "centroOrigen", vm_id)
        destino = safe_text(nodo, "centroDestino", "centroDestino", vm_id)

        resultado = self.vms.migrar_vm(vm_id, origen, destino)

        if resultado:
            print("VM migrada exitosamente")
        else:
            print("No se pudo migrar la VM")

    #Procesar solicitudes
    def _instruccion_procesar_solicitudes(self, nodo):
        cantidad = int(safe_text(nodo, "cantidad", "cantidad", "procesarSolicitudes"))

        procesadas, completadas, fallidas = self.solicitudes.procesar_n(cantidad)

        print(f"Procesadas: {procesadas}, Completadas: {completadas}, Fallidas: {fallidas}")