import polars as pl
import random

def ejecutar_forecast_pipeline(horizonte_meses: int = 12):
    """
    Simula o ejecuta tu pipeline de Polars y XGBoost Quantile Regression.
    Retorna un DataFrame de Polars con los resultados del forecast.
    """
    # Ejemplo simulado basado en tu pipeline de demanda
    meses = [f"2026-{m:02d}" if m > 11 else f"2027-{(m-11):02d}" for m in range(12, 12 + horizonte_meses)]
    
    datos = {
        "Mes": meses[:horizonte_meses],
        "Demanda_Estimada": [random.randint(1200, 2500) for _ in range(horizonte_meses)],
        "Limite_Inferior": [random.randint(900, 1100) for _ in range(horizonte_meses)],
        "Limite_Superior": [random.randint(2600, 3000) for _ in range(horizonte_meses)]
    }
    
    df = pl.DataFrame(datos)
    return df