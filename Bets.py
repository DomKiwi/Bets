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
import xlsxwriter
from vincent.colors import brews


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
            "Position",
            "Team",
            "Points",
            "Matches",
            "Wins",
            "Draws",
            "Loses",
            "G_Scored",
            "G_Against",
            "Won vs",
            "Lost vs",
            "Draw vs",
            "G_Scored last_4",
            "G_Against last_4",
            "Max G_Scored last_4",
            "Min G_Scored last_4",
            "Max G_Against last_4",
            "Min G_Against last_4",
            "Averg G_Scored last_4",
            "Averg G_Against last_4",
            "Strength Points",
            "Weakness Points"
        ]
        recopilacionImportanteEquipo.columns = [
            "Team",
            "G_Scored last_4",
            "G_Against last_4",
            "Max G_Scored last_4",
            "Min G_Scored last_4",
            "Max G_Against last_4",
            "Min G_Against last_4",
            "Averg G_Scored last_4",
            "Averg G_Against last_4",
            "Strength Points",
            "Weakness Points"
        ]
        return recopilacionequipo, recopilacionImportanteEquipo

###########################################################     EXCEL CLASS     ###############################################################################
# Create excel to write data call it more times if I want
class excelWriter:
    writerName = ''
    def __init__(self,writerName, data = pd.DataFrame(),nameSheet = ''):
        self.writerName = writerName
        self.writer = pd.ExcelWriter(writerName, engine='xlsxwriter')
    def excelWriterFunction(self, data, nameSheet):
        nameSheet = nameSheet[0:30]
        data.to_excel(self.writer, sheet_name=nameSheet, index=0)
        wb = self.writer.book
        ws = self.writer.sheets[nameSheet]
        chart = wb.add_chart({'type': 'column'})
        col_1 = data[data.columns[0]]
        for col_num in range(1, len(col_1) + 1):
            chart.add_series({
                'name': [nameSheet, col_num, 0],
                'categories': [nameSheet, 0, 1, 0, len(data.columns)-1],
                'values': [nameSheet, col_num, 1, col_num, len(data.columns)-1],
                'gap': 300,
            })
        ws.set_column(0, len(data.columns), 20)
        chart.set_x_axis({'name': 'Teams'})
        chart.set_y_axis({'name': 'Points', 'major_gridlines': {'visible': False}})
        ws.insert_chart('A7', chart)
    def closingProgram(self):
        self.writer.close()
        print('Guardando el excel de datos pedidos')



#################################################   FUNCTIONS   ##################################################################################################
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

def addPointsStrengthWeakness(listOfTeams):
    for team in listOfTeams:
        iter = 200
        metodoFuerza(iter, team, team, [])
        metodoDebilidad(iter, team, team, [])

def searchForEachTeam(route):
    listOfTeams = []

    # Lets start the program searching for Data in website
    soupOfLeague = BeautifulSoup(route.text, 'html.parser')  # Use this format to read it

    blockquote_items = soupOfLeague.find('table', {'id': 'tabla2'})  # Use Bs4 to find specific data
    blockquote_items = blockquote_items.find('tbody')
    blockquote_items = blockquote_items.find_all('tr')

    # Get name of teams and create a class for each one
    for num, blockquote in enumerate(blockquote_items):
        equipo = blockquote.find("td", {"class": ["equipo", "equipo sube", "equipo baja"]}).find('a').contents[0]
        team = Equipo(equipo)
        listOfTeams.append(team)
    return listOfTeams

def MatchesDay(route, listOfTeams, excel):
    currentDay = route.find('div',{'class': 'j_cur'}).get('a')
    routeNextMatch = route.find('table', {'id': 'tabla1'})
    routeNextMatch = routeNextMatch.find_all('tr', {'class': ['vevent', 'vevent impar']})
    for j, nextMatch in enumerate(routeNextMatch):
        teamOne = nextMatch.find('td', {'class': 'equipo1'}).find('a', href=True).find('img', alt=True).get('alt')
        teamOneGoals = nextMatch.find('td', {'class': 'equipo1'}).find('a', href=True).find('img', alt=True).get('alt')
        teamTwo = nextMatch.find('td', {'class': 'equipo2'}).find('a', href=True).find('img', alt=True).get('alt')
        # Excepcion
        for num_2, a in enumerate(listOfTeams):     #Excepciones por toda la cara de la pagina web
            if a.name in teamOne:
                teamOne = a.name
            if a.name in teamTwo:
                teamTwo = a.name
        if 'Levante' in teamOne and 'Planas' in teamOne:
            teamOne = 'Levante Planas'
        if 'Levante' in teamTwo and 'Planas' in teamTwo:
            teamTwo = 'Levante Planas'
        # Fin de Excepcion
        [teamDataOne, teamDataOneImportant] = getEquipo(teamOne, listOfTeams).getDataframe()
        [teamDataTwo, teamDataTwoImportant] = getEquipo(teamTwo, listOfTeams).getDataframe()
        matchs = pd.concat([teamDataOneImportant, teamDataTwoImportant])
        excel.excelWriterFunction(matchs, teamOne + ' vs ' + teamTwo)

pagePrimeraDivision = requests.get('https://www.resultados-futbol.com/primera')  # Get URL
listaDeEquiposDePrimera, soupPrimeraDivision = searchForEachTeam(pagePrimeraDivision)
#For day BASE (obtener), -i to iter (4,5,6,7...) result efficiency