def calcular_kpis_agro(df):


    humedad_promedio = df["humedad_suelo_pct"].mean()

    temperatura_maxima = df["temp_ambiente_c"].max()

    parcelas_criticas = (df["humedad_suelo_pct"] < 30.0).sum()

    return {
        "humedad_promedio": humedad_promedio,
        "temperatura_maxima": temperatura_maxima,
        "parcelas_criticas": parcelas_criticas
    }