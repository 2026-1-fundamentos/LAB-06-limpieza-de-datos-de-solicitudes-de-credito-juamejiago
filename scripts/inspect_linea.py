import pandas as pd
pd.set_option('display.max_rows',200)
df=pd.read_csv('files/input/solicitudes_de_credito.csv',sep=';')
if df.columns[0]=='':
    df=df.drop(df.columns[0],axis=1)
obj_cols = df.select_dtypes(include=['object']).columns.tolist()
for c in obj_cols:
    df[c]=df[c].astype(str).str.strip()
    df.loc[df[c].str.lower()=='nan', c]=pd.NA
required = ['sexo','tipo_de_emprendimiento','idea_negocio','barrio','estrato','comuna_ciudadano','monto_del_credito','línea_credito']
df_req = df.dropna(subset=required).copy()
print('df_req shape', df_req.shape)
print(df_req['línea_credito'].astype(str).str.lower().value_counts())
