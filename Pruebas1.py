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
    equiposQueHaGanado = []
    equiposQueHaPerdido = []
    equiposQueHaEmpatado = []
    golesEncontraUltimasJornadas = 0
    golesAfavorUltimasJornadas = 0
    maximosGoles = 0
    minimosGoles = 0
    maximosGolesEnContra = 0
    minimosGolesEnContra = 0
    mediaGolPorPartidoMarcados = 0
    mediaGolPorPartidoEnContra = 0
    puntosDeDebilidad = 0
    puntosDeFuerza = 0
    equiposQueHaEmpatadoNombre = []
    equiposQueHaGanadoNombre = []
    equiposQueHaPerdidoNombre = []

    def __init__(self, name, ganados=None, perdidos=None, empatados=None,
                 golesAfavorUltimasJornadas=0, golesEncontraUltimasJornadas=0, maximosGoles=0, minimosGoles=0,
                 maximosGolesEnContra=0, minimosGolesEnContra=0, mediaGolPorPartidoMarcados=0,
                 mediaGolPorPartidoEnContra=0):  # Llamo a los datos que me interan ya inicializados y les añado el valor que he dado en la entrada de la clase
        self.name = name
        if ganados == None:
            ganados = []
        if perdidos == None:
            perdidos = []
        if empatados == None:
            empatados = []
        self.setvalues(ganados, perdidos, empatados,
                       golesAfavorUltimasJornadas, golesEncontraUltimasJornadas, maximosGoles, minimosGoles,
                       maximosGolesEnContra, minimosGolesEnContra, mediaGolPorPartidoMarcados,
                       mediaGolPorPartidoEnContra)
    def setvalues(self,ganados= None, perdidos=None, empatados=None,
                  golesAfavorUltimasJornadas=0, golesEncontraUltimasJornadas=0, maximosGoles=0, minimosGoles=0,
                  maximosGolesEnContra=0, minimosGolesEnContra=0, mediaGolPorPartidoMarcados=0,
                  mediaGolPorPartidoEnContra=0):  # Llamo a los datos que me interan ya inicializados y les añado el valor que he dado en la entrada de la clase
        if ganados == None:
            ganados = []
        if perdidos == None:
            perdidos = []
        if empatados == None:
            empatados = []
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
            self.name,
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
            "Team",
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

###################################################################################################################################################################

def getEquipo(teamName, listaDeEquipos):
    for b in listaDeEquipos:
        if b.name == teamName:
            return b
###################################################################################################################################################################

def getTeamsObjects(route):
    listOfTeams = []
    tableData = route.find('table', {'class': "styled__TableStyled-sc-43wy8s-1 iOBNZZ"})
    eachRowMatch = tableData.find_all('div', {'class': 'styled__MatchStyled-sc-2hkd8m-1 jVNhaC'})
    for row in eachRowMatch:
        teams = row.find_all('p', {'class': 'styled__TextRegularStyled-sc-1raci4c-0 hvREvZ'})
        lenOfTeams = len(teams)
        for i in range(lenOfTeams):
            teamClass = Equipo(teams[i].contents[0])
            listOfTeams.append(teamClass)
    return listOfTeams

###################################################################################################################################################################

def getResults(route, listOfTeams):
    tableData = route.find('table', {'class': "styled__TableStyled-sc-43wy8s-1 iOBNZZ"})
    eachRowMatch = tableData.find_all('div', {'class': 'styled__MatchStyled-sc-2hkd8m-1 jVNhaC'})
    resultadosPartidos = []
    for row in eachRowMatch:
        match = {}
        results = row.find_all('p', {'class': 'styled__TextRegularStyled-sc-1raci4c-0 fYuQIM'})
        teams = row.find_all('p', {'class': 'styled__TextRegularStyled-sc-1raci4c-0 hvREvZ'})
        lenOfTeams = len(teams)
        for i in range(lenOfTeams):
            match[teams[i].contents[0]] = results[i].contents[0]
        resultadosPartidos.append(match)
    return resultadosPartidos
###################################################################################################################################################################

def lecturaDeJornada(resultadosEstaJornada, listOfTeams):
    for match in resultadosEstaJornada:
        teams = list(match.keys())
        team_1 = getEquipo(teams[0], listOfTeams)
        team_2 = getEquipo(teams[1], listOfTeams)
        if match[teams[0]] > match[teams[1]]:
            team_1.equiposQueHaGanado.append(team_2)
            team_2.equiposQueHaPerdido.append(team_1)
            match['Resultado'] = 1
        if match[teams[0]] < match[teams[1]]:
            match['Resultado'] = 2
            team_2.equiposQueHaGanado.append(team_1)
            team_1.equiposQueHaPerdido.append(team_2)
        if match[teams[0]] == match[teams[1]]:
            match['Resultado'] = 'x'
            team_1.equiposQueHaEmpatado.append(team_2)
            team_2.equiposQueHaEmpatado.append(team_1)
    return resultadosEstaJornada

###################################################################################################################################################################

