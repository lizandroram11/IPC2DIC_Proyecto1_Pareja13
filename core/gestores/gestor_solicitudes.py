from core.estructuras.cola_prioridad import ColaPrioridad
from core.modelos.maquina_virtual import MaquinaVirtual

class GestorSolicitudes:
    def __init__(self):
        # Cola de prioridad donde se almacenan las solicitudes
        self.cola = ColaPrioridad()

        # Estos gestores se conectan desde el main
        self.gestor_centros = None
        self.gestor_vms = None


    # Conectar gestores externos
    def conectar_gestores(self, centros, vms):
        self.gestor_centros = centros
        self.gestor_vms = vms

   
    # Agregar solicitud a la cola
    def agregar(self, solicitud):
        self.cola.insertar(solicitud)

    
    # Procesar N solicitudes
    def procesar_n(self, cantidad):
        procesadas = 0
        completadas = 0
        fallidas = 0

        while procesadas < cantidad:
            solicitud = self.cola.extraer()

            # Si la cola está vacía, detenemos el proceso
            if solicitud is None:
                break

            procesadas += 1

            # Determinar el tipo de solicitud
            if solicitud.tipo == "Deploy":
                resultado = self._procesar_deploy(solicitud)

            elif solicitud.tipo == "Backup":
                resultado = self._procesar_backup(solicitud)

            else:
                # Tipo desconocido
                resultado = False

            # Contabilizar resultados
            if resultado:
                completadas += 1
            else:
                fallidas += 1

        return procesadas, completadas, fallidas

    
    # Procesar solicitud tipo Deploy
    def _procesar_deploy(self, solicitud):

        centro = self.gestor_centros.obtener_centro_con_mas_recursos()
        if centro is None:
            return False

        # Crear VM basada en la solicitud
        vm = MaquinaVirtual(
            solicitud.id,          # ID de la VM = ID de la solicitud
            "Ubuntu 22.04",        # SO por defecto
            solicitud.cpu,
            solicitud.ram,
            solicitud.almacenamiento,
            "0.0.0.0",             # IP por defecto
            centro.id
        )

        # Intentar crear la VM en el centro
        return self.gestor_vms.crear_vm_instruccion(vm, centro.id)

   
    # Procesar solicitud tipo Backup
    def _procesar_backup(self, solicitud):
        centro = self.gestor_centros.obtener_centro_con_mas_recursos()
        if centro is None:
            return False

        # Crear VM de backup
        vm = MaquinaVirtual(
            solicitud.id,
            "Backup-VM",
            solicitud.cpu,
            solicitud.ram,
            solicitud.almacenamiento,
            "0.0.0.0",
            centro.id
        )

        # Estado especial para backups
        vm.estado = "Suspendida"

        return self.gestor_vms.crear_vm_instruccion(vm, centro.id)