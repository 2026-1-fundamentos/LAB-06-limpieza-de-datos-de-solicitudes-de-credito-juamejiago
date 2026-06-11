import pandas as pd
pd.set_option('display.max_rows',200)
df=pd.read_csv('files/input/solicitudes_de_credito.csv',sep=';')
if df.columns[0]=='': df=df.drop(df.columns[0],axis=1)
for c in df.select_dtypes(include=['object']).columns:
    df[c]=df[c].astype(str).str.strip(); df.loc[df[c].str.lower()=='nan',c]=pd.NA
req = ['sexo','tipo_de_emprendimiento','idea_negocio','barrio','estrato','comuna_ciudadano','monto_del_credito','línea_credito']
df_req = df.dropna(subset=req).copy()
com = df_req['comuna_ciudadano'].astype(str).str.extract(r"(\d+)")[0]
invalid = ['50','60','70','80','90']
mask = com.isin(invalid) & (df_req['línea_credito'].astype(str).str.lower()=='microempresarial')
print('invalid & microempresarial count', int(mask.sum()))
print('breakdown by comuna:', df_req.loc[mask,'comuna_ciudadano'].astype(str).value_counts().to_dict())
