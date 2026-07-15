"""
Funciones para generar ZPL y preview desde archivos Excel
"""

import pandas as pd
from pathlib import Path

# =====================================================
# CONFIGURACIÓN
# =====================================================

# Etiqueta 25 x 25 mm
# Zebra ZT230 - 200 dpi

ANCHO = 197
ALTO = 197

# Posiciones
CODIGO_X = 15
CODIGO_Y = 10

QR_X = 42
QR_Y = 35
QR_MAGNIFICACION = 5

DNI_X = 30
DNI_Y = 165

# =====================================================
# FUNCIONES
# =====================================================

def generar_preview_excel(filepath):
    """
    Lee el Excel y retorna un preview de los datos
    """
    try:
        df = pd.read_excel(filepath)
        
        # Validar columnas requeridas
        columnas_requeridas = ['CODIGO', 'CODIGO-DNI']
        columnas_faltantes = [col for col in columnas_requeridas if col not in df.columns]
        
        if columnas_faltantes:
            raise ValueError(f"Columnas faltantes: {', '.join(columnas_faltantes)}")
        
        preview = {
            'total': len(df),
            'columnas': df.columns.tolist(),
            'datos': df.head(10).to_dict('records'),
            'mensaje': f"Total de registros: {len(df)}"
        }
        
        return preview
    
    except Exception as e:
        raise Exception(f"Error leyendo archivo: {str(e)}")

def generar_zpl_desde_excel(filepath):
    """
    Lee el Excel y genera el contenido ZPL
    """
    try:
        df = pd.read_excel(filepath)
        
        # Validar columnas requeridas
        columnas_requeridas = ['CODIGO', 'CODIGO-DNI']
        columnas_faltantes = [col for col in columnas_requeridas if col not in df.columns]
        
        if columnas_faltantes:
            raise ValueError(f"Columnas faltantes: {', '.join(columnas_faltantes)}")
        
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
        
        return zpl
    
    except Exception as e:
        raise Exception(f"Error generando ZPL: {str(e)}")

def guardar_zpl(zpl_content, filepath):
    """
    Guarda el contenido ZPL en un archivo
    """
    try:
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as archivo:
            archivo.write(zpl_content)
        
        return True
    
    except Exception as e:
        raise Exception(f"Error guardando archivo: {str(e)}")
