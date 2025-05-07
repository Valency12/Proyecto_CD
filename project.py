#pip install openai==0.28 (instalalo primero)
import numpy as np
import pandas as pd 

import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error

# ANALISIS EXPLORATORIO DE DATOS
students = pd.read_csv('students_dropout_academic_success.csv')
print(students.head()) #primeras 4 filas
print(students.info()) #informacion de los datos
print(students.describe()) #estadisticas de los datos
#print(students.shape()) #dimensiones de los datos

#Histograma Admission grade
admission = students['Admission grade']
plt.figure(figsize=(10, 6))
sns.histplot(admission, kde=False, bins=10)
plt.title(f'Histograma de {admission.name}')
plt.xlabel(admission.name)
plt.ylabel('Frecuencia')
plt.show()

#Histograma Previus grade
previous = students['Previous qualification']
plt.figure(figsize=(10, 6))
sns.histplot(previous, kde=False, bins=10)
plt.title(f'Histograma de {previous.name}')
plt.xlabel(previous.name)
plt.ylabel('Frecuencia')
plt.show()






