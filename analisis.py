import pandas as pd
from matplotlib import pyplot as plt
from uncertainties import ufloat,unumpy
from uncertainties.umath import *
from sklearn.linear_model import LinearRegression

df1=pd.read_csv('tabla_1.csv')
df2=pd.read_csv('tabla_2.csv')
print(df1.dtypes)

def ajuste_1():
    x = df1.I.values.reshape(10, 1)
    y = df1.Angulo.values.reshape(10, 1)
    print(calcula_media(x,0.005))
    print(calcula_media(y, 1))
    df1['campo']=calcula_campo(x,y)
    print(df1)
    plot(x,y,1)

def ajuste_2():
    x = df2.Numero_vueltas.values.reshape(3, 1)
    y = df2.Angulo.values.reshape(3, 1)
    plot(x,y,2)


def plot(x,y,i):
    regr = LinearRegression()
    regr.fit(x, y)
    plt.scatter(x, y, color='black')
    plt.xlabel(f'{"I(A)" if i==1 else "Número de vueltas"}')
    plt.ylabel('Ángulo (°)')
    plt.plot(x, regr.predict(x), color='blue', linewidth=3, )
    plt.title(f'intercepto:{round(regr.intercept_[0], 3)} Coeficiente:{round(regr.coef_[0][0], 3)}')
    #plt.savefig(f'ajuste{i}.png')
    plt.show()
    plt.clf()

def export_latex():
    #Se añade cláusula Try por posible excepción al añadir incertidumbres al dataframe
    try:
        df1['I']=list(map(lambda x: ufloat(x,0.005),df1.I.values))
        df1['Angulo']=list(map(lambda x: ufloat(x,1),df1.Angulo.values))
        df2['Angulo']=list(map(lambda x: ufloat(x, 1), df2.Angulo.values))
    except Exception:
        pass
    return df1.to_latex(index=False), df2.to_latex(index=False)

def calcula_media(x,incert):
    arr1=unumpy.uarray(x,[incert for _ in range(10)])
    return arr1.mean()

def calcula_campo(i,an):
    i=list(map(lambda x: ufloat(x,0.005),i))
    an=list(map(lambda x: ufloat(x,1),an))
    resultado=[(15*i[n]*4*3.141592*0.0000001)/(2*0.0635*tan(an[n]*3.141592/180)) for n in range(10)]
    return resultado
  
ajuste_1()
#print(f'{export_latex()[0]}\n {export_latex()[1]}')
