# from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import requests


# from IPython.display import display

# Clasificacion de Equipos con sus respectivos datos
# de interes como puntos, victorias, equipos contrarios vencidos, etc..
class Equipo:
    # Agrego valores iniciales de los datos que me interesan de la pagina web como otros que quiera crear yo nuevos
    name = ""
    columnaPosiciones = 0
    puntos = 0
    partidos = 0
    wins = 0
    loses = 0
    draws = 0
    afavor = 0
    encontra = 0
    equiposQueHaGanado = []
    puntosFuerza = len(equiposQueHaGanado)
    equiposQueHaPerdido = []
    puntosDebilidad = len(equiposQueHaPerdido)
    equiposQueHaEmpatado = []
    puntosGanados = 0
    puntosPerdidos = 0
    puntosEmpatados = 0
    golesEncontraUltimasJornadas = 0
    golesAfavorUltimasJornadas = 0
    maximosGoles = 0
    minimosGoles = 0
    maximosGolesEnContra = 0
    minimosGolesEnContra = 0
    mediaGolPorPartidoMarcados = 0
    mediaGolPorPartidoEnContra = 0

    def getDataframe(self):  # de los valores que estoy trabajando, los meto en un dataframe para manejarlos mejor
        recopilacionequipo = [
            self.columnaPosiciones,
            self.name,
            self.puntos,
            partidos,
            wins,
            draws,
            loses,
            afavor,
            encontra,
            equiposQueHaGanado,
            self.equiposQueHaPerdido,
            equiposQueHaEmpatado,
            golesAfavorUltimasJornadas,
            golesEncontraUltimasJornadas,
            maximosGoles,
            minimosGoles,
            maximosGolesEnContra,
            minimosGolesEnContra,
            mediaGolPorPartidoMarcados,
            mediaGolPorPartidoEnContra
                              ]
        recopilacionequipo = pd.DataFrame(recopilacionequipo).transpose()
        return recopilacionequipo

    def __init__(self, name, columnasPosiciones = 0, puntos = 0, partidos = 0, wins = 0,
                 draws = 0, loses = 0, afavor = 0, encontra = 0, ganados = [], perdidos = [], empatados = [],
                 golesAfavorUltimasJornadas = 0, golesEncontraUltimasJornadas = 0, maximosGoles = 0, minimosGoles = 0,
                 maximosGolesEnContra = 0, minimosGolesEnContra = 0, mediaGolPorPartidoMarcados = 0,
                 mediaGolPorPartidoEnContra = 0):  # Llamo a los datos que me interan ya inicializados y les añado el valor que he dado en la entrada de la clase
        self.name = name
        self.setvalues(columnasPosiciones, puntos, partidos , wins ,
                 draws , loses, afavor, encontra, ganados, perdidos, empatados ,
                 golesAfavorUltimasJornadas, golesEncontraUltimasJornadas , maximosGoles, minimosGoles ,
                 maximosGolesEnContra, minimosGolesEnContra , mediaGolPorPartidoMarcados,
                 mediaGolPorPartidoEnContra )
    def setvalues(self, columnasPosiciones = 0, puntos = 0, partidos = 0, wins = 0,
                 draws = 0, loses = 0, afavor = 0, encontra = 0, ganados = [], perdidos = [], empatados = [],
                 golesAfavorUltimasJornadas = 0, golesEncontraUltimasJornadas = 0, maximosGoles = 0, minimosGoles = 0,
                 maximosGolesEnContra = 0, minimosGolesEnContra = 0, mediaGolPorPartidoMarcados = 0,
                 mediaGolPorPartidoEnContra = 0 ):  # Llamo a los datos que me interan ya inicializados y les añado el valor que he dado en la entrada de la clase
        self.columnaPosiciones = columnasPosiciones
        self.puntos = puntos
        self.partidos = partidos
        self.wins = wins
        self.loses = loses
        self.draws = draws
        self.afavor = afavor
        self.encontra = encontra
        self.equiposQueHaGanado = ganados
        self.equiposQueHaPerdido = perdidos
        self.equiposQueHaEmpatado = empatados
        self.golesAfavorUltimasJornadas = golesAfavorUltimasJornadas
        self.golesEncontraUltimasJornadas = golesEncontraUltimasJornadas
        self.maximosGoles = maximosGoles
        self.minimosGoles = minimosGoles
        self.maximosGolesEnContra = maximosGolesEnContra
        self.minimosGolesEnContra = minimosGolesEnContra
        self.mediaGolPorPartidoMarcados = mediaGolPorPartidoMarcados
        self.mediaGolPorPartidoEnContra = mediaGolPorPartidoEnContra

