import pandas as pd
from itertools import combinations
orig = pd.read_csv('files/input/solicitudes_de_credito.csv', sep=';')
# normalize strings
for c in orig.select_dtypes(include=['object']).columns:
    orig[c] = orig[c].astype(str).str.strip()
    orig.loc[orig[c].str.lower()=='nan', c] = pd.NA
# drop rows with missing tipo or barrio
base = orig.dropna(subset=['tipo_de_emprendimiento','barrio']).copy()
print('after dropping missing tipo/barrio', base.shape)
vals=[50,60,70,80,90]
found=[]
for r in range(0,6):
    for comb in combinations(vals, r):
        df=base.copy()
        if comb:
            com= df['comuna_ciudadano'].astype(str).str.extract(r"(\d+)")[0]
            df = df[~com.isin([str(x) for x in comb])]
        # try remove rows with unparseable fecha
        parsed = pd.to_datetime(df['fecha_de_beneficio'], dayfirst=True, errors='coerce')
        df_keep = df.copy()
        # two options: keep all, or drop unparseable
        for drop_unparse in (False, True):
            d = df_keep.copy()
            if drop_unparse:
                d = d[parsed.notna()]
            if d.shape[0]==10206:
                print('Found comb', comb, 'drop_unparse', drop_unparse)
                print('sex counts', d['sexo'].astype(str).str.lower().value_counts().to_list())
                found.append((comb, drop_unparse))
print('done', found)
