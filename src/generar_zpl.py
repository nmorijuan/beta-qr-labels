import pandas as pd
from pathlib import Path

# =====================================================
# CONFIGURACIÓN
# =====================================================

EXCEL = "../data/2657.xlsx"
SALIDA = "../output/etiquetas.zpl"

# -----------------------------------------------------
# ETIQUETA 25 x 25 mm
# Zebra ZT230 - 200 dpi
# -----------------------------------------------------

ANCHO = 197
ALTO = 197

# -----------------------------------------------------
# POSICIONES
# (Mañana solo modificaremos estos valores si es necesario)
# -----------------------------------------------------

CODIGO_X = 15
CODIGO_Y = 10

QR_X = 42
QR_Y = 35
QR_MAGNIFICACION = 5

DNI_X = 30
DNI_Y = 165

# =====================================================
# LEER EXCEL
# =====================================================

df = pd.read_excel(EXCEL)

# =====================================================
# GENERAR ZPL
# =====================================================

zpl = ""

for _, fila in df.iterrows():

    codigo = str(fila["CODIGO"]).strip()
    codigo_dni = str(fila["CODIGO-DNI"]).strip()

    etiqueta = f"""
^XA
^CI28
^PW{ANCHO}
^LL{ALTO}
^LH0,0
^FWN

^CF0,18

^FO{CODIGO_X},{CODIGO_Y}
^FD{codigo}^FS

^FO{QR_X},{QR_Y}
^BQN,2,{QR_MAGNIFICACION}
^FDQA,{codigo}^FS

^CF0,20

^FO{DNI_X},{DNI_Y}
^FD{codigo_dni}^FS

^XZ
"""

    zpl += etiqueta

# =====================================================
# GUARDAR
# =====================================================

Path("../output").mkdir(exist_ok=True)

with open(SALIDA, "w", encoding="utf-8") as archivo:
    archivo.write(zpl)

print("=" * 60)
print("ETIQUETAS GENERADAS CORRECTAMENTE")
print("=" * 60)
print(f"Archivo : {SALIDA}")
print(f"Cantidad: {len(df)}")
print("=" * 60)