import busio
import board
import sdcardio
import storage
import os
import gc  # Para obtener memoria disponible en el microcontrolador

class SDManager:
    def __init__(self, sck=board.SD_SCK, mosi=board.SD_MOSI, miso=board.SD_MISO, cs=board.SD_CS):
        """Inicializa la tarjeta SD."""
        self.spi = busio.SPI(sck, mosi, miso)
        self.cs = cs
        self.mounted = False
        try:
            self.sd = sdcardio.SDCard(self.spi, self.cs)
            self.vfs = storage.VfsFat(self.sd)
            storage.mount(self.vfs, "/sd")
            self.mounted = True
            print("Tarjeta SD montada con éxito.")
        except Exception as e:
            print("Error al inicializar la tarjeta SD:", e)

    def listar_archivos(self):
        """Lista todos los archivos en la raíz de la tarjeta SD."""
        if self.mounted:
            try:
                return os.listdir("/sd")
            except Exception as e:
                print("Error al listar archivos:", e)
                return []
        else:
            print("La tarjeta SD no está montada.")
            return []

    def escribir_archivo(self, nombre, contenido):
        """Escribe contenido en un archivo."""
        if self.mounted:
            try:
                with open(f"/sd/{nombre}", "w") as f:
                    f.write(contenido)
                print(f"Archivo '{nombre}' escrito con éxito.")
            except Exception as e:
                print(f"Error al escribir en el archivo '{nombre}':", e)
        else:
            print("La tarjeta SD no está montada.")

    def leer_archivo(self, nombre):
        """Lee el contenido de un archivo."""
        if self.mounted:
            try:
                with open(f"/sd/{nombre}", "r") as f:
                    contenido = f.read()
                print(f"Contenido de '{nombre}':")
                return contenido
            except Exception as e:
                print(f"Error al leer el archivo '{nombre}':", e)
                return None
        else:
            print("La tarjeta SD no está montada.")
            return None

    def renombrar_archivo(self, nombre_actual, nuevo_nombre):
        """Renombra un archivo."""
        if self.mounted:
            try:
                os.rename(f"/sd/{nombre_actual}", f"/sd/{nuevo_nombre}")
                print(f"Archivo '{nombre_actual}' renombrado a '{nuevo_nombre}'.")
            except Exception as e:
                print(f"Error al renombrar '{nombre_actual}':", e)
        else:
            print("La tarjeta SD no está montada.")

    def borrar_archivo(self, nombre):
        """Elimina un archivo."""
        if self.mounted:
            try:
                os.remove(f"/sd/{nombre}")
                print(f"Archivo '{nombre}' eliminado con éxito.")
            except Exception as e:
                print(f"Error al eliminar el archivo '{nombre}':", e)
        else:
            print("La tarjeta SD no está montada.")

    def detalles_tarjeta(self):
        """Muestra detalles de la tarjeta SD: capacidad, espacio libre, espacio utilizado y archivos."""
        if self.mounted:
            try:
                statvfs = os.statvfs("/sd")
                capacidad_total = statvfs[0] * statvfs[2] / 1024 / 1024  # Capacidad total en MB
                espacio_libre = statvfs[0] * statvfs[3] / 1024 / 1024    # Espacio libre en MB
                espacio_utilizado = capacidad_total - espacio_libre     # Espacio utilizado en MB
                archivos = self.listar_archivos()

                print(f"Detalles de la tarjeta SD:")
                print(f"- Capacidad total: {capacidad_total:.2f} MB")
                print(f"- Espacio utilizado: {espacio_utilizado:.2f} MB")
                print(f"- Espacio libre: {espacio_libre:.2f} MB")
                print(f"- Archivos: {archivos}")
                return {
                    "capacidad_total": capacidad_total,
                    "espacio_utilizado": espacio_utilizado,
                    "espacio_libre": espacio_libre,
                    "archivos": archivos
                }
            except Exception as e:
                print("Error al obtener los detalles de la tarjeta SD:", e)
                return None
        else:
            print("La tarjeta SD no está montada.")
            return None
