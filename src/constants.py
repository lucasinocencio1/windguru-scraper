# Mapping of Windguru row IDs to readable names in Portuguese
PARAM_LABELS = {
    "time": "hora",
    "init": "inicialização",
    "WINDSPD": "vento_kmh",
    "GUST": "rajadas_kmh",
    "TMP": "temperatura_c",
    "TMPE": "temperatura_c",
    "HTSGW": "ondulacao_m",
    "PERPW": "periodo_vaga_s",
    "APCP": "precipitacao_mm",
    "APCP1": "precipitacao_mm_1h",
    "DIRPW": "direcao_vaga",
    "WAVEDIR": "direcao_vaga",
    "TCDC": "nebulosidade_pct",
    "RH": "humidade_pct",
    "SLP": "pressao_hpa",
    "WVHGT": "ondas_vento_m",
    "WVPER": "periodo_ondas_vento_s",
    "SWELL1": "ondulacao_1_m",
    "SWPER1": "periodo_ondulacao_1_s",
    "SWELL2": "ondulacao_2_m",
    "SWPER2": "periodo_ondulacao_2_s",
    "TIDE": "mare",
}

# Labels to exclude from the output
EXCLUDED_LABELS = {"tides", "cdc", "direcao_vaga", "mare"}