def getPreviousJourneys(routeRef, itermax):       # INWORK
    #busco la jornada actual
    journeys = routeRef.find('div', {'class': 'styled__SubHeaderCalendarGrid-sc-1engvts-8 iYpljZ'}).find('div', {'class': 'styled__DropdownContainer-d9k1bl-0 kmhQzc'})
    currentJourney = journeys.find('span').contents[0]
    #busco las jornadas
    eachjourney = journeys.find('ul', {'class': 'styled__ItemsList-d9k1bl-2 hkGQnA'}).find_all('a')
    lenJourneys = len(eachjourney)
    previousJourneys = []
    linkPreviousJourneys = []   #uso esto para buscar cada jornada
    for numday, day in enumerate(eachjourney):
        linkPreviousJourneys.append('https://www.laliga.com/' + day['href'])
        previousJourneys.append(day)
        if day.contents[0] == currentJourney:
            del previousJourneys[:numday-itermax]
            del linkPreviousJourneys[:numday - itermax]
            break
    previousJourneys.reverse()
    linkPreviousJourneys.reverse()
    # enterPage = requests.get('https://www.laliga.com/' + linkPreviousJourneys[0])  # Get URL
    return previousJourneys, linkPreviousJourneys

###################################################################################################################################################################

def getLinkHtml(route):
    link = requests.get(route)
    soupOfLink = BeautifulSoup(link.text, 'html.parser')
    return soupOfLink
###################################################################################################################################################################

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

###################################################################################################################################################################

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

###################################################################################################################################################################

def addPointsStrengthWeakness(listOfTeams):
    for team in listOfTeams:
        iter = 200
        metodoFuerza(iter, team, team, [])
        metodoDebilidad(iter, team, team, [])

###################################################################################################################################################################





###################################################################################################################################################################
soupOfTeams = getLinkHtml('https://www.laliga.com/laliga-santander/resultados')

###################################################################################################################################################################

#For day BASE (obtener), -i to iter (4,5,6,7...) result efficiency
# Set inicial
listOfPrimera= getTeamsObjects(soupOfTeams)
resultadosJornadaDeReferencia = getResults(soupOfTeams, listOfPrimera)





###################################################################################################################################################################


def maxProbability(soupOfTeams, itermax, journeyRefResults, listOfTeams):

    jornadasprevias, linkJP = getPreviousJourneys(soupOfTeams, itermax)
    for link in linkJP:
        ruta = getLinkHtml(link)
        resultados = getResults(ruta, listOfPrimera)
        resultadosR = lecturaDeJornada(resultados, listOfPrimera)

    # llamo al metodo puntos Fuerza y debilidad
    addPointsStrengthWeakness(listOfPrimera)

    resultadosTotal = lecturaDeJornada(journeyRefResults, listOfTeams)
    numHits = 0
    for partido in resultadosTotal:
        llaves = list(partido.keys())
        team_1 = getEquipo(llaves[0], listOfTeams)
        team_2 = getEquipo(llaves[1], listOfTeams)
        pointsTeam_1 = team_1.puntosDeFuerza + team_2.puntosDeDebilidad
        pointsTeam_2 = team_2.puntosDeFuerza + team_1.puntosDeDebilidad
        minimumP = min([pointsTeam_1, pointsTeam_2])
        if minimumP == 0:
            minimumP = 0.00000001
        pointsTeam_1_Normalized = round(pointsTeam_1/minimumP, 2)
        pointsTeam_2_Normalized = round(pointsTeam_2/minimumP, 2)
        margenError = 0.05      #variar Dinamicamente
        if abs(pointsTeam_1_Normalized - pointsTeam_2_Normalized) > margenError and pointsTeam_1_Normalized > pointsTeam_2_Normalized and partido[llaves[2]] == 1:
            numHits += 1
        if abs(pointsTeam_1_Normalized - pointsTeam_2_Normalized) > margenError and pointsTeam_1_Normalized < pointsTeam_2_Normalized and partido[llaves[2]] == 2:
            numHits += 1
        if abs(pointsTeam_1_Normalized - pointsTeam_2_Normalized) < margenError and partido[llaves[2]] == 'x':
            numHits += 1
    porcentajeAcierto = 100*numHits/len(resultadosTotal)
    return porcentajeAcierto

itermax = 10
valorInicialAcierto = 0
for numIter in range(itermax):
    if numIter == 0:
        continue
    porcentajeAcierto = maxProbability(soupOfTeams, numIter, resultadosJornadaDeReferencia, listOfPrimera)
    print(porcentajeAcierto)
    if porcentajeAcierto > valorInicialAcierto:
        valorInicialAcierto = porcentajeAcierto
        valorIterMaxAcierto = numIter
        print(valorInicialAcierto, valorIterMaxAcierto)

print(valorInicialAcierto, valorIterMaxAcierto)

#obtener modulo de partidos de X jornada:
p = 0
w=0
for i in listOfPrimera:
    i.transformData()
    w = w + len(i.equiposQueHaGanado)
    p = p + len(i.equiposQueHaPerdidoNombre)
    # print(i.name, i.equiposQueHaPerdidoNombre)
    # print(i.name, i.puntosDeFuerza, i.puntosDeDebilidad)
# print(w,p)
