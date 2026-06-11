import pandas as pd
req=['sexo','tipo_de_emprendimiento','idea_negocio','barrio','estrato','comuna_ciudadano','fecha_de_beneficio','monto_del_credito','línea_credito']
df=pd.read_csv('files/input/solicitudes_de_credito.csv',sep=';')
print('input shape', df.shape)
for c in req:
    s=df[c].astype(str).str.strip()
    n_empty=(s=='').sum()
    n_null=s.isna().sum()
    print(c, 'empty', n_empty, 'na', n_null)

# show some example rows with empty fields
print('\nRows with empty barrio sample:')
print(df[df['barrio'].astype(str).str.strip()==""].head(5))
print('\nRows with non-numeric estrato sample:')
print(df[~df['estrato'].astype(str).str.extract(r"(\\d+)")[0].notna()].head(5))
