import pandas as pd
orig=pd.read_csv('files/input/solicitudes_de_credito.csv',sep=';')
estr=orig['estrato'].astype(str).str.extract(r"(\d+)")[0]
estr_num=pd.to_numeric(estr, errors='coerce')
mask=(estr_num<1)|(estr_num>6)|estr_num.isna()
print('rows with estrato invalid:', int(mask.sum()))
print('sexo counts among invalid estrato:', orig.loc[mask,'sexo'].astype(str).str.strip().str.lower().value_counts().to_dict())
