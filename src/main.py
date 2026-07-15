import pandas as pd

archivo = "../data/2657.xlsx"

df = pd.read_excel(archivo)

print("\n=== REGISTROS ENCONTRADOS ===\n")

print(df)

print(f"\nTotal de registros: {len(df)}")