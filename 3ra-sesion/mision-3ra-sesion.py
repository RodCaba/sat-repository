# MISIÓN 3RA SESIÓN
#%% DatSetNik.csv son los datos originales, queremos llegar a DataSetNike_sku.csv
import numpy as np
import pandas as pd

#DEFINE QUALITY REPORT TO GET INFO OF OUR DATA
def quality_report(data):

    """This method will do a basic data quality report for a data frame"""
        
    if (type(data) != pd.core.frame.DataFrame):
        raise TypeError("Data must be pandas.core.frame.DataFrame")
    else: 
        columns = list(data.columns.values)
        data_type = pd.DataFrame(data.dtypes, columns=['Data type'])
        missing_data = pd.DataFrame(
        data.isnull().sum(), columns=['missing values'])
        present_data = pd.DataFrame(data.count(), columns=['present values'])
        unique_values = pd.DataFrame(columns=['unique values'])
        minimum_values = pd.DataFrame(columns=['minimum values'])
        max_values = pd.DataFrame(columns=['maximun values'])
        
        for i in columns:
            unique_values.loc[i] = [data[i].nunique()]
            try:
                minimum_values.loc[i] = [data[i].min()]
                max_values.loc[i] = [data[i].max()]
            except:
                pass
        
        DQ_report = data_type.join(missing_data).join(present_data).join(
        unique_values).join(minimum_values).join(max_values)
    
    return DQ_report

## DESCARGAR DATOS ORIGINALES
csv_original = 'DataSetNike.csv'
dataset_original = pd.read_csv(csv_original, encoding = 'latin-1', low_memory = False)
dataset_original

quality_report(dataset_original)

#%% DATA MANIPULATION 

#%%SELECCIONAR COLUMNAS MATERIAL DATE Y UNITS

mision_dataset = dataset_original[['Date', 'Material', 'Units']]

#%% ELIMINAR REGISTROS DONDE VARIABLE MATERIAL ESTÁ VACÍA

mision_dataset = mision_dataset.dropna()

#%% ELIMINAR REGISTROS DONDE LA VARIABLE UNITS < 1

mision_dataset = mision_dataset[mision_dataset.Units >= 1]

#%% RENOMBRAR COLUMNA Material a CÓDIGO

mision_dataset = mision_dataset.rename(columns = {'Material' : 'CÓDIGO'})

#%% REVISAR QUE LOS DATOS SEAN LOS MISMOS QUE LO QUE PIDEN
quality_report(mision_dataset)

#Observamos que la columna Date esta en str, transformar a timestamp

import datetime as dt

mision_dataset['Date'] = pd.to_datetime(mision_dataset['Date'])
mision_dataset['Month'] = mision_dataset['Date'].dt.month
mision_dataset['AÑO'] = mision_dataset['Date'].dt.year



#mision_dataset = mision_dataset.sort_values(by = ['Month','AÑO'])




#%%PIVOT TABLE, RESET INDEX, RENAME A FORMATO ENE, FEB

temp = mision_dataset.pivot_table(values = 'Units', index = ['CÓDIGO', 'AÑO'], columns = 'Month',aggfunc = np.sum)
temp = temp.fillna(0)                                  

temp = temp.reset_index()
temp = temp.rename(columns = {1:'ENE.',2:'FEB.',3:'MAR.',4:'ABR.',5:'MAY.',6:'JUN.',7:'JUL.',8:'AGO.',9:'SEP',10:'OCT.',11:'NOV.',12:'DIC.'})

mision_dataset = temp.sort_values(['AÑO','CÓDIGO'])

del(temp)

print(quality_report(mision_dataset))
print(mision_dataset)
