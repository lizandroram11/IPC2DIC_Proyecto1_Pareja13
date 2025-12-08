from xml.dom import minidom 
from clases.campo import CampoAgricola 
from clases.estacion import EstacionBase

def leer_inventario(ruta, campos):
    doc = minidom.parse(ruta)

    campo_nuevo = None
    for campo in doc.getElementsByTagName('campo'): #Iterar sobre todos los elementos con la etiqueta 'campo'
        campo_nuevo = CampoAgricola(campo.getAttribute('id'), campo.getAttribute('nombre')) 
        estaciones = []

        for estacion in campo.getElementsByTagName('estacion'): #Iterar sobre los subelementos
            id = estacion.getAttribute('id')
            nombre = estacion.getAttribute('nombre')
            estaciones.append(EstacionBase(id, nombre))

        campo_nuevo.estaciones = estaciones
        campos.append(campo_nuevo)

    print('Información leída con éxito')

def escribir_inventario(ruta, campos):
    doc = minidom.Document() #Crea el documento DOM
    root = doc.createElement('camposAgricolas') #Crea el elemento raíz con la etiqueta inventario
    doc.appendChild(root) #Agrega la raíz al documento


    for campo in campos:
        campo_agricola = doc.createElement('campo') #Crea el elemento 'campo'
        campo_agricola.setAttribute('nombre', campo.get_nombre()) #Agregar el atributo 'nombre' al elemento

        estaciones = doc.createElement('estacionesBase')

        for estacion in campo.estaciones:
            tag_estacion = doc.createElement('estacion') 
            tag_estacion.setAttribute('id', estacion.get_id())
            tag_estacion.setAttribute('nombre', estacion.get_nombre())

            estaciones.appendChild(tag_estacion)

        campo_agricola.appendChild(estaciones)
        root.appendChild(campo_agricola)

    #Guardar el archivo XML
    with open(ruta, 'wb') as file:
        file.write(doc.toprettyxml(indent='\t', encoding="UTF-8")) 