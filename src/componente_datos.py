import pandas as pd


def cargar_y_validar_datos_agro(file) -> pd.DataFrame:
    """Carga y valida los datos telemétricos de humedad y temperatura del suelo.

    :param file: Ruta del archivo o buffer del archivo subido en Streamlit.
    :return: DataFrame validado según el contrato de datos.
    :raises ValueError: Si faltan columnas, tipos de datos no válidos o
      valores fuera de rango.
    """
    # 1. Cargar el archivo
    try:
        if isinstance(file, str) and file.endswith(".xlsx"):
            df = pd.read_excel(file)
        elif isinstance(file, str) and file.endswith(".json"):
            df = pd.read_json(file)
        else:
            df = pd.read_csv(file)
    except Exception as e:
        raise ValueError(f"Error al leer el archivo de datos: {str(e)}")

    # 2. Validar que existan las 4 columnas requeridas
    columnas_esperadas = {
        "timestamp",
        "id_parcela",
        "humedad_suelo_pct",
        "temp_ambiente_c",
    }
    columnas_presentes = set(df.columns)

    if not columnas_esperadas.issubset(columnas_presentes):
        columnas_faltantes = columnas_esperadas - columnas_presentes
        raise ValueError(
            f"El archivo no cumple el contrato de datos. Columnas faltantes: {columnas_faltantes}"
        )

    # 3. Convertir tipos de datos según especificación
    try:
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df["id_parcela"] = df["id_parcela"].astype(str)
        df["humedad_suelo_pct"] = df["humedad_suelo_pct"].astype(float)
        df["temp_ambiente_c"] = df["temp_ambiente_c"].astype(float)
    except Exception as e:
        raise ValueError(
            f"Error en la conversión de tipos de datos según la especificación: {str(e)}"
        )

    # 4. Validar que no existan valores nulos
    if df[list(columnas_esperadas)].isnull().any().any():
        raise ValueError(
            "El dataset contiene valores nulos en columnas obligatorias."
        )

    # 5. Validar rango estricto de humedad (0.0 <= humedad <= 100.0)
    humedad_invalida = df[
        (df["humedad_suelo_pct"] < 0.0) | (df["humedad_suelo_pct"] > 100.0)
    ]
    if not humedad_invalida.empty:
        raise ValueError(
            f"Se encontraron {len(humedad_invalida)} registros con 'humedad_suelo_pct' fuera del rango permitido (0.0 - 100.0)."
        )

    return df