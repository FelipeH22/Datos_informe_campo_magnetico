import pandas as pd
from matplotlib import pyplot as plt
from uncertainties import ufloat,unumpy
from uncertainties.umath import *
from sklearn.linear_model import LinearRegression

df1=pd.read_csv('tabla_1.csv')
df2=pd.read_csv('tabla_2.csv')

def ajuste_1():
    x = df1.I.values.reshape(10, 1)
    y = df1.Angulo.values.reshape(10, 1)
    df1['campo_e']=calcula_campo(x,y,0)[1]
    df1['campo_t'] = calcula_campo(x, y, 1)[1]
    campo_t = df1.campo_t.values.reshape(10, 1)
    campo_e = df1.campo_e.values.reshape(10, 1)
    plot(x,y,1)
    plot_campo(x,campo_t,1)
    plot_campo(x,campo_e,0)
    plot_campo(campo_e,campo_t,3)
    print(export_latex(x,y))

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
    plt.savefig(f'ajuste{i}.png')
    plt.show()
    plt.clf()

def plot_campo(x,y,i):
    plt.clf()
    regr = LinearRegression()
    regr.fit(x, y)
    plt.scatter(x, y, color='black')
    plt.xlabel(f'{"Campo magnético espira (T)" if i==3 else "I(A)"}')
    plt.ylabel(f'Campo magnético {"tierra" if i==1 or i==3 else "espira"} (T)')
    plt.plot(x, regr.predict(x), color='blue', linewidth=3, )
    plt.title(f'intercepto:{"{0:.2E}".format(regr.intercept_[0])} Coeficiente:{"{0:.2E}".format(regr.coef_[0][0])}')
    if i!=3: plt.savefig(f'ajuste_campo_{"tierra" if i==1 else "espira"}.png')
    else: plt.savefig(f'ajuste_campos.png')
    plt.show()
    plt.clf()

def export_latex(x,y):
    #Se añade cláusula Try por posible excepción al añadir incertidumbres al dataframe
    try:
        df1['I']=list(map(lambda x: ufloat(x,0.005),df1.I.values))
        df1['Angulo']=list(map(lambda x: ufloat(x,1),df1.Angulo.values))
        df1['campo_t']=calcula_campo(x,y,1)[0]
        df1['campo_e']=calcula_campo(x,y,0)[0]
        #df2['Angulo']=list(map(lambda x: ufloat(x,1), df2.Angulo.values))
    except Exception:
        pass
    return df1.to_latex(index=False)#, df2.to_latex(index=False)

def calcula_campo(i,an,tipo):
    #tipo==1: campo magnético de la tierra, campo magnético de la espira e.o.c.
    i=list(map(lambda x: ufloat(x,0.005),i))
    an=list(map(lambda x: ufloat(x,1),an))
    if tipo==1: resultado=[(15*i[n]*4*3.141592*0.0000001)/(2*0.0635*tan(an[n]*3.141592/180)) for n in range(10)]
    else: resultado=[(15*i[n]*4*3.141592*0.0000001)/(2*0.0635) for n in range(10)]
    clean_res=list(map(lambda x:x.nominal_value,resultado))
    sta_dev=list(map(lambda x:x.std_dev,resultado))
    media=unumpy.uarray(clean_res,sta_dev)
    print(f'media campo magnético {"terrestre" if tipo==1 else "espira"} {media.mean()}')
    return resultado,clean_res
  
ajuste_1()
#print(f'{export_latex()[0]}\n {export_latex()[1]}')
