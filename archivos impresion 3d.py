import os
from pathlib import Path
import shutil

def obtener_carpeta_escritorio():
    """Obtiene la ruta correcta del escritorio del usuario."""
    try:
        # Detectar el Escritorio automáticamente
        return Path(os.path.join(os.environ["USERPROFILE"], "Desktop"))
    except KeyError:
        # Si no funciona, intenta con una ruta alternativa
        return Path.home() / "Escritorio"

def mover_archivos_3d():
    # Obtener las rutas de las carpetas principales
    carpeta_descargas = Path.home() / "Descargas"
    carpeta_escritorio = obtener_carpeta_escritorio()
    carpeta_destino = carpeta_escritorio / "Archivos impresion 3D"

    # Crear la carpeta de destino si no existe
    carpeta_destino.mkdir(parents=True, exist_ok=True)

    # Extensiones a buscar
    extensiones_3d = (".stl", ".3mf")

    # Función para buscar archivos en un directorio
    def buscar_archivos(directorio):
        archivos_encontrados = []
        for root, _, files in os.walk(directorio):
            for file in files:
                if file.lower().endswith(extensiones_3d):
                    archivos_encontrados.append(os.path.join(root, file))
        return archivos_encontrados

    # Priorizar la búsqueda en la carpeta Descargas
    archivos = buscar_archivos(carpeta_descargas)

    # Buscar en el resto del sistema si es necesario
    if not archivos:
        print("No se encontraron archivos en Descargas. Buscando en toda la computadora (esto puede tardar)...")
        archivos = buscar_archivos("/")

    # Mover archivos encontrados a la carpeta de destino
    for archivo in archivos:
        try:
            destino = carpeta_destino / os.path.basename(archivo)
            shutil.move(archivo, destino)  # Usar move para mover los archivos
            print(f"Archivo movido: {archivo} -> {destino}")
        except Exception as e:
            print(f"Error al mover {archivo}: {e}")

    print(f"Proceso completado. Archivos encontrados y movidos: {len(archivos)}")

if __name__ == "__main__":
    mover_archivos_3d()
