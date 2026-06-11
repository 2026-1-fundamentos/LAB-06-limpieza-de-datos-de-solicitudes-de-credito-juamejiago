import pandas as pd
orig = pd.read_csv('files/input/solicitudes_de_credito.csv', sep=';')
orig_cols = orig.columns.tolist()
print('orig shape', orig.shape)
subsets = [
    ['monto_del_credito','fecha_de_beneficio','sexo','idea_negocio','línea_credito','estrato','comuna_ciudadano'],
    ['monto_del_credito','fecha_de_beneficio','sexo','idea_negocio','línea_credito'],
    ['monto_del_credito','fecha_de_beneficio','sexo','idea_negocio','línea_credito','barrio','tipo_de_emprendimiento'],
    ['monto_del_credito','fecha_de_beneficio','sexo','idea_negocio','línea_credito','estrato'],
]
for s in subsets:
    df = orig.copy()
    # normalize strings to catch blanks
    for c in df.select_dtypes(include=['object']).columns:
        df[c] = df[c].astype(str).str.strip()
        df.loc[df[c].str.lower()=='nan', c] = pd.NA
    df = df.dropna(subset=s)
    print('subset', s, '-> shape', df.shape, 'sexo counts', df['sexo'].astype(str).str.lower().value_counts().to_list())
