import pandas as pd
from itertools import combinations

expected = {'femenino':6617,'masculino':3589}

# load and apply initial cleaning as in pregunta_01 up to required drop
df = pd.read_csv('files/input/solicitudes_de_credito.csv', sep=';')
if df.columns[0]=='':
    df = df.drop(df.columns[0], axis=1)

df = df.drop_duplicates()
obj_cols = df.select_dtypes(include=['object']).columns.tolist()
for c in obj_cols:
    df[c] = df[c].astype(str).str.strip()
    df.loc[df[c].str.lower() == 'nan', c] = pd.NA

required = ["sexo", "tipo_de_emprendimiento", "idea_negocio", "barrio", "estrato", "comuna_ciudadano", "monto_del_credito", "línea_credito"]
df_req = df.dropna(subset=required).copy()

# examine unique comuna codes
com_codes = df_req['comuna_ciudadano'].astype(str).str.extract(r"(\d+)")[0].dropna().unique().tolist()
com_invalid = [c for c in com_codes if int(c) not in range(1,22)]
com_invalid_sorted = sorted([int(x) for x in com_invalid])
print('invalid codes present:', com_invalid_sorted)
vals = sorted([int(x) for x in com_invalid])

found = []
for r in range(0, len(vals)+1):
    for comb in combinations(vals, r):
        comb_str = [str(x) for x in comb]
        com = df_req['comuna_ciudadano'].astype(str).str.extract(r"(\d+)")[0]
        df2 = df_req[~com.isin(comb_str)]
        counts = df2['sexo'].astype(str).str.lower().value_counts()
        f = int(counts.get('femenino',0))
        m = int(counts.get('masculino',0))
        if f==expected['femenino'] and m==expected['masculino']:
            print('Found comb', comb)
            found.append(comb)

print('done, found combos:', found)
