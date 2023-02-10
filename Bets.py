import pandas as pd

# Se trabajara con las filas como predominantes en victorias y demás

# def quitarnan_listas(lista):
#     lista2 = [[y for y in x if pd.notna(y)] for x in lista.values.tolist()]
#     return lista2
#
def puntos_equipo(WBDict,Header,Victorias):
    Points = {}  # Diccionario de equipos con sus respectivos puntos de victorias
    for num0, q in enumerate(Header):
        Sum = Victorias[q]
        for num, x in enumerate(WBDict[q].keys()):
            if WBDict[q][x] == "G":
                # print(x,WBDict[q][x])
                Sum = Sum + Victorias[x]
            Points[q] = Sum
    return Points
def Victorias_equipo(WBDict,Header):


    Wins = {}  # Diccionario de equipos con sus respectivos puntos de victorias
    for num0, q in enumerate(Header):
        Sum = 0
        for num, x in enumerate(WBDict[q].keys()):
            if WBDict[q][x] == "G":
                # print(x,WBDict[q][x])
                Perdedor = x
                Sum = Sum + 1
            Wins[q] = Sum
    return Wins

WB = pd.read_excel('bets.xlsx',index_col=0, header=0).transpose()
WBDict = WB.to_dict()
Header = list(WB.to_dict().keys())
Victorias = Victorias_equipo(WBDict,Header)


Puntos = puntos_equipo(WBDict,Header,Victorias)


print(pd.DataFrame.from_dict(Puntos, orient='index', columns=['Puntos']))
# print(pd.DataFrame.from_dict(Victorias, orient='index', columns=['Wins']))


