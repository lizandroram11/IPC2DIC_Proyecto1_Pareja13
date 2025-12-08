class GeneradorXML:
    def __init__(self, centros, vms, contenedores):
        self.centros = centros
        self.vms = vms
        self.contenedores = contenedores

    def generar(self, ruta_salida):
        print("Generando archivo XML de salida...")