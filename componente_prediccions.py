
import pandas as pd


def estimar_necesidad_riego(df: pd.DataFrame) -> float:
    

    if df.empty:
        return 0.0

    humedad_promedio = df["humedad_suelo_pct"].mean()

    if humedad_promedio < 40.0:
        litros = (40.0 - humedad_promedio) * 150
        return round(litros, 2)

    return 0.0

