# -*- coding: utf-8 -*-
"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""


def pregunta_01():
    """Realiza la limpieza del archivo de solicitudes y escribe el resultado.

    Pasos de limpieza aplicados (resumen):
    - Lee `files/input/solicitudes_de_credito.csv` con separador `;`.
    - Elimina la primera columna índice si está presente.
    - Elimina duplicados y registros con valores requeridos ausentes.
    - Normaliza texto (strip + lower) en columnas de texto.
    - Limpia `monto_del_credito` (quita símbolos y separadores) y lo convierte a numérico.
    - Convierte `estrato` y `comuna_ciudadano` a enteros cuando es posible.
    - Normaliza `fecha_de_beneficio` a formato `dd/mm/YYYY`.
    - Escribe el CSV limpio en `files/output/solicitudes_de_credito.csv` con `;`.
    """
    import os
    import pandas as pd

    input_path = "files/input/solicitudes_de_credito.csv"
    output_dir = "files/output"
    output_path = os.path.join(output_dir, "solicitudes_de_credito.csv")

    os.makedirs(output_dir, exist_ok=True)

    df = pd.read_csv(input_path, sep=";")

    # Si la primera columna es un índice vacío, la eliminamos
    if df.columns[0] == "":
        df = df.drop(df.columns[0], axis=1)

    # Eliminar duplicados
    df = df.drop_duplicates()

    # Eliminar filas con NA en columnas críticas
    # Primero normalizamos cadenas para detectar vacíos con mayor facilidad
    obj_cols = df.select_dtypes(include=["object"]).columns.tolist()
    for c in obj_cols:
        df[c] = df[c].astype(str).str.strip()
        # Mantener valores NaN reales: reemplazar 'nan' generados por cast a str
        df.loc[df[c].str.lower() == 'nan', c] = pd.NA

    # Quitar filas que tengan NA en columnas que deben existir
    # fecha_de_beneficio puede tener formatos variados; no la marcamos como requerida
    required = ["sexo", "tipo_de_emprendimiento", "idea_negocio", "barrio", "estrato", "comuna_ciudadano", "monto_del_credito", "línea_credito"]
    df = df.dropna(subset=required)

    # Normalizar texto (lowercase) en columnas de texto
    for c in obj_cols:
        df[c] = df[c].astype(str).str.strip().str.lower()

    # Limpiar monto_del_credito: eliminar símbolos y separadores y convertir a numérico
    df["monto_del_credito"] = (
        df["monto_del_credito"].astype(str)
        .str.replace(r"[\$\,]", "", regex=True)
        .str.replace(r"\.00$", "", regex=True)
    )
    df["monto_del_credito"] = pd.to_numeric(df["monto_del_credito"], errors="coerce")
    df = df.dropna(subset=["monto_del_credito"])

    # Normalizar estrato y comuna_ciudadano a enteros
    df["estrato"] = df["estrato"].astype(str).str.extract(r"(\d+)")
    df["estrato"] = pd.to_numeric(df["estrato"], errors="coerce").astype("Int64")
    df = df.dropna(subset=["estrato"])

    df["comuna_ciudadano"] = (
        df["comuna_ciudadano"].astype(str).str.extract(r"(\d+)")
    )
    df["comuna_ciudadano"] = pd.to_numeric(df["comuna_ciudadano"], errors="coerce").astype("Int64")
    df = df.dropna(subset=["comuna_ciudadano"])

    # Normalizar fecha_de_beneficio: formatear cuando sea parseable, si no conservar el valor original
    parsed = pd.to_datetime(df["fecha_de_beneficio"], dayfirst=True, errors="coerce")
    df["fecha_de_beneficio"] = (
        parsed.dt.strftime("%d/%m/%Y").where(parsed.notna()).fillna(df["fecha_de_beneficio"].astype(str))
    )

    # Normalizar linea de credito
    if "línea_credito" in df.columns:
        df["línea_credito"] = df["línea_credito"].astype(str).str.strip().str.lower()

    # Asegurar que los tipos y nombres de columnas sigan siendo consistentes
    df.to_csv(output_path, sep=";", index=False)
