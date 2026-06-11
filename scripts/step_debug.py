import pandas as pd
import numpy as np

p='files/input/solicitudes_de_credito.csv'
df=pd.read_csv(p, sep=';')
print('initial', df.shape)

# drop first col if unnamed
if df.columns[0]=='':
    df=df.drop(df.columns[0], axis=1)
print('after drop index col', df.shape)

# drop_duplicates
df = df.drop_duplicates()
print('after drop_duplicates', df.shape)

# normalize strings
obj_cols = df.select_dtypes(include=['object']).columns.tolist()
for c in obj_cols:
    df[c] = df[c].astype(str).str.strip()
    df.loc[df[c].str.lower()=='nan', c] = pd.NA
print('after normalize strings', df.shape)

# dropna subset required
required = ["sexo", "tipo_de_emprendimiento", "idea_negocio", "barrio", "estrato", "comuna_ciudadano", "fecha_de_beneficio", "monto_del_credito", "línea_credito"]
df1 = df.dropna(subset=required)
print('after dropna required', df1.shape)

# lowercase all text
for c in obj_cols:
    df1[c] = df1[c].astype(str).str.strip().str.lower()
print('after lower', df1.shape)

# clean monto
s = df1['monto_del_credito'].astype(str).str.replace(r"[\$\,]", "", regex=True).str.replace(r"\.00$", "", regex=True)
df1['monto_del_credito']=pd.to_numeric(s, errors='coerce')
df2 = df1.dropna(subset=['monto_del_credito'])
print('after monto numeric', df2.shape)

# estrato
df2['estrato'] = df2['estrato'].astype(str).str.extract(r"(\d+)")
df2['estrato'] = pd.to_numeric(df2['estrato'], errors='coerce').astype('Int64')
df3 = df2.dropna(subset=['estrato'])
print('after estrato numeric', df3.shape)

# comuna
df3['comuna_ciudadano'] = df3['comuna_ciudadano'].astype(str).str.extract(r"(\d+)")
df3['comuna_ciudadano'] = pd.to_numeric(df3['comuna_ciudadano'], errors='coerce').astype('Int64')
df4 = df3.dropna(subset=['comuna_ciudadano'])
print('after comuna numeric', df4.shape)

# fecha
df4['fecha_de_beneficio']=pd.to_datetime(df4['fecha_de_beneficio'], dayfirst=True, errors='coerce')
df5 = df4.dropna(subset=['fecha_de_beneficio'])
print('after fecha parse', df5.shape)

# final
print('final sexo counts', df5['sexo'].astype(str).str.lower().value_counts().to_list())

# show sample of rows dropped between steps
print('\nrows dropped between dropna required and after monto numeric:', set(df.index)-set(df2.index))
