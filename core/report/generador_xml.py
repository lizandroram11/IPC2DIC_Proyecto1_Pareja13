import xml.etree.ElementTree as ET

class GeneradorXML:
    def __init__(self, gestor_centros, gestor_vms, gestor_contenedores, gestor_solicitudes):
        self.centros = gestor_centros
        self.vms = gestor_vms
        self.contenedores = gestor_contenedores
        self.solicitudes = gestor_solicitudes

    
    # MÉTODO PRINCIPAL
    def generar_xml(self, ruta_salida="salida.xml"):
        root = ET.Element("CloudSync")

        self._xml_centros(root)
        self._xml_vms(root)
        self._xml_solicitudes(root)

        # Crear árbol y guardar archivo
        tree = ET.ElementTree(root)
        tree.write(ruta_salida, encoding="utf-8", xml_declaration=True)

        print(f"XML generado correctamente en: {ruta_salida}")

   
    # SECCIÓN: CENTROS DE DATOS
    def _xml_centros(self, root):
        tag_centros = ET.SubElement(root, "CentrosDatos")

        actual = self.centros.centros.primero
        if actual is None:
            return

        while True:
            centro = actual.valor

            nodo_centro = ET.SubElement(tag_centros, "Centro", {
                "id": centro.id,
                "nombre": centro.nombre
            })

            ubicacion = ET.SubElement(nodo_centro, "Ubicacion")
            ET.SubElement(ubicacion, "Pais").text = centro.pais
            ET.SubElement(ubicacion, "Ciudad").text = centro.ciudad

            capacidad = ET.SubElement(nodo_centro, "Capacidad")
            ET.SubElement(capacidad, "CPU").text = str(centro.cpu_total)
            ET.SubElement(capacidad, "RAM").text = str(centro.ram_total)
            ET.SubElement(capacidad, "Almacenamiento").text = str(centro.alm_total)

            uso = ET.SubElement(nodo_centro, "UsoActual")
            ET.SubElement(uso, "CPU").text = str(centro.cpu_usado)
            ET.SubElement(uso, "RAM").text = str(centro.ram_usado)
            ET.SubElement(uso, "Almacenamiento").text = str(centro.alm_usado)

            actual = actual.siguiente
            if actual == self.centros.centros.primero:
                break

    # SECCIÓN: MÁQUINAS VIRTUALES
    def _xml_vms(self, root):
        tag_vms = ET.SubElement(root, "MaquinasVirtuales")

        actual_centro = self.centros.centros.primero
        if actual_centro is None:
            return

        while True:
            centro = actual_centro.valor

            nodo_vm = centro.vms.primero
            while nodo_vm:
                vm = nodo_vm.valor

                nodo_vm_xml = ET.SubElement(tag_vms, "VM", {
                    "id": vm.id,
                    "centroAsignado": vm.centro
                })

                ET.SubElement(nodo_vm_xml, "SO").text = vm.so

                recursos = ET.SubElement(nodo_vm_xml, "Recursos")
                ET.SubElement(recursos, "CPU").text = str(vm.cpu)
                ET.SubElement(recursos, "RAM").text = str(vm.ram)
                ET.SubElement(recursos, "Almacenamiento").text = str(vm.alm)

                ET.SubElement(nodo_vm_xml, "IP").text = vm.ip

                # Contenedores dentro de la VM
                self._xml_contenedores(nodo_vm_xml, vm)

                nodo_vm = nodo_vm.siguiente

            actual_centro = actual_centro.siguiente
            if actual_centro == self.centros.centros.primero:
                break


    # SECCIÓN: CONTENEDORES
    def _xml_contenedores(self, nodo_vm_xml, vm):
        tag_conts = ET.SubElement(nodo_vm_xml, "Contenedores")

        nodo_cont = vm.contenedores.primero
        while nodo_cont:
            cont = nodo_cont.valor

            nodo_cont_xml = ET.SubElement(tag_conts, "Contenedor", {
                "id": cont.id
            })

            ET.SubElement(nodo_cont_xml, "Nombre").text = cont.nombre
            ET.SubElement(nodo_cont_xml, "Imagen").text = cont.imagen

            recursos = ET.SubElement(nodo_cont_xml, "Recursos")
            ET.SubElement(recursos, "CPU").text = str(cont.cpu)
            ET.SubElement(recursos, "RAM").text = str(cont.ram)

            ET.SubElement(nodo_cont_xml, "Puerto").text = str(cont.puerto)

            nodo_cont = nodo_cont.siguiente

    #Seccion de Solicitudes
    def _xml_solicitudes(self, root):
        tag_solicitudes = ET.SubElement(root, "Solicitudes")

        actual = self.solicitudes.cola.primero
        if actual is None:
            return

        while actual:
            sol = actual.valor

            nodo_sol = ET.SubElement(tag_solicitudes, "Solicitud", {
                "id": sol.id
            })

            ET.SubElement(nodo_sol, "Cliente").text = sol.cliente
            ET.SubElement(nodo_sol, "Tipo").text = sol.tipo
            ET.SubElement(nodo_sol, "Prioridad").text = str(sol.prioridad)

            recursos = ET.SubElement(nodo_sol, "Recursos")
            ET.SubElement(recursos, "CPU").text = str(sol.cpu)
            ET.SubElement(recursos, "RAM").text = str(sol.ram)
            ET.SubElement(recursos, "Almacenamiento").text = str(sol.alm)

            ET.SubElement(nodo_sol, "TiempoEstimado").text = str(sol.tiempo)

            actual = actual.siguiente