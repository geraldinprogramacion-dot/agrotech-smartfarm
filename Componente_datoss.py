import pandas as pd

def cargar_y_validar_transacciones(file):
    """
    Carga el archivo de transacciones y valida que cumpla las reglas del examen.
    """
    df = pd.read_csv(file)

    #  las 4 columnas obligatorias
    columnas_requeridas = ['id_transaccion', 'fecha_hora', 'monto_eur', 'distancia_km_cliente']
    for col in columnas_requeridas:
        if col not in df.columns:
            raise ValueError(f"Falta la columna obligatoria: {col}")

    # 3.(monto > 0 y distancia >= 0)
    if (df['monto_eur'] <= 0).any():
        raise ValueError("Error: Se detectaron transacciones con monto_eur <= 0")

    if (df['distancia_km_cliente'] < 0).any():
        raise ValueError("Error: Se detectaron distancias negativas")

    df['fecha_hora'] = pd.to_datetime(df['fecha_hora'])
    df['monto_eur'] = pd.to_numeric(df['monto_eur'])
    df['distancia_km_cliente'] = pd.to_numeric(df['distancia_km_cliente'])

    return df


if __name__ == "__main__":
    
    print("Probando el archivo...")
    df_resultado = cargar_y_validar_transacciones("transacciones.csv")
    print("¡Validado con éxito!")