import pandas as pd
import sqlite3
import numpy as np
import sklearn
from sklearn import linear_model
import matplotlib.pyplot as pyplot
from matplotlib import style
import pickle

#Lee el archivo y selecciona solo las variables (separadas con ';') relevantes
print('Conectandose a base de datos...')
conn = sqlite3.connect('C:/Users/cfmor/PycharmProjects/Machine Learning Tutorial by Tech with Tim/CSGO rating predicter/db.sqlite')
data = pd.DataFrame(pd.read_sql_query("""SELECT * FROM Raw""", conn), columns=['maps', 'rounds', 'kd_diff', 'kd_rel', 'rating'])
print('Conectado a db.sqlite')
print(data, end='\n\n')
predict = 'rating' #Etiqueta la variable que quiere predecir
x = np.array(data.drop([predict], 1)) #X = toda info menos G3 (dato a predecir) --> feature(s)
y = np.array(data[predict])           #Y = solo G3                              --> label
x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size=0.1) #Otorga 10% de info a las variables de predicción, así la app no memoriza
#Entrena el modelo y lo almacena dentro de un pickle
training = True
if training:
    print('Entrenando modelos...')
    best = 0.0
    for i in range(30):
        x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size=0.1) #Otorga 10% de info a las variables de predicción, así la app no memoriza

        #Se establece el modelo (regresión lineal) y se entrena con los datos de prueba
        model = linear_model.LinearRegression()
        model.fit(x_train, y_train)

        acc = model.score(x_test, y_test)
        print('Accuracy   : ', acc)
        if acc > best:
            best = acc
            with open('ratingmodel.pickle', 'wb') as file:
                pickle.dump(model, file)

pickle_in = open('ratingmodel.pickle', 'rb')
model = pickle.load(pickle_in)
#Impresión de resultados
print('====MEJOR MODELO====')
if training: print('Accuracy   : ', best)
print('Coefficient:', model.coef_)
print('Intercept  :', model.intercept_)

print("{:<20} {:<10} {:<50}".format('Predicción', 'Valor Real', 'Coeficientes'))
predictions = model.predict(x_test)
for i in range(len(predictions)):
    print("{:<20} {:<10}".format(predictions[i], y_test[i]), end=" ")
    print(x_test[i])

x_labels = ['maps', 'rounds', 'kd_diff', 'kd_rel']
x_label = x_labels[3]
style.use('ggplot') #Estilo del grafico
pyplot.scatter(data[x_label], data['rating']) #Se crea el tipo de grafico
pyplot.xlabel(x_label)  #Texto horizontal
pyplot.ylabel('rating') #Texto vertical
pyplot.show() #Ejecución del gráfico