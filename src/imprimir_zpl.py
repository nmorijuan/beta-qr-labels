import os
import win32print

# ============================================
# CONFIGURACIÓN
# ============================================

IMPRESORA = "ZDesigner ZT230-200dpi ZPL"

ARCHIVO_ZPL = os.path.join(
    os.path.dirname(__file__),
    "..",
    "output",
    "etiquetas.zpl"
)

# ============================================
# VERIFICACIONES
# ============================================

print("=" * 50)
print("IMPRESIÓN DE ETIQUETAS ZPL")
print("=" * 50)

print(f"Impresora : {IMPRESORA}")
print(f"Archivo   : {ARCHIVO_ZPL}")

if not os.path.exists(ARCHIVO_ZPL):
    print("\nERROR:")
    print("No existe el archivo etiquetas.zpl")
    input("\nPresione ENTER para salir...")
    exit()

# ============================================
# LEER ARCHIVO ZPL
# ============================================

with open(ARCHIVO_ZPL, "rb") as archivo:
    datos = archivo.read()

print(f"\nTamaño del archivo: {len(datos)} bytes")

# ============================================
# ENVIAR A LA IMPRESORA
# ============================================

try:

    hPrinter = win32print.OpenPrinter(IMPRESORA)

    hJob = win32print.StartDocPrinter(
        hPrinter,
        1,
        ("Etiquetas QR", None, "RAW")
    )

    win32print.StartPagePrinter(hPrinter)

    win32print.WritePrinter(hPrinter, datos)

    win32print.EndPagePrinter(hPrinter)

    win32print.EndDocPrinter(hPrinter)

    win32print.ClosePrinter(hPrinter)

    print("\n====================================")
    print("IMPRESIÓN ENVIADA CORRECTAMENTE")
    print("====================================")

except Exception as e:

    print("\nERROR AL IMPRIMIR")
    print(e)

input("\nPresione ENTER para salir...")
