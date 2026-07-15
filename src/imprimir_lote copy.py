from pathlib import Path
import sys

import pandas as pd
import win32print


# ============================================================
# CONFIGURACIÓN GENERAL
# ============================================================

IMPRESORA = "ZDesigner ZT230-200dpi ZPL"

# Rutas calculadas desde la ubicación de este archivo.
CARPETA_PROYECTO = Path(__file__).resolve().parent.parent
ARCHIVO_EXCEL = CARPETA_PROYECTO / "data" / "2657.xlsx"
CARPETA_SALIDA = CARPETA_PROYECTO / "output"
ARCHIVO_ZPL = CARPETA_SALIDA / "etiquetas.zpl"


# ============================================================
# CONFIGURACIÓN DEL ROLLO
# ============================================================

# Cuatro stickers por cada fila física.
ETIQUETAS_POR_FILA = 4

# ZT230 de 203 dpi: aproximadamente 8 dots por milímetro.
# Se utiliza un ancho total conservador de 104 mm.
ANCHO_TOTAL_DOTS = 832

# Cada espacio disponible dentro de la fila.
ANCHO_COLUMNA_DOTS = 208

# Altura de una fila:
# 25 mm de etiqueta + aproximadamente 4 mm de separación vertical.
ALTO_FILA_DOTS = 232

# Inicio horizontal de cada una de las cuatro posiciones.
POSICIONES_X = [0, 208, 416, 624]


# ============================================================
# POSICIÓN DEL CONTENIDO DENTRO DE CADA STICKER
# ============================================================

# QR
QR_DESPLAZAMIENTO_X = 54
QR_Y = 28
QR_MAGNIFICACION = 5.5

# Texto inferior: contenido de CODIGO-DNI
TEXTO_Y = 170
TEXTO_ALTO = 20
TEXTO_ANCHO = 18


def leer_excel() -> list[dict[str, str]]:
    """
    Lee el Excel y devuelve CODIGO y CODIGO-DNI como texto.
    """

    if not ARCHIVO_EXCEL.exists():
        raise FileNotFoundError(
            f"No se encontró el archivo Excel:\n{ARCHIVO_EXCEL}"
        )

    dataframe = pd.read_excel(
        ARCHIVO_EXCEL,
        dtype={
            "CODIGO": str,
            "CODIGO-DNI": str,
        },
    )

    columnas_requeridas = {"CODIGO", "CODIGO-DNI"}
    columnas_encontradas = set(dataframe.columns)

    faltantes = columnas_requeridas - columnas_encontradas

    if faltantes:
        raise ValueError(
            "Faltan columnas obligatorias en el Excel: "
            + ", ".join(sorted(faltantes))
        )

    # Elimina filas completamente vacías.
    dataframe = dataframe.dropna(
        how="all",
        subset=["CODIGO", "CODIGO-DNI"],
    )

    registros: list[dict[str, str]] = []

    for numero_fila, fila in dataframe.iterrows():
        codigo = str(fila["CODIGO"]).strip()
        codigo_dni = str(fila["CODIGO-DNI"]).strip()

        if not codigo or codigo.lower() == "nan":
            raise ValueError(
                f"La fila {numero_fila + 2} no tiene un CODIGO válido."
            )

        if not codigo_dni or codigo_dni.lower() == "nan":
            raise ValueError(
                f"La fila {numero_fila + 2} no tiene un CODIGO-DNI válido."
            )

        registros.append(
            {
                "codigo": codigo,
                "codigo_dni": codigo_dni,
            }
        )

    if not registros:
        raise ValueError("El archivo Excel no contiene registros válidos.")

    return registros


def dividir_en_filas(
    registros: list[dict[str, str]],
    cantidad: int = ETIQUETAS_POR_FILA,
) -> list[list[dict[str, str]]]:
    """
    Divide los registros en grupos de cuatro.
    """

    return [
        registros[indice:indice + cantidad]
        for indice in range(0, len(registros), cantidad)
    ]


def escapar_zpl(valor: str) -> str:
    """
    Evita que caracteres de control ZPL alteren la impresión.
    """

    return (
        valor
        .replace("^", " ")
        .replace("~", " ")
        .replace("\r", " ")
        .replace("\n", " ")
        .strip()
    )


