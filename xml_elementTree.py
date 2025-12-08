import xml.etree.ElementTree as ET 
from clases.campo import CampoAgricola
from clases.estacion import EstacionBase

def leer_archivo(ruta, campos):
    try:
        tree = ET.parse(ruta) #Parsear el archivo XML
        root = tree.getroot() #Obtener el elemento raíz

        for campo_xml in root.findall('campo'):
            campo_id = campo_xml.get('id')
            campo_nombre = campo_xml.get('nombre')
            campo = CampoAgricola(campo_id, campo_nombre)

            # Estaciones base
            for estacion_xml in campo_xml.find('estacionesBase').findall('estacion'):
                id_estacion = estacion_xml.get('id')
                nombre_estacion = estacion_xml.get('nombre')
                estacion = EstacionBase(id_estacion, nombre_estacion)
                campo.agregar_estacion(estacion)
            
            campos.append(campo)
            print(f'Campo {campo_id} cargado exitosamente')

    except Exception as e:
        print(f"Error al cargar el archivo XML: {e}")


def escribir_archivo(ruta, campos):
    root = ET.Element('camposAgricolas') #Crea el elemento raíz con la etiqueta 'camposAgricolas'
    
    for campo in campos:
        campos = ET.SubElement(root, 'campo') #Agrega a la raíz un subelemento 'campo'
        #agrega atributos al subelemento
        campos.set('id', campo.get_id())
        campos.set('nombre', campo.get_nombre())

        estaciones_base = ET.SubElement(campos, 'estacionesBase') 
        for estacion in campo.estaciones:
            e =  ET.SubElement(estaciones_base, 'estacion')
            e.set('id', estacion.get_id())
            e.set('nombre', estacion.get_nombre())
            
    ET.indent(root, space='\t') #Agrega identación para que se vea mejor
    ET.ElementTree(root).write(ruta, encoding='UTF-8', xml_declaration=True) #Guardar el archivo XML