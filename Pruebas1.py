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

def getResults(route, listOfTeams,resultsEmpty):
    tableData = route.find('table', {'class': "styled__TableStyled-sc-43wy8s-1 iOBNZZ"})
    eachRowMatch = tableData.find_all('div', {'class': 'styled__MatchStyled-sc-2hkd8m-1 jVNhaC'})
    resultadosPartidos = []
    for row in eachRowMatch:
        match = {}
        results = row.find_all('p', {'class': 'styled__TextRegularStyled-sc-1raci4c-0 fYuQIM'})
        teams = row.find_all('p', {'class': 'styled__TextRegularStyled-sc-1raci4c-0 hvREvZ'})
        lenOfTeams = len(teams)
        if resultsEmpty is True:
            for i in range(lenOfTeams):
                match[teams[i].contents[0]] = 'No Data'
        else:
            for i in range(lenOfTeams):
                match[teams[i].contents[0]] = results[i].contents[0]
        resultadosPartidos.append(match)
    return resultadosPartidos
###################################################################################################################################################################
# def lecturaDeJornadaInicial(resultadosEstaJornadaInicial, listOfTeams, there_is_data):
#     for match in resultadosEstaJornadaInicial:
#         teams = list(match.keys())
#         team_1 = getEquipo(teams[0], listOfTeams)
#         team_2 = getEquipo(teams[1], listOfTeams)
#         team_1.equiposQueHaGanado = []
#         team_1.equiposQueHaPerdido = []
#         team_2.equiposQueHaPerdido = []
#         team_2.equiposQueHaGanado = []
#         team_1.equiposQueHaEmpatado = []
#         team_2.equiposQueHaEmpatado = []
#         if there_is_data is True:
#             if match[teams[0]] > match[teams[1]]:
#                 match['Resultado'] = 1
#             if match[teams[0]] < match[teams[1]]:
#                 match['Resultado'] = 2
#             if match[teams[0]] == match[teams[1]]:
#                 match['Resultado'] = 'x'
#     return resultadosEstaJornadaInicial


def lecturaDeJornada(resultadosEstaJornada, listOfTeams, there_is_data, it_is_Reference):
    for match in resultadosEstaJornada:
        teams = list(match.keys())
        team_1 = getEquipo(teams[0], listOfTeams)
        team_2 = getEquipo(teams[1], listOfTeams)
        if there_is_data is True and it_is_Reference is True:
            team_1.equiposQueHaGanado = []
            team_1.equiposQueHaPerdido = []
            team_2.equiposQueHaPerdido = []
            team_2.equiposQueHaGanado = []
            team_1.equiposQueHaEmpatado = []
            team_2.equiposQueHaEmpatado = []
            if match[teams[0]] > match[teams[1]]:
                match['Resultado'] = 1
            if match[teams[0]] < match[teams[1]]:
                match['Resultado'] = 2
            if match[teams[0]] == match[teams[1]]:
                match['Resultado'] = 'x'
        elif there_is_data is False and it_is_Reference is True:
            team_1.equiposQueHaGanado = []
            team_1.equiposQueHaPerdido = []
            team_2.equiposQueHaPerdido = []
            team_2.equiposQueHaGanado = []
            team_1.equiposQueHaEmpatado = []
            team_2.equiposQueHaEmpatado = []
        else:
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
        previousJourneys.append(day.contents[0])
        if day.contents[0] == currentJourney:
            del previousJourneys[:numday-itermax]
            previousJourneys = previousJourneys[:-1]
            del linkPreviousJourneys[:numday - itermax]
            linkPreviousJourneys = linkPreviousJourneys[:-1]
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

def metodoFuerza(iter, teamToCheck, teamToAddPoints, teamsCountedAlready, resetPoints):
    if resetPoints is True:
        teamToAddPoints.puntosDeDebilidad = 0
    if (iter <= 0): return
    # teamList = []
    for G in teamToCheck.equiposQueHaGanado:
        teamToAddPoints.puntosDeFuerza += 1
        if G in teamsCountedAlready:
            continue
        iter -= 1
        teamsCountedAlready.append(G)
        metodoFuerza(iter, G, teamToAddPoints, teamsCountedAlready, False)

###################################################################################################################################################################

def metodoDebilidad(iter, teamToCheck, teamToAddPoints, teamsCountedAlready, resetPoints):
    if resetPoints is True:
        teamToAddPoints.puntosDeDebilidad = 0
    if (iter <= 0): return
    # teamList = []
    for L in teamToCheck.equiposQueHaPerdido:
        teamToAddPoints.puntosDeDebilidad += 1
        if L in teamsCountedAlready:
            continue
        iter -= 1
        teamsCountedAlready.append(L)
        metodoDebilidad(iter, L, teamToAddPoints, teamsCountedAlready, False)

###################################################################################################################################################################

def addPointsStrengthWeakness(listOfTeams, resetPoints):
    for team in listOfTeams:
        iter = 200
        metodoFuerza(iter, team, team, [], resetPoints)
        metodoDebilidad(iter, team, team, [], resetPoints)

###################################################################################################################################################################

def maxProbability(soupOfTeams, itermax, listOfTeams, journeyRefResults, there_is_data):
    if there_is_data is True:
        # resultados de la jornada de referencia
        resultadosTotal = lecturaDeJornada(journeyRefResults, listOfTeams, True, True)
        # resultados de las anteriores jornadas actualizandolo cada iteracion
        jornadasprevias, linkJP = getPreviousJourneys(soupOfTeams, itermax)
        for numLink, link in enumerate(linkJP):
            ruta = getLinkHtml(link)
            resultados = getResults(ruta, listOfTeams, False)
            resultadosR = lecturaDeJornada(resultados, listOfTeams, True, False)

        # llamo al metodo puntos Fuerza y debilidad con los partidos ganados y perdidos actualizados
        addPointsStrengthWeakness(listOfTeams, True)
        # empiezo la iteracion en la jornada de referencia para comparar los resultados con los datos que tengo yo segun las iteraciones que he hecho en cada caso
        numHits = 0
        for partido in resultadosTotal:
            llaves = list(partido.keys())
            team_1 = getEquipo(llaves[0], listOfTeams)
            team_2 = getEquipo(llaves[1], listOfTeams)
            pointsTeam_1 = team_1.puntosDeFuerza + team_2.puntosDeDebilidad
            pointsTeam_2 = team_2.puntosDeFuerza + team_1.puntosDeDebilidad
            minimumP = min([pointsTeam_1, pointsTeam_2])
            if minimumP == 0:
                minimumP = 1
            pointsTeam_1_Normalized = round(pointsTeam_1 / minimumP, 2)
            pointsTeam_2_Normalized = round(pointsTeam_2 / minimumP, 2)
            margenError = 0.05  # variar Dinamicamente
            print(team_1.name, pointsTeam_1_Normalized, pointsTeam_2_Normalized, team_2.name)
            if abs(pointsTeam_1_Normalized - pointsTeam_2_Normalized) > margenError and pointsTeam_1_Normalized > pointsTeam_2_Normalized and \
                    partido[llaves[2]] == 1:
                numHits += 1
            if abs(pointsTeam_1_Normalized - pointsTeam_2_Normalized) > margenError and pointsTeam_1_Normalized < pointsTeam_2_Normalized and \
                    partido[llaves[2]] == 2:
                numHits += 1
            if abs(pointsTeam_1_Normalized - pointsTeam_2_Normalized) < margenError and partido[llaves[2]] == 'x':
                numHits += 1
        print(numHits)
        porcentajeAcierto = 100 * numHits / len(resultadosTotal)
        return porcentajeAcierto
    else:
        #resultados de la jornada de referencia
        resultadosTotal = lecturaDeJornada(journeyRefResults, listOfTeams, False, True)
        # resultados de las anteriores jornadas actualizandolo cada iteracion
        jornadasprevias, linkJP = getPreviousJourneys(soupOfTeams, itermax)
        for numLink, link in enumerate(linkJP):
            ruta = getLinkHtml(link)
            resultados = getResults(ruta, listOfTeams, False)
            resultadosR = lecturaDeJornada(resultados, listOfTeams, True, False)

        # llamo al metodo puntos Fuerza y debilidad con los partidos ganados y perdidos actualizados
        addPointsStrengthWeakness(listOfTeams, True)
        #empiezo la iteracion en la jornada de referencia para comparar los resultados con los datos que tengo yo segun las iteraciones que he hecho en cada caso
        numHits = 0
        for partido in resultadosTotal:
            llaves = list(partido.keys())
            team_1 = getEquipo(llaves[0], listOfTeams)
            team_2 = getEquipo(llaves[1], listOfTeams)
            pointsTeam_1 = team_1.puntosDeFuerza + team_2.puntosDeDebilidad
            pointsTeam_2 = team_2.puntosDeFuerza + team_1.puntosDeDebilidad
            minimumP = min([pointsTeam_1, pointsTeam_2])
            if minimumP == 0:
                minimumP = 1
            pointsTeam_1_Normalized = round(pointsTeam_1/minimumP, 2)
            pointsTeam_2_Normalized = round(pointsTeam_2/minimumP, 2)
            print(team_1.name, pointsTeam_1_Normalized, pointsTeam_2_Normalized,team_2.name)

