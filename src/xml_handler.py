import xml.etree.ElementTree as ET

# ===== Importar nodos =====
from nodos.nodo_centro import NodoCentro
from nodos.nodo_vm import NodoVM
from nodos.nodo_contenedor import NodoContenedor
from nodos.nodo_solicitud import NodoSolicitud
from nodos.nodo_instruccion import NodoInstruccion

# ===== Importar listas =====
from listas.lista_doble import ListaDoble
from listas.lista_simple import ListaSimple
from listas.lista_circular import ListaCircular
from listas.cola_prioridad import ColaPrioridad


class XMLHandler:
    """
    Clase responsable de cargar y procesar archivos XML.
    Guarda datos en listas enlazadas propias.
    """

    def __init__(self):
        # Estructuras principales
        self.centros = ListaDoble()        # lista doble de centros
        self.vms = ListaSimple()           # lista simple global de VMs
        self.solicitudes = ColaPrioridad() # cola de prioridad
        self.instrucciones = ListaSimple() # lista instrucciones


    # =============================================================
    # MÉTODO PRINCIPAL
    # =============================================================
    def cargar_archivo(self, ruta):
        """
        Abre el XML, valida y procesa todas las secciones del archivo.
        """
        try:
            tree = ET.parse(ruta)
            root = tree.getroot()

            if root.tag != "cloudSync":
                print("ERROR: archivo XML inválido. Falta etiqueta raíz <cloudSync>")
                return False

            self.leer_centros(root)
            self.leer_vms(root)
            self.leer_contenedores(root)
            self.leer_solicitudes(root)
            self.leer_instrucciones(root)

            # Después de cargar TODO, vincular VMs con su centro
            self.relacionar_vms_con_centro()

            # Vincular contenedores con sus VMs
            self.relacionar_contenedores_con_vm()

            print("Archivo cargado correctamente.")
            return True

        except Exception as e:
            print("ERROR al cargar archivo XML:", e)
            return False


    # =============================================================
    # CENTROS
    # =============================================================
    def leer_centros(self, root):
        """
        Carga centros de datos desde:
        <configuracion><centrosDatos><centro>
        """
        try:
            centrosXML = root.find("configuracion").find("centrosDatos")

            for c in centrosXML.findall("centro"):
                id = c.attrib["id"]
                nombre = c.attrib["nombre"]

                cpu = int(c.find("capacidad").find("cpu").text)
                ram = int(c.find("capacidad").find("ram").text)
                almacenamiento = int(c.find("capacidad").find("almacenamiento").text)

                ciudad = c.find("ubicacion").find("ciudad").text

                nodo = NodoCentro(id, nombre, cpu, ram, almacenamiento, ciudad)
                nodo.vms = ListaSimple()  # cada centro tiene lista propia de VMs

                self.centros.insertar(nodo)

        except:
            print("No se encontraron centros.")


    # =============================================================
    # MÁQUINAS VIRTUALES
    # =============================================================
    def leer_vms(self, root):
        """
        Carga VMs desde:
        <configuracion><maquinasVirtuales><vm>
        """
        try:
            vmsXML = root.find("configuracion").find("maquinasVirtuales")

            for vm in vmsXML.findall("vm"):
                id = vm.attrib["id"]
                centroAsignado = vm.attrib["centroAsignado"]
                so = vm.find("sistemaOperativo").text

                cpu = int(vm.find("recursos").find("cpu").text)
                ram = int(vm.find("recursos").find("ram").text)
                almacenamiento = int(vm.find("recursos").find("almacenamiento").text)

                ip = vm.find("ip").text

                nodo = NodoVM(id, so, cpu, ram, almacenamiento, ip, centroAsignado)
                nodo.contenedores = ListaSimple()  # cada VM tiene lista propia de contenedores

                self.vms.insertar(nodo)

        except:
            print("No se encontraron VMs.")


    # =============================================================
    # CONTENEDORES
    # =============================================================
    def leer_contenedores(self, root):
        """
        Carga contenedores anidados dentro de cada VM
        """
        try:
            vmsXML = root.find("configuracion").find("maquinasVirtuales")

            for vm in vmsXML.findall("vm"):
                
                vmId = vm.attrib["id"]

                contenedoresXML = vm.find("contenedores")
                if contenedoresXML is None:
                    continue

                for c in contenedoresXML.findall("contenedor"):
                    
                    id = c.attrib["id"]
                    nombre = c.find("nombre").text
                    imagen = c.find("imagen").text
                    cpu = int(c.find("recursos").find("cpu").text)
                    ram = int(c.find("recursos").find("ram").text)
                    puerto = int(c.find("puerto").text)

                    nodo = NodoContenedor(id, nombre, imagen, cpu, ram, puerto)

                    # Guardamos relación (VM se asignará después)
                    nodo.vmId = vmId

                    if not hasattr(self, "contenedores_temp"):
                        self.contenedores_temp = ListaSimple()

                    self.contenedores_temp.insertar(nodo)

        except:
            print("No se encontraron contenedores.")


    # =============================================================
    # SOLICITUDES
    # =============================================================
    def leer_solicitudes(self, root):
        """
        Carga solicitudes desde:
        <configuracion><solicitudes><solicitud>
        """
        try:
            solicitudesXML = root.find("configuracion").find("solicitudes")

            for s in solicitudesXML.findall("solicitud"):
                id = s.attrib["id"]
                cliente = s.find("cliente").text
                tipo = s.find("tipo").text
                prioridad = int(s.find("prioridad").text)

                cpu = int(s.find("recursos").find("cpu").text)
                ram = int(s.find("recursos").find("ram").text)
                almacenamiento = int(s.find("recursos").find("almacenamiento").text)

                tiempo = int(s.find("tiempoEstimado").text)

                nodo = NodoSolicitud(id, cliente, tipo, prioridad, cpu, ram, almacenamiento, tiempo)

                self.solicitudes.insertar(nodo)

        except:
            print("No se encontraron solicitudes.")


    # =============================================================
    # INSTRUCCIONES
    # =============================================================
    def leer_instrucciones(self, root):
        """
        Carga instrucciones desde:
        <instrucciones><instruccion>
        """
        try:
            instruccionesXML = root.find("instrucciones")

            for inst in instruccionesXML.findall("instruccion"):
                tipo = inst.attrib["tipo"]
                parametros = inst.text
                nodo = NodoInstruccion(tipo, parametros)
                self.instrucciones.insertar(nodo)

        except:
            print("No se encontraron instrucciones.")


    # =============================================================
    # RELACIONES ENTRE ESTRUCTURAS
    # =============================================================
    def relacionar_vms_con_centro(self):
        """
        Después de cargar VMs y centros,
        meter cada VM en su centro correspondiente.
        """

        aux = self.vms.primero
        while aux is not None:
            vm = aux
            centro = self.centros.buscar(vm.centroAsignado)
            if centro is not None:
                centro.vms.insertar(vm)
            aux = aux.siguiente


    def relacionar_contenedores_con_vm(self):
        """
        Vincular contenedores con su VM correspondiente.
        """
        if not hasattr(self, "contenedores_temp"):
            return

        aux = self.contenedores_temp.primero
        while aux is not None:
            c = aux
            vm = self.vms.buscar(c.vmId)
            if vm is not None:
                vm.contenedores.insertar(c)
            aux = aux.siguiente