page = requests.get('https://www.resultados-futbol.com/primera')
soup = BeautifulSoup(page.text, 'html.parser')

blockquote_items = soup.find('table', {'id': 'tabla2'})
blockquote_items = blockquote_items.find('tbody')
blockquote_items = blockquote_items.find_all('tr')
listaDeEquipos = []
dataframetotal = pd.DataFrame()
def getEquipo(teamName):
    for b in listaDeEquipos:
        if b.name == teamName:
            return b

for num, blockquote in enumerate(blockquote_items):
    equipo = blockquote.find("td", {"class": ["equipo", "equipo sube", "equipo baja"]}).find('a').contents[0]
    team = Equipo(equipo)
    listaDeEquipos.append(team)
# del bloque buscado empiezo a obtener los datos
for num, blockquote in enumerate(blockquote_items):
    # con cada equipo poner su fila en horizontal todos los datos, escribo todas las opciones para que recoga los datos
    columnaPosiciones = \
        blockquote.find("th",
                        {"class": ["pos2 pos-cha", "pos3 pos-uefa", "pos5 pos-conf", "", "pos6 pos-desc"]}).contents[0]
    equipo = blockquote.find("td", {"class": ["equipo", "equipo sube", "equipo baja"]}).find('a').contents[0]
    puntos = blockquote.find("td", {"class": "pts"}).contents[0]
    partidos = blockquote.find("td", {"class": "pj"}).contents[0]
    wins = blockquote.find("td", {"class": "win"}).contents[0]
    draws = blockquote.find("td", {"class": "draw"}).contents[0]
    loses = blockquote.find("td", {"class": "lose"}).contents[0]
    afavor = blockquote.find("td", {"class": "f"}).contents[0]
    encontra = blockquote.find("td", {"class": "c"}).contents[0]

    resultadopartidos = blockquote.find_all("span", {"class": "classicsmall"})
    equiposQueHaGanado = []
    equiposQueHaperdido = []
    equiposQueHaEmpatado = []
    golesAfavorUltimasJornadas = 0
    golesEncontraUltimasJornadas = 0
    minimosGoles = 100
    maximosGoles = 0
    minimosGolesEnContra = 100
    maximosGolesEnContra = 0
    for x, resultado in enumerate(resultadopartidos):
        if x == 0: continue
        resultadoDelPartido = resultado.find("li", {"class": "title g"}).contents[0]
        equiposDelPartido = resultado.find_all("b", {"class": "bname"})
        ambosEquipos = [b.get_text() for b in equiposDelPartido]
        equipoContrario = ambosEquipos.copy()
        equipoContrario.remove(equipo)
        golesDelPartido = resultado.find_all("b", {"class": "bres"})
        golesDeAmbos = [b.get_text() for b in golesDelPartido]
        equiposYgoles = dict(map(lambda i, j: (i, j), ambosEquipos, golesDeAmbos))

        if int(equiposYgoles[equipo]) > maximosGoles: maximosGoles = int(equiposYgoles[equipo])
        if int(equiposYgoles[equipo]) < minimosGoles: minimosGoles = int(equiposYgoles[equipo])
        if int(equiposYgoles[equipoContrario[0]]) > maximosGolesEnContra: maximosGolesEnContra = int(
            equiposYgoles[equipoContrario[0]])
        if int(equiposYgoles[equipoContrario[0]]) < minimosGolesEnContra: minimosGolesEnContra = int(
            equiposYgoles[equipoContrario[0]])

        golesAfavorUltimasJornadas = golesAfavorUltimasJornadas + int(equiposYgoles[equipo])
        golesEncontraUltimasJornadas = golesEncontraUltimasJornadas + int(equiposYgoles[equipoContrario[0]])

        teamObject = getEquipo(equipo)
        newEnemyName = equipoContrario[0]
        newEnemyObject = getEquipo(newEnemyName)
        if resultadoDelPartido == 'VICTORIA':
            equiposQueHaGanado.append(newEnemyObject)
        if resultadoDelPartido == 'DERROTA':
            equiposQueHaperdido.append(newEnemyObject)
        if resultadoDelPartido == 'EMPATE':
            equiposQueHaEmpatado.append(newEnemyObject)



    numDePartidos = len(equiposQueHaGanado) + len(equiposQueHaperdido) + len(equiposQueHaEmpatado)
    mediaGolPorPartidoMarcados = golesAfavorUltimasJornadas / numDePartidos
    mediaGolPorPartidoEnContra = golesEncontraUltimasJornadas / numDePartidos

    teamObject.setvalues(columnaPosiciones, puntos, partidos, wins, draws, loses,
              afavor, encontra, equiposQueHaGanado, equiposQueHaperdido, equiposQueHaEmpatado,
              golesAfavorUltimasJornadas, golesEncontraUltimasJornadas, maximosGoles, minimosGoles,
              maximosGolesEnContra, minimosGolesEnContra, mediaGolPorPartidoMarcados, mediaGolPorPartidoEnContra)

    # Dataframes para posterior uso
    recopilacionDeDatos = teamObject.getDataframe()
    dataframetotal = pd.concat([dataframetotal, recopilacionDeDatos])
    # listaDeEquipos.append(Data)

