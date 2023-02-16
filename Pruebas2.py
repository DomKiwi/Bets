# from selenium import webdriver
import itertools

from bs4 import BeautifulSoup
import pandas as pd
import requests
import time
import matplotlib.pyplot as plt
from random import randrange
import numpy as np
import openpyxl as pxl
import os
import zipfile
import atexit


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

    def __init__(self, name, columnasPosiciones=0, puntos=0, partidos=0, wins=0,
                 draws=0, loses=0, afavor=0, encontra=0, ganados=[], perdidos=[], empatados=[],
                 golesAfavorUltimasJornadas=0, golesEncontraUltimasJornadas=0, maximosGoles=0, minimosGoles=0,
                 maximosGolesEnContra=0, minimosGolesEnContra=0, mediaGolPorPartidoMarcados=0,
                 mediaGolPorPartidoEnContra=0):  # Llamo a los datos que me interan ya inicializados y les añado el valor que he dado en la entrada de la clase
        self.name = name
        self.setvalues(columnasPosiciones, puntos, partidos, wins,
                       draws, loses, afavor, encontra, ganados, perdidos, empatados,
                       golesAfavorUltimasJornadas, golesEncontraUltimasJornadas, maximosGoles, minimosGoles,
                       maximosGolesEnContra, minimosGolesEnContra, mediaGolPorPartidoMarcados,
                       mediaGolPorPartidoEnContra)

    def setvalues(self, columnasPosiciones=0, puntos=0, partidos=0, wins=0,
                  draws=0, loses=0, afavor=0, encontra=0, ganados=[], perdidos=[], empatados=[],
                  golesAfavorUltimasJornadas=0, golesEncontraUltimasJornadas=0, maximosGoles=0, minimosGoles=0,
                  maximosGolesEnContra=0, minimosGolesEnContra=0, mediaGolPorPartidoMarcados=0,
                  mediaGolPorPartidoEnContra=0):  # Llamo a los datos que me interan ya inicializados y les añado el valor que he dado en la entrada de la clase
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
        recopilacionImportanteEquipo = [
            self.name,
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
        recopilacionImportanteEquipo = pd.DataFrame(recopilacionImportanteEquipo).transpose()

        recopilacionequipo.columns = [
            "posicion",
            "nombre",
            "puntos",
            "partidos",
            "ganados",
            "empatados",
            "perdidos",
            "afavor",
            "encontra",
            "Ha Ganado vs",
            "Ha perdido vs",
            "Ha empatado vs",
            "golesAfavorUltimas5",
            "golesEnContraUltimas5",
            "maximos goles marcados ultimos5",
            "minimos goles marcados ultimos5",
            "maximos goles en contra ultimo5",
            "minimos goles en contra ultimos5",
            "media gol marcado ultimos5",
            "media gol en contra ultimos5",
            "puntosFuerza",
            "puntosDebilidad"
        ]
        recopilacionImportanteEquipo.columns = [
            "nombre",
            "golesAfavorUltimas5",
            "golesEnContraUltimas5",
            "maximos goles marcados ultimos5",
            "minimos goles marcados ultimos5",
            "maximos goles en contra ultimo5",
            "minimos goles en contra ultimos5",
            "media gol marcado ultimos5",
            "media gol en contra ultimos5",
            "puntosFuerza",
            "puntosDebilidad"
        ]
        return recopilacionequipo, recopilacionImportanteEquipo


####################################################################################################################################################################
# Create excel to write data call it more times if I want
class excelWriter:
    writerName = ''
    def __init__(self,writerName, data = pd.DataFrame(),nameSheet = ''):
        self.writerName = writerName
        self.writer = pd.ExcelWriter(writerName, engine='openpyxl')
    def excelWriterFunction(self, data, nameSheet):
        data.to_excel(self.writer, sheet_name=nameSheet, index=0)
    def closingProgram(self):
        self.writer.close()
        print('Guardando el excel de datos pedidos')
excelGlobal = excelWriter('Output.xlsx')

####################################################################################################################################################################
# MODULES
def getEquipo(teamName, listaDeEquipos):
    for b in listaDeEquipos:
        if b.name == teamName:
            return b


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
    for L in teamToCheck.equiposQueHaPerdido:
        teamToAddPoints.puntosDeDebilidad += 1
        if L in teamsCountedAlready:
            continue
        iter -= 1
        teamsCountedAlready.append(L)
        metodoDebilidad(iter, L, teamToAddPoints, teamsCountedAlready)


# def excelWriter(data, nameSheet):
#     # Start excel writer
#     if not os.path.exists('Output.xlsx'):
#         data.to_excel('Output.xlsx', sheet_name=nameSheet, index = 0)
#         print('hola')
#     else:
#
#         excel_book = pxl.load_workbook('Output.xlsx')
#         excel_book.create_sheet(nameSheet)
#         ws = pd.ExcelWriter('Output.xlsx', engine = 'openpyxl')
#         ws.book = excel_book
#         # ws = excel_book[nameSheet]
#         # writer = pd.ExcelWriter('Output.xlsx', engine='openpyxl')
#         # writer.book = pxl.load_workbook('Output.xlsx')
#         data.to_excel(ws, sheet_name=nameSheet, index=0)
#         # excel_book.save()
#         # excel_book.close()


# with zipfile.ZipFile("Output.zip", "w") as zf:
#     # in open function specify the name in which
#     # the excel file has to be stored
#     with zf.open("Output.xlsx", "w") as buffer:
#         with pd.ExcelWriter(buffer) as writer:
#             # use to_excel function and specify the sheet_name and
#             # index to store the dataframe in specified sheet
#             data.to_excel(writer, sheet_name=nameSheet, index=False)
####################################################################################################################################################################
# Lets start the program searching for Data in website
page = requests.get('https://www.resultados-futbol.com/primera')  # Get URL
soup = BeautifulSoup(page.text, 'html.parser')  # Use this format to read it

blockquote_items = soup.find('table', {'id': 'tabla2'})  # Use Bs4 to find specific data
blockquote_items = blockquote_items.find('tbody')
blockquote_items = blockquote_items.find_all('tr')

# Get name of teams and create a class for each one
listaDeEquipos = []
for num, blockquote in enumerate(blockquote_items):
    equipo = blockquote.find("td", {"class": ["equipo", "equipo sube", "equipo baja"]}).find('a').contents[0]
    team = Equipo(equipo)
    listaDeEquipos.append(team)

####################################################################################################################################################################
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

        teamObject = getEquipo(equipo, listaDeEquipos)
        newEnemyName = equipoContrario[0]
        newEnemyObject = getEquipo(newEnemyName, listaDeEquipos)
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
                         maximosGolesEnContra, minimosGolesEnContra, mediaGolPorPartidoMarcados,
                         mediaGolPorPartidoEnContra)
    # teamObject.calculateData()
    # print(teamObject.puntosDeFuerza)

####################################################################################################################################################################
# Get points of Streght and Weakness
for team in listaDeEquipos:
    iter = 200
    metodoFuerza(iter, team, team, [])
    metodoDebilidad(iter, team, team, [])

####################################################################################################################################################################


####################################################################################################################################################################
# Get Dataframe
dataframetotal = pd.DataFrame()
dataframeDatosImportantes = pd.DataFrame()
for teamObject in listaDeEquipos:
    # UnoDataframes
    [recopilacionDeDatos, recopilacionDatosImportantes] = teamObject.getDataframe()
    dataframetotal = pd.concat([dataframetotal, recopilacionDeDatos])
    dataframeDatosImportantes = pd.concat([dataframeDatosImportantes, recopilacionDatosImportantes])

time.sleep(1)

####################################################################################################################################################################
variable = dataframeDatosImportantes.columns[0]
plt.xticks(x=variable)
ay = np.arange(-2, 100, 1)
for name in dataframeDatosImportantes.columns:
    if name == variable:
        continue
    rand_color = (randrange(255), randrange(255), randrange(255))  # crea colores rgb aleatorios
    # gca stands for 'get current axis'
    # ax = plt.gca()
    fig, ax = plt.subplots()
    ax.step(x=dataframeDatosImportantes[variable], y=dataframeDatosImportantes[name], linewidth=2)
    maxValue = dataframeDatosImportantes[name].max()
    ax.set(ylim=(-2, maxValue), yticks=np.arange(-2, maxValue, 1))
    # dataframeDatosImportantes.plot(kind='step', x=variable, y=name, ax=ax)
# plt.show()

####################################################################################################################################################################
# Next match take from soup
routeNextMatch = soup.find('table', {'id': 'tabla1'})
routeNextMatch = routeNextMatch.find_all('tr', {'class': ['vevent', 'vevent impar']})
for j, nextMatch in enumerate(routeNextMatch):
    teamOne = nextMatch.find('td', {'class': 'equipo1'}).find('a', href=True).find('img', alt=True).get('alt')
    teamTwo = nextMatch.find('td', {'class': 'equipo2'}).find('a', href=True).find('img', alt=True).get('alt')
    [teamDataOne, teamDataOneImportant] = getEquipo(teamOne, listaDeEquipos).getDataframe()
    [teamDataTwo, teamDataTwoImportant] = getEquipo(teamTwo, listaDeEquipos).getDataframe()
    matchs = pd.concat([teamDataOneImportant, teamDataTwoImportant])
    # Ploteo
    var = matchs.columns[0]
    plt.xticks(x=var)
    for i in matchs.columns:
        if i == var:
            continue
        ax = plt.gca()
        matchs.plot(kind='line', x=var, y=i, ax=ax)
    # plt.show()
    excelGlobal.excelWriterFunction(matchs, teamOne + ' vs ' + teamTwo)

# Obtener excel final
excelGlobal.excelWriterFunction(dataframetotal, "Datos en bruto")
# print(dataframetotal.to_string())
atexit.register(excelGlobal.closingProgram())
# exit(excelGlobal.closingProgram())º