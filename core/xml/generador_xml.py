import xml.etree.ElementTree as ET
from xml.dom import minidom
from clases.campo import CampoAgricola
from clases.estacion import Estacion
from clases.sensor_suelo import SensorSuelo
from clases.sensor_cultivo import SensorCultivo
from clases.frecuencia import Frecuencia
from clases.nodo import ListaEnlazada
from graphviz import Digraph


'''codigo utilizado semestre pasado, a partir de aca se modificara para uso del proyecto'''

# Definición de la clase XMLManager, representa una entidad del sistema
class XMLManager:
# Método __init__: se encarga de una funcionalidad específica de la clase o del flujo principal
    def __init__(self):
        self.campos = ListaEnlazada()

    # Helpers that work with ListaEnlazada instead of Python lists
# Método _ids_de_estaciones: se encarga de una funcionalidad específica de la clase o del flujo principal
    def _ids_de_estaciones(self, campo):
        ids = ListaEnlazada()
        for est in campo.estaciones.recorrer():
            ids.insertar(est.get_id())
        return ids

# Método _sensores_unicos: se encarga de una funcionalidad específica de la clase o del flujo principal
    def _sensores_unicos(self, iter_estaciones, attr_name):
        unicos = ListaEnlazada()
        for est in iter_estaciones.recorrer():
            sensores = getattr(est, attr_name)
            for s in sensores.recorrer():
                if not unicos.contiene(lambda x: x.get_id() == s.get_id()):
                    unicos.insertar(s)
        return unicos

# Método _valor_frecuencia: se encarga de una funcionalidad específica de la clase o del flujo principal
    def _valor_frecuencia(self, sensor, id_est):
        # retorna el valor numérico o 0
        for f in sensor.frecuencias.recorrer():
            if f.id_estacion == id_est:
                return f.valor
        return 0

# Método _existe_frecuencia: se encarga de una funcionalidad específica de la clase o del flujo principal
    def _existe_frecuencia(self, sensor, id_est):
        for f in sensor.frecuencias.recorrer():
            if f.id_estacion == id_est:
                return 1
        return 0

# Método cargar_archivo: se encarga de una funcionalidad específica de la clase o del flujo principal
    def cargar_archivo(self, ruta):
        tree = ET.parse(ruta)
        root = tree.getroot()

        for campo_xml in root.findall("campo"):
            id_campo = campo_xml.get("id")
            nombre_campo = campo_xml.get("nombre")
            campo = CampoAgricola(id_campo, nombre_campo)

            # Estaciones
            estaciones_xml = campo_xml.find("estacionesBase")
            if estaciones_xml is not None:
                for est_xml in estaciones_xml.findall("estacion"):
                    est = Estacion(est_xml.get("id"), est_xml.get("nombre"))
                    campo.agregar_estacion(est)

            # Sensores Suelo
            suelo_xml = campo_xml.find("sensoresSuelo")
            if suelo_xml is not None:
                for s_xml in suelo_xml.findall("sensorS"):
                    sensor = SensorSuelo(s_xml.get("id"), s_xml.get("nombre"))
                    for f_xml in s_xml.findall("frecuencia"):
                        sensor.agregar_frecuencia(Frecuencia(f_xml.get("idEstacion"), f_xml.text.strip()))
                    # asignar a estaciones relacionadas
                    for est in campo.estaciones.recorrer():
                        if self._existe_frecuencia(sensor, est.get_id()) == 1:
                            est.agregar_sensor_suelo(sensor)

            # Sensores Cultivo
            cultivo_xml = campo_xml.find("sensoresCultivo")
            if cultivo_xml is not None:
                for t_xml in cultivo_xml.findall("sensorT"):
                    sensor = SensorCultivo(t_xml.get("id"), t_xml.get("nombre"))
                    for f_xml in t_xml.findall("frecuencia"):
                        sensor.agregar_frecuencia(Frecuencia(f_xml.get("idEstacion"), f_xml.text.strip()))
                    for est in campo.estaciones.recorrer():
                        if self._existe_frecuencia(sensor, est.get_id()) == 1:
                            est.agregar_sensor_cultivo(sensor)

            self.campos.insertar(campo)
        print("Archivo cargado correctamente.")