def generar_zpl(registros: list[dict[str, str]]) -> str:
    """
    Genera una fila física por cada grupo de cuatro registros.
    """

    bloques: list[str] = []

    grupos = dividir_en_filas(registros)

    for grupo in grupos:
        bloque = [
            "^XA",
            "^CI28",
            f"^PW{ANCHO_TOTAL_DOTS}",
            f"^LL{ALTO_FILA_DOTS}",
            "^LH0,0",
            "^FWN",
            "^MMT",
        ]

        for posicion, registro in enumerate(grupo):
            base_x = POSICIONES_X[posicion]

            codigo = escapar_zpl(registro["codigo"])
            codigo_dni = escapar_zpl(registro["codigo_dni"])

            qr_x = base_x + QR_DESPLAZAMIENTO_X

            # QR: contiene únicamente la columna CODIGO.
            bloque.extend(
                [
                    f"^FO{qr_x},{QR_Y}",
                    f"^BQN,2,{QR_MAGNIFICACION}",
                    f"^FDLA,{codigo}^FS",
                ]
            )

            # Texto centrado debajo del QR.
            bloque.extend(
                [
                    f"^FO{base_x + 45},{TEXTO_Y}",
                    f"^A0N,{TEXTO_ALTO},{TEXTO_ANCHO}",
                    f"^FD{codigo_dni}^FS",
                ]
            )

        bloque.append("^XZ")

        bloques.append("\n".join(bloque))

    return "\n".join(bloques)


def guardar_zpl(contenido: str) -> None:
    """
    Guarda una copia del trabajo generado.
    """

    CARPETA_SALIDA.mkdir(parents=True, exist_ok=True)

    ARCHIVO_ZPL.write_text(
        contenido,
        encoding="utf-8",
        newline="\n",
    )


def verificar_impresora() -> None:
    """
    Confirma que la impresora existe en Windows.
    """

    impresoras = {
        informacion[2]
        for informacion in win32print.EnumPrinters(
            win32print.PRINTER_ENUM_LOCAL
            | win32print.PRINTER_ENUM_CONNECTIONS
        )
    }

    if IMPRESORA not in impresoras:
        raise RuntimeError(
            f"No se encontró la impresora:\n{IMPRESORA}"
        )


def imprimir_zpl(contenido: str) -> None:
    """
    Envía el ZPL como un único trabajo RAW.
    """

    verificar_impresora()

    datos = contenido.encode("utf-8")

    manejador = None
    documento_iniciado = False
    pagina_iniciada = False

    try:
        manejador = win32print.OpenPrinter(IMPRESORA)

        win32print.StartDocPrinter(
            manejador,
            1,
            (
                "Etiquetas QR - Lote",
                None,
                "RAW",
            ),
        )
        documento_iniciado = True

        win32print.StartPagePrinter(manejador)
        pagina_iniciada = True

        bytes_enviados = win32print.WritePrinter(
            manejador,
            datos,
        )

        if bytes_enviados != len(datos):
            raise RuntimeError(
                "Windows no envió todos los datos a la impresora."
            )

    finally:
        if manejador is not None:
            if pagina_iniciada:
                win32print.EndPagePrinter(manejador)

            if documento_iniciado:
                win32print.EndDocPrinter(manejador)

            win32print.ClosePrinter(manejador)


def main() -> None:
    print("=" * 62)
    print("GENERACIÓN E IMPRESIÓN DE ETIQUETAS QR")
    print("=" * 62)
    print(f"Excel     : {ARCHIVO_EXCEL}")
    print(f"Impresora : {IMPRESORA}")
    print()

    try:
        registros = leer_excel()

        cantidad_registros = len(registros)
        cantidad_filas = (
            cantidad_registros + ETIQUETAS_POR_FILA - 1
        ) // ETIQUETAS_POR_FILA

        print(f"Registros encontrados : {cantidad_registros}")
        print(f"Filas físicas         : {cantidad_filas}")
        print(f"Etiquetas por fila    : {ETIQUETAS_POR_FILA}")

        contenido_zpl = generar_zpl(registros)
        guardar_zpl(contenido_zpl)

        print()
        print("Archivo ZPL actualizado correctamente:")
        print(ARCHIVO_ZPL)

        respuesta = input(
            "\n¿Deseas imprimir este lote ahora? [S/N]: "
        ).strip().upper()

        if respuesta != "S":
            print("\nImpresión cancelada.")
            return

        imprimir_zpl(contenido_zpl)

        print()
        print("=" * 62)
        print("LOTE ENVIADO CORRECTAMENTE A LA IMPRESORA")
        print("=" * 62)
        print(f"Etiquetas enviadas : {cantidad_registros}")
        print(f"Filas físicas      : {cantidad_filas}")

    except Exception as error:
        print()
        print("=" * 62)
        print("ERROR")
        print("=" * 62)
        print(error)
        sys.exit(1)


if __name__ == "__main__":
    main()