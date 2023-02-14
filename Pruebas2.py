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
    equiposQueHaPerdido = []
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
    # puntosDeFuerza = len(equiposQueHaGanado)
    puntosDeDebilidad = 0
    puntosDeFuerza = 0
    equiposQueHaEmpatadoNombre = []
    equiposQueHaGanadoNombre = []
    equiposQueHaPerdidoNombre = []

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

    def transformData(self):
        self.equiposQueHaGanadoNombre = [tm.name for tm in self.equiposQueHaGanado]
        self.equiposQueHaPerdidoNombre = [tm.name for tm in self.equiposQueHaPerdido]
        self.equiposQueHaEmpatadoNombre = [tm.name for tm in self.equiposQueHaEmpatado]

    def getDataframe(self):  # de los valores que estoy trabajando, los meto en un dataframe para manejarlos mejor
        self.transformData()
        recopilacionequipo = [
            self.columnaPosiciones,
            self.name,
            self.puntos,
            self.partidos,
            self.wins,
            self.draws,
            self.loses,
            self.afavor,
            self.encontra,
            self.equiposQueHaGanadoNombre,
            self.equiposQueHaPerdidoNombre,
            self.equiposQueHaEmpatadoNombre,
            self.golesAfavorUltimasJornadas,
            self.golesEncontraUltimasJornadas,
            self.maximosGoles,
            self.minimosGoles,
            self.maximosGolesEnContra,
            self.minimosGolesEnContra,
            self.mediaGolPorPartidoMarcados,
            self.mediaGolPorPartidoEnContra,
            self.puntosDeFuerza,
            self.puntosDeDebilidad
                              ]
        recopilacionequipo = pd.DataFrame(recopilacionequipo).transpose()
        return recopilacionequipo

def getEquipo(teamName, listaDeEquipos):
    for b in listaDeEquipos:
        if b.name == teamName:
            return b

# Lets start the program searching for Data in website
page = requests.get('https://www.resultados-futbol.com/primera')    #Get URL
soup = BeautifulSoup(page.text, 'html.parser')      #Use this format to read it

blockquote_items = soup.find('table', {'id': 'tabla2'})     #Use Bs4 to find specific data
blockquote_items = blockquote_items.find('tbody')
blockquote_items = blockquote_items.find_all('tr')


#Get name of teams and create a class for each one
listaDeEquipos = []
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

        teamObject = getEquipo(equipo,listaDeEquipos)
        newEnemyName = equipoContrario[0]
        newEnemyObject = getEquipo(newEnemyName,listaDeEquipos)
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
    # teamObject.calculateData()
    # print(teamObject.puntosDeFuerza)



def metodoFuerza(iter, teamToCheck, teamToAddPoints, teamsCountedAlready):
    if (iter <= 0): return
    # teamList = []
    for G in teamToCheck.equiposQueHaGanado:
        teamToAddPoints.puntosDeFuerza += 1
        if G in teamsCountedAlready:
            continue
        iter -= 1
        teamsCountedAlready.append(G)
        metodoFuerza(iter, G, teamToAddPoints, teamsCountedAlready)


def metodoDebilidad(iter, teamToCheck, teamToAddPoints, teamsCountedAlready):
    if (iter <= 0): return
    # teamList = []
    for L in teamToCheck.equiposQueHaGanado:
        teamToAddPoints.puntosDeDebilidad += 1
        if L in teamsCountedAlready:
            continue
        iter -= 1
        teamsCountedAlready.append(L)
        metodoDebilidad(iter, L, teamToAddPoints, teamsCountedAlready)




for team in listaDeEquipos:
    iter = 200
    metodoFuerza(iter, team, team, [])
    metodoDebilidad(iter, team, team, [])
    # print(team.name, team.puntosDeFuerza)
    # llamar al metood y ajustar los datos desde ahi




dataframetotal = pd.DataFrame()
for teamObject in listaDeEquipos:
    # Dataframes para posterior uso
    recopilacionDeDatos = teamObject.getDataframe()
    dataframetotal = pd.concat([dataframetotal, recopilacionDeDatos])
# Aplico header de los datos obtenidos
dataframetotal.columns = ["posicion", "nombre", "puntos", "partidos", "ganados", "empatados",
                          "perdidos", "afavor", "encontra", "Ha Ganado vs", "Ha perdido vs",
                          "Ha empatado vs", "golesAfavorUltimas5", "golesEnContraUltimas5",
                          "maximos goles marcados ultimos5",
                          "minimos goles marcados ultimos5", "maximos goles en contra ultimo5",
                          "minimos goles en contra ultimos5",
                          "media gol marcado ultimos5", "media gol en contra ultimos5","puntosFuerza", "puntosDebilidad"]
print(dataframetotal.to_string())
# print(dataframetotal[["nombre", "puntosFuerza"]])

# Obtener excel final
# dataframetotal.to_excel("output.xlsx", sheet_name = "Datos en vivo", index=0)


# Implementar:
# Grafica por cada quiepo con medias y desviaciones
# añadir metodologias de probabilidad para los datos recogidos
#
