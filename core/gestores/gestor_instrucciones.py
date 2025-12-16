class GestorInstrucciones:
    def __init__(self, gestor_centros, gestor_vms, gestor_solicitudes):
        self.centros = gestor_centros
        self.vms = gestor_vms
        self.solicitudes = gestor_solicitudes

    def ejecutar(self, nodo_instrucciones):
        if nodo_instrucciones is None:
            print("No hay instrucciones en el XML")
            return

        for instr in nodo_instrucciones.findall("instruccion"):
            tipo = instr.get("tipo")

            if tipo == "crearVM":
                self._crear_vm(instr)

            elif tipo == "migrarVM":
                self._migrar_vm(instr)

            elif tipo == "procesarSolicitudes":
                self._procesar_solicitudes(instr)

            elif tipo == "mostrarCentros":
                self._mostrar_centros()

            else:
                print(f"Instrucción desconocida: {tipo}")

    # --- Métodos privados para cada instrucción ---

    def _crear_vm(self, instr):
        from core.modelos.maquina_virtual import MaquinaVirtual

        vm = MaquinaVirtual(
            instr.find("id").text,
            instr.find("so").text,
            int(instr.find("cpu").text),
            int(instr.find("ram").text),
            int(instr.find("almacenamiento").text),
            "0.0.0.0",  # IP por defecto
            instr.find("centro").text
        )

        resultado = self.vms.crear_vm_instruccion(vm, vm.centro)
        if resultado:
            print(f"✓ VM {vm.id} creada exitosamente en {vm.centro}")
        else:
            print(f"✗ No se pudo crear la VM {vm.id}")

    def _migrar_vm(self, instr):
        vm_id = instr.find("vmId").text
        origen = instr.find("centroOrigen").text
        destino = instr.find("centroDestino").text

        resultado = self.vms.migrar_vm(vm_id, origen, destino)
        if resultado:
            print(f"✓ VM {vm_id} migrada exitosamente de {origen} a {destino}")
        else:
            print(f"✗ No se pudo migrar la VM {vm_id}")

    def _procesar_solicitudes(self, instr):
        cantidad = int(instr.find("cantidad").text)
        procesadas, completadas, fallidas = self.solicitudes.procesar_n(cantidad)
        print(f"✓ Procesadas: {procesadas}, Completadas: {completadas}, Fallidas: {fallidas}")

    def _mostrar_centros(self):
        actual = self.centros.centros.primero
        if actual is None:
            print("No hay centros registrados")
            return

        while True:
            centro = actual.valor
            print(f"Centro {centro.id} - {centro.nombre} ({centro.pais}, {centro.ciudad})")
            actual = actual.siguiente
            if actual == self.centros.centros.primero:
                break
