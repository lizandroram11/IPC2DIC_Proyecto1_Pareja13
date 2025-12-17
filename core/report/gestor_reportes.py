import graphviz

class GestorReportes:

    def __init__(self, gestor_centros, gestor_vms, gestor_contenedores, gestor_solicitudes):
        self.centros = gestor_centros
        self.vms = gestor_vms
        self.contenedores = gestor_contenedores
        self.solicitudes = gestor_solicitudes

    # Reporte Centro de datos
    def reporte_centros(self):
        grafo = graphviz.Digraph("CentrosDatos", format="png")
        grafo.attr(rankdir="LR", bgcolor="white")

        actual = self.centros.centros.primero
        if actual is None:
            print("No hay centros para graficar")
            return

        while True:
            c = actual.valor
            etiqueta = f"""
            {c.nombre}
            ID: {c.id}
            CPU: {c.cpu_usado}/{c.cpu_total}
            RAM: {c.ram_usado}/{c.ram_total}
            ALM: {c.alm_usado}/{c.alm_total}
            """
            grafo.node(c.id, etiqueta, shape="box", style="filled", fillcolor="lightblue")

            actual = actual.siguiente
            if actual == self.centros.centros.primero:
                break

        # Conexiones (lista circular)
        actual = self.centros.centros.primero
        while True:
            siguiente = actual.siguiente
            grafo.edge(actual.valor.id, siguiente.valor.id)
            actual = siguiente
            if actual == self.centros.centros.primero:
                break

        grafo.render("reporte_centros", view=True)
        print("Reporte de centros generado: reporte_centros.png")

    # Reporte VMs por centro
    def reporte_vms_por_centro(self):
        grafo = graphviz.Digraph("VMsPorCentro", format="png")
        grafo.attr(rankdir="LR", bgcolor="white")

        actual_centro = self.centros.centros.primero
        if actual_centro is None:
            print("No hay centros para graficar")
            return

        while True:
            centro = actual_centro.valor
            etiqueta_centro = f"""
            {centro.nombre}
            ID: {centro.id}
            CPU: {centro.cpu_usado}/{centro.cpu_total}
            RAM: {centro.ram_usado}/{centro.ram_total}
            ALM: {centro.alm_usado}/{centro.alm_total}
            """
            grafo.node(centro.id, etiqueta_centro, shape="box", style="filled", fillcolor="lightblue")

            nodo_vm = centro.vms.primero
            while nodo_vm:
                vm = nodo_vm.valor
                etiqueta_vm = f"""
                VM: {vm.id}
                SO: {vm.so}
                CPU: {vm.cpu}
                RAM: {vm.ram}
                ALM: {vm.almacenamiento}
                """
                grafo.node(vm.id, etiqueta_vm, shape="ellipse", style="filled", fillcolor="lightyellow")
                grafo.edge(centro.id, vm.id)
                nodo_vm = nodo_vm.siguiente

            actual_centro = actual_centro.siguiente
            if actual_centro == self.centros.centros.primero:
                break

        grafo.render("reporte_vms_por_centro", view=True)
        print("Reporte generado: reporte_vms_por_centro.png")

    # Reporte: Contenedores por VM
    def reporte_contenedores_por_vm(self):
        grafo = graphviz.Digraph("ContenedoresPorVM", format="png")
        grafo.attr(rankdir="LR", bgcolor="white")

        actual_centro = self.centros.centros.primero
        if actual_centro is None:
            print("No hay centros para graficar")
            return

        while True:
            centro = actual_centro.valor
            nodo_vm = centro.vms.primero
            while nodo_vm:
                vm = nodo_vm.valor
                etiqueta_vm = f"""
                VM: {vm.id}
                SO: {vm.so}
                CPU: {vm.cpu}
                RAM: {vm.ram}
                ALM: {vm.almacenamiento}
                """
                grafo.node(vm.id, etiqueta_vm, shape="box", style="filled", fillcolor="lightyellow")

                nodo_cont = vm.contenedores.primero
                while nodo_cont:
                    cont = nodo_cont.valor
                    etiqueta_cont = f"""
                    Contenedor: {cont.id}
                    Nombre: {cont.nombre}
                    Imagen: {cont.imagen}
                    CPU: {cont.cpu}
                    RAM: {cont.ram}
                    Puerto: {cont.puerto}
                    """
                    grafo.node(cont.id, etiqueta_cont, shape="ellipse", style="filled", fillcolor="lightgreen")
                    grafo.edge(vm.id, cont.id)
                    nodo_cont = nodo_cont.siguiente

                nodo_vm = nodo_vm.siguiente

            actual_centro = actual_centro.siguiente
            if actual_centro == self.centros.centros.primero:
                break

        grafo.render("reporte_contenedores_por_vm", view=True)
        print("Reporte generado: reporte_contenedores_por_vm.png")

    # Reporte: Solicitudes en cola
    def reporte_solicitudes(self):
        grafo = graphviz.Digraph("Solicitudes", format="png")
        grafo.attr(rankdir="TB", bgcolor="white")

        cola = self.solicitudes.cola
        if cola.esta_vacia():
            print("No hay solicitudes en la cola")
            return

        actual = cola.primero
        anterior_id = None
        while actual:
            sol = actual.valor
            etiqueta = f"""
            Solicitud: {sol.id}
            Cliente: {sol.cliente}
            Tipo: {sol.tipo}
            Prioridad: {sol.prioridad}
            CPU: {sol.cpu}
            RAM: {sol.ram}
            ALM: {sol.almacenamiento}
            Tiempo: {sol.tiempo}
            """
            grafo.node(sol.id, etiqueta, shape="box", style="filled", fillcolor="lightcoral")

            if anterior_id:
                grafo.edge(anterior_id, sol.id)

            anterior_id = sol.id
            actual = actual.siguiente

        grafo.render("reporte_solicitudes", view=True)
        print("Reporte generado: reporte_solicitudes.png")