# Aplico header de los datos obtenidos
dataframetotal.columns = ["posicion", "nombre", "puntos", "partidos", "ganados", "empatados",
                          "perdidos", "afavor", "encontra", "Ha Ganado vs", "Ha perdido vs",
                          "Ha empatado vs", "golesAfavorUltimas5", "golesEnContraUltimas5",
                          "maximos goles marcados ultimos5",
                          "minimos goles marcados ultimos5", "maximos goles en contra ultimo5",
                          "minimos goles en contra ultimos5",
                          "media gol marcado ultimos5", "media gol en contra ultimos5"]

def metodoFuerzaYDebilidad(team):
    # print(team.puntosFuerza)
    print("")
    #Cojo este nombre, cojo su fila de datos, le añado puntos corresondientes, y busco en sus ganados y en sus perdidos a quien ha ganado y perdido, dentro de este bucle vuelvo a llamar a la funcion
    # for eq in team.equiposQueHaGanado:
        # team.puntosFuerza = team.puntosFuerza + eq
        # team.puntosDebilidad = team.puntosDebilidad +
    # team.equiposQueHaPerdido
    # team.puntosFuerza = team.puntosFuerza +
    # team.puntosDebilidad


    # fila = datosMetodo.loc[datosMetodo[datosRelevantes[0]] == team]
    # print(fila.to_string())
    # puntosDeFuerza = len(fila[haGanado][0])
    # puntosDeDebilidad = len(fila[haPerdido][0])
    # if puntosDeFuerza != 0:
    #     #puntos Fuerza
    #     for teamG in fila[haGanado]:
    #         puntosDeFuerza = puntosDeFuerza + metodoFuerzaYDebilidad(dataframeDeDatos, teamG,haGanado, haPerdido)
    #         # print(puntosDeFuerza)
    #         break
    # if puntosDeDebilidad != 0:
    #     #puntos Debilidad
    #     for teamP in fila[haPerdido]:
    #         puntosDeFuerza = puntosDeFuerza + len(row["Ha Ganado vs"])
    #         # print(puntosDeFuerza)
    #         break

datosRelevantes = ["nombre", "Ha Ganado vs", "Ha perdido vs", "Ha empatado vs"]
haPerdio = "Ha perdido vs"
haGanado = "Ha Ganado vs"
datosMetodo = dataframetotal[datosRelevantes].copy()
listaDePuntosDeFuerza = []
listaDePuntosDeDebilidad = []
for team in listaDeEquipos:
    metodo0 = metodoFuerzaYDebilidad(team)
    # llamar al metood y ajustar los datos desde ahi
    # print(team.name)
    break


    # print(dataframetotal[datosRelevantes].to_string())


print(dataframetotal.to_string())

# Obtener excel final
# dataframetotal.to_excel("output.xlsx", sheet_name = "Datos en vivo", index=0)


# Implementar:
# Grafica por cada quiepo con medias y desviaciones
# añadir metodologias de probabilidad para los datos recogidos
#