###################################################################################################################################################################

def getDataOfMaxEfficiency(URL, in_this_link_there_are_results, maxValueOfMatchsCalculated):
    maxValueOfMatchsCalculated = maxValueOfMatchsCalculated + 1
    soupOfPage = getLinkHtml(URL)
    listOfTeams = getTeamsObjects(soupOfPage)
    resultadosJornadaDeReferencia = getResults(soupOfPage, listOfTeams, in_this_link_there_are_results)
    getPorcentaje(soupOfPage,maxValueOfMatchsCalculated, listOfTeams, resultadosJornadaDeReferencia, in_this_link_there_are_results)
    return listOfTeams

def getPorcentaje(soupOfPage, itermax, listOfTeams, resultsRef,there_is_data):
    if there_is_data is True:
        valorInicialAcierto = 0  # % Porcentaje
        for numIter in range(1, itermax, 1):
            porcentajeAcierto = maxProbability(soupOfPage, numIter, listOfTeams, resultsRef, there_is_data)
            print(porcentajeAcierto, numIter)
            if porcentajeAcierto > valorInicialAcierto:
                valorInicialAcierto = porcentajeAcierto
                valorIterMaxAcierto = numIter
    else:
        valorInicialAcierto = 0  # % Porcentaje
        for numIter in range(1, itermax, 1):
            porcentajeAcierto = maxProbability(soupOfPage, numIter, listOfTeams, resultsRef, there_is_data)



###################################################################################################################################################################
    # INPUT DATA #
URL_Ref = 'https://www.laliga.com/laliga-santander/resultados/2022-23/jornada-22'
in_this_link_there_are_results_Ref = True
maxValueOfMatchsCalculated_Ref = 5

###################################################################################################################################################################
# in_this_link_there_are_results = True
listOfPrimera = getDataOfMaxEfficiency(URL_Ref, in_this_link_there_are_results_Ref, maxValueOfMatchsCalculated_Ref)
#For day BASE (obtener), -i to iter (4,5,6,7...) result efficiency
# # Set inicial
# listOfPrimera= getTeamsObjects(soupOfTeams)
# resultadosJornadaDeReferencia = getResults(soupOfTeams, listOfPrimera, False)
# resultadosJornadaDeReferencia = getResults(soupOfTeams, listOfPrimera, False) #CUANDO QUIERA COMPROBAR EL METODO

###################################################################################################################################################################
# Obtengo probabilidad de cada caso que yo busque
# itermax = 10
# valorInicialAcierto = 0     # % Porcentaje
# for numIter in range(1, itermax, 1):
#     porcentajeAcierto = maxProbability(soupOfTeams, numIter, resultadosJornadaDeReferencia, listOfPrimera)
#     print(porcentajeAcierto,numIter)
#     if porcentajeAcierto > valorInicialAcierto:
#         valorInicialAcierto = porcentajeAcierto
#         valorIterMaxAcierto = numIter
# print(valorInicialAcierto, valorIterMaxAcierto)

#obtener modulo de partidos de X jornada:
p = 0
w=0
for i in listOfPrimera:
    i.transformData()
    w = w + len(i.equiposQueHaGanado)
    p = p + len(i.equiposQueHaPerdidoNombre)
    # print(i.name, i.equiposQueHaGanadoNombre)
    # print(i.name, i.puntosDeFuerza, i.puntosDeDebilidad)
# print(w,p)