# Método procesar_archivo: se encarga de una funcionalidad específica de la clase o del flujo principal
    def procesar_archivo(self):
        if self.campos.esta_vacia():
            print("No hay campos cargados.")
            return

        for campo in self.campos.recorrer():
            print(f"\nProcesando Campo: {campo.get_nombre()} (ID: {campo.get_id()})")

            estaciones_ids = self._ids_de_estaciones(campo)
            sensores_suelo = self._sensores_unicos(campo.estaciones, "sensores_suelo")
            sensores_cultivo = self._sensores_unicos(campo.estaciones, "sensores_cultivo")

            # Matriz F[n,s]
            cabecera_suelo = [s.get_id() for s in sensores_suelo.recorrer()]
            print("\nMatriz F[n,s] (Estaciones x Sensores de Suelo)")
            print("     " + "  ".join(cabecera_suelo))
            for id_est in estaciones_ids.recorrer():
                fila_vals = []
                for s in sensores_suelo.recorrer():
                    fila_vals.append(str(self._valor_frecuencia(s, id_est)))
                print(f"{id_est}  " + "  ".join(fila_vals))

            # Matriz F[n,t]
            cabecera_cult = [s.get_id() for s in sensores_cultivo.recorrer()]
            print("\nMatriz F[n,t] (Estaciones x Sensores de Cultivo)")
            print("     " + "  ".join(cabecera_cult))
            for id_est in estaciones_ids.recorrer():
                fila_vals = []
                for s in sensores_cultivo.recorrer():
                    fila_vals.append(str(self._valor_frecuencia(s, id_est)))
                print(f"{id_est}  " + "  ".join(fila_vals))

# Método generar_patrones: se encarga de una funcionalidad específica de la clase o del flujo principal
    def generar_patrones(self):
        if self.campos.esta_vacia():
            print("No hay campos cargados.")
            return {}

        patrones_por_campo = {}
        for campo in self.campos.recorrer():
            estaciones_ids = self._ids_de_estaciones(campo)
            sensores_suelo = self._sensores_unicos(campo.estaciones, "sensores_suelo")
            sensores_cultivo = self._sensores_unicos(campo.estaciones, "sensores_cultivo")

            print(f"\nGenerando patrones para Campo: {campo.get_nombre()} (ID: {campo.get_id()})")

            print("\nMatriz de Patrones Fp[n,s]")
            cabecera_suelo = [s.get_id() for s in sensores_suelo.recorrer()]
            print("     " + "  ".join(cabecera_suelo))
            patrones_suelo = {}
            for id_est in estaciones_ids.recorrer():
                bits = []
                for s in sensores_suelo.recorrer():
                    bits.append(str(self._existe_frecuencia(s, id_est)))
                print(f"{id_est}  " + "  ".join(bits))
                patrones_suelo[id_est] = "".join(bits)

            print("\nMatriz de Patrones Fp[n,t]")
            cabecera_cult = [s.get_id() for s in sensores_cultivo.recorrer()]
            print("     " + "  ".join(cabecera_cult))
            patrones_cult = {}
            for id_est in estaciones_ids.recorrer():
                bits = []
                for s in sensores_cultivo.recorrer():
                    bits.append(str(self._existe_frecuencia(s, id_est)))
                print(f"{id_est}  " + "  ".join(bits))
                patrones_cult[id_est] = "".join(bits)

            patrones_por_campo[campo.get_id()] = (campo, patrones_suelo, patrones_cult)
        return patrones_por_campo

# Método reducir_estaciones: se encarga de una funcionalidad específica de la clase o del flujo principal
    def reducir_estaciones(self):
        patrones = self.generar_patrones()
        resultado = []  # (campo, grupos)  *usaremos para escribir salida*

        for _, (campo, p_suelo, p_cult) in patrones.items():
            grupos = []
            usados = set()

            # construir lista de estaciones (ListaEnlazada)
            estaciones = ListaEnlazada()
            for e in campo.estaciones.recorrer():
                estaciones.insertar(e)

            for e1 in estaciones.recorrer():
                if e1.get_id() in usados:
                    continue
                grupo = ListaEnlazada()
                grupo.insertar(e1)
                usados.add(e1.get_id())

                for e2 in estaciones.recorrer():
                    if e2.get_id() in usados or e2.get_id() == e1.get_id():
                        continue
                    if p_suelo.get(e1.get_id(), "") == p_suelo.get(e2.get_id(), "") and \
                        p_cult.get(e1.get_id(), "") == p_cult.get(e2.get_id(), ""):
                        grupo.insertar(e2)
                        usados.add(e2.get_id())

                grupos.append(grupo)
                # mostrar
            print("\nAgrupamiento de estaciones (Campo: " + campo.get_nombre() + ")")
            for g in grupos:
                ids = [e.get_id() for e in g.recorrer()]
                print("   Grupo: " + ", ".join(ids))

            resultado.append((campo, grupos))
        return resultado

