from homework.pregunta_01 import pregunta_01
import pandas as pd
import os

pregunta_01()
path='files/output/solicitudes_de_credito.csv'
print('exists', os.path.exists(path))
df=pd.read_csv(path, sep=';')
print('rows', len(df))
print('sexo', df.sexo.value_counts().to_list()[:5])
print('tipo', df.tipo_de_emprendimiento.value_counts().to_list()[:5])
print('linea', df['línea_credito'].value_counts().to_list()[:5])