# Método escribir_salida: se encarga de una funcionalidad específica de la clase o del flujo principal
    def escribir_salida(self, ruta_salida, grupos):
        root = ET.Element("camposAgricolas")

        for campo, grupos_estaciones in grupos:
            campo_elem = ET.SubElement(root, "campo", id=campo.get_id(), nombre=campo.get_nombre())
            estaciones_reducidas_elem = ET.SubElement(campo_elem, "estacionesBaseReducidas")

            # crear estaciones reducidas
            for grupo in grupos_estaciones:
                # nuevo id = del primero
                primero = None
                nombres_concat = []
                for e in grupo.recorrer():
                    if primero is None:
                        primero = e
                    nombres_concat.append(e.get_nombre())
                ET.SubElement(estaciones_reducidas_elem, "estacion",
                              id=primero.get_id(), nombre=", ".join(nombres_concat))

            # Sensores Suelo
            sensores_suelo_elem = ET.SubElement(campo_elem, "sensoresSuelo")
            # Necesitamos lista de sensores únicos
            sensores_suelo = self._sensores_unicos(campo.estaciones, "sensores_suelo")
            for s in sensores_suelo.recorrer():
                s_elem = ET.SubElement(sensores_suelo_elem, "sensorS", id=s.get_id(), nombre=s.get_nombre())
                for grupo in grupos_estaciones:
                    # sumatoria de frecuencias por grupo
                    id_destino = None
                    suma = 0
                    for e in grupo.recorrer():
                        if id_destino is None:
                            id_destino = e.get_id()
                        suma += self._valor_frecuencia(s, e.get_id())
                    f_elem = ET.SubElement(s_elem, "frecuencia", idEstacion=id_destino)
                    f_elem.text = str(suma)

            # Sensores Cultivo
            sensores_cult_elem = ET.SubElement(campo_elem, "sensoresCultivo")
            sensores_cultivo = self._sensores_unicos(campo.estaciones, "sensores_cultivo")
            for s in sensores_cultivo.recorrer():
                s_elem = ET.SubElement(sensores_cult_elem, "sensorT", id=s.get_id(), nombre=s.get_nombre())
                for grupo in grupos_estaciones:
                    id_destino = None
                    suma = 0
                    for e in grupo.recorrer():
                        if id_destino is None:
                            id_destino = e.get_id()
                        suma += self._valor_frecuencia(s, e.get_id())
                    f_elem = ET.SubElement(s_elem, "frecuencia", idEstacion=id_destino)
                    f_elem.text = str(suma)

        xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent="   ")
        with open(ruta_salida, "w", encoding="utf-8") as f:
            f.write(xml_str)
        print(f"Archivo de salida escrito en: {ruta_salida}")

# Método generar_grafica: se encarga de una funcionalidad específica de la clase o del flujo principal
    def generar_grafica(self, archivo_salida="grafica"):
        if self.campos.esta_vacia():
            print("No hay campos cargados.")
            return

        dot = Digraph(comment="Campos Agrícolas", format="png")
        dot.attr(rankdir="LR", size="8")

        for campo in self.campos.recorrer():
            campo_id = f"campo_{campo.get_id()}"
            dot.node(campo_id, f"Campo: {campo.get_nombre()}", shape="box", style="filled", color="lightblue")

            for est in campo.estaciones.recorrer():
                est_id = f"est_{est.get_id()}"
                dot.node(est_id, f"Estación: {est.get_nombre()}", shape="ellipse", style="filled", color="lightgreen")
                dot.edge(campo_id, est_id)

                # Sensores de suelo
                for sensor in est.sensores_suelo.recorrer():
                    s_id = f"suelo_{sensor.get_id()}"
                    dot.node(s_id, f"Suelo: {sensor.get_nombre()}", shape="diamond", style="filled", color="orange")
                    dot.edge(est_id, s_id)

                # Sensores de cultivo
                for sensor in est.sensores_cultivo.recorrer():
                    c_id = f"cult_{sensor.get_id()}"
                    dot.node(c_id, f"Cultivo: {sensor.get_nombre()}", shape="diamond", style="filled", color="pink")
                    dot.edge(est_id, c_id)

        output_path = dot.render(archivo_salida, cleanup=True)
        print(f"Gráfica generada: {output_path}")