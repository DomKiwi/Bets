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
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import lxml
from selenium.webdriver.common.by import By





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
            self.ganados = []
        if perdidos == None:
            perdidos = []
        if empatados == None:
            empatados = []
        self.setvalues(ganados, perdidos, empatados,
                       golesAfavorUltimasJornadas, golesEncontraUltimasJornadas, maximosGoles, minimosGoles,
                       maximosGolesEnContra, minimosGolesEnContra, mediaGolPorPartidoMarcados,
                       mediaGolPorPartidoEnContra)

    def setvalues(self, ganados=None, perdidos=None, empatados=None,
                  golesAfavorUltimasJornadas=0, golesEncontraUltimasJornadas=0, maximosGoles=0, minimosGoles=0,
                  maximosGolesEnContra=0, minimosGolesEnContra=0, mediaGolPorPartidoMarcados=0,
                  mediaGolPorPartidoEnContra=0):  # Llamo a los datos que me interan ya inicializados y les añado el valor que he dado en la entrada de la clase
        if ganados is None:
            ganados = []
        if perdidos is None:
            perdidos = []
        if empatados is None:
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

def getLinkHtml(route):
    link = requests.get(route)
    soupOfLink = BeautifulSoup(link.text, 'html.parser')
    return soupOfLink

def getLinkHtml_Pirate(route):

    driver = webdriver.Chrome()
    driver.get(route)
    driver.find_element(By.XPATH, '//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]').click()
    driver.find_element(By.XPATH, '/html/body/div[5]/div[5]/div/ul/li[2]/a').click()
    time.sleep(3)
    soupOfLink = BeautifulSoup(driver.page_source, 'lxml')
    driver.quit()
    return soupOfLink


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

def metodoFuerza(iter, teamToCheck, teamToAddPoints, teamsCountedAlready, resetPoints, valorDePuntos, factorDegenerativo):
    if resetPoints:
        teamToAddPoints.puntosDeFuerza = 0
    if iter <= 0:
        return
    for G in teamToCheck.equiposQueHaGanado:
        teamToAddPoints.puntosDeFuerza += 1*valorDePuntos
        if G in teamsCountedAlready:
            continue
        iter -= 1
        teamsCountedAlready.append(G)
        valorDePuntosNuevo = valorDePuntos*factorDegenerativo
        metodoFuerza(iter, G, teamToAddPoints, teamsCountedAlready, False, valorDePuntosNuevo,factorDegenerativo)


###################################################################################################################################################################

def metodoDebilidad(iter, teamToCheck, teamToAddPoints, teamsCountedAlready, resetPoints, valorDePuntos, factorDegenerativo):
    if resetPoints:
        teamToAddPoints.puntosDeDebilidad = 0
    if (iter <= 0): return
    for L in teamToCheck.equiposQueHaPerdido:
        teamToAddPoints.puntosDeDebilidad += 1*valorDePuntos
        if L in teamsCountedAlready:
            continue
        iter -= 1
        teamsCountedAlready.append(L)
        # valorDePuntosNuevo = round(max(valorDePuntos - 0.1, 0), 2)
        valorDePuntosNuevo = factorDegenerativo * valorDePuntos
        metodoDebilidad(iter, L, teamToAddPoints, teamsCountedAlready, False, valorDePuntosNuevo, factorDegenerativo)

###################################################################################################################################################################

def addPointsStrengthWeakness(listOfTeams, resetPoints, valorDePuntos, factorDegenerativo):
    for team in listOfTeams:
        iter = 200
        metodoFuerza(iter, team, team, [], resetPoints, valorDePuntos, factorDegenerativo)
        metodoDebilidad(iter, team, team, [], resetPoints, valorDePuntos, factorDegenerativo)


###################################################################################################################################################################
###################################################################################################################################################################

def getDataOfMaxEfficiency(URL, in_this_link_there_are_results, maxValueOfMatchsCalculated):
    maxValueOfMatchsCalculated = maxValueOfMatchsCalculated + 1
    soupOfPage = getLinkHtml(URL)
    listOfTeams = getTeamsObjects(soupOfPage)
    #Loop last matches compare method
    previousJourneys_Repeticiones, linkPreviousJourneysRepeticiones = getPreviousJourneys(soupOfPage, maxValueOfMatchsCalculated)

    # # # for numLink, linkRep in enumerate(linkPreviousJourneysRepeticiones):
    # # #     print('#####################################################################################################################################################################')
    # # #     print('Entramos en la jornada: ' + str(previousJourneys_Repeticiones[numLink]))
    # # #     soup_rep = getLinkHtml(linkRep)
    # # #     results_rep = getResults(soup_rep, True)
    # # #     getPorcentaje(soup_rep, maxValueOfMatchsCalculated, listOfTeams, results_rep, True)
    # # #     print('/////////////////////////////////////////////////////////////////////////////////////////////////')
    # # #     print('CAMBIO DE JORNADA QUE COMPROBAR')

    #OFICIAL
    print('REALIZAMOS LA ULTIMA JORNADA')
    resultadosJornadaDeReferencia = getResults(soupOfPage, in_this_link_there_are_results)
    getPorcentaje(soupOfPage, maxValueOfMatchsCalculated, listOfTeams, resultadosJornadaDeReferencia,
                  in_this_link_there_are_results)
    return listOfTeams


###################################################################################################################################################################

def getResults(route, there_is_data):
    tableData = route.find('table', {'class': "styled__TableStyled-sc-43wy8s-1 iOBNZZ"})
    eachRowMatch = tableData.find_all('tr', {'class': ['styled__TableRow-sc-43wy8s-4 lkicZz', 'styled__TableRow-sc-43wy8s-4 WrPER', 'styled__TableRow-sc-43wy8s-4 kSOWNM', 'styled__TableRow-sc-43wy8s-4 czleHG']})
    resultadosPartidos = []
    for numruow, row in enumerate(eachRowMatch):
        rowMatch = row.find('div', {'class': 'styled__MatchStyled-sc-2hkd8m-1 jVNhaC'})
        match = {}
        results = rowMatch.find_all('p', {'class': 'styled__TextRegularStyled-sc-1raci4c-0 fYuQIM'})
        teams = rowMatch.find_all('p', {'class': 'styled__TextRegularStyled-sc-1raci4c-0 hvREvZ'})
        arbitro = row.find('p', {'class': 'styled__TextRegularStyled-sc-1raci4c-0 jbKUta'})
        lenOfTeams = len(teams)
        if there_is_data is True:
            for i in range(lenOfTeams):
                match[teams[i].contents[0]] = results[i].contents[0]
        else:
            for i in range(lenOfTeams):
                match[teams[i].contents[0]] = 'No Data'
        match['Arbitro'] = arbitro.contents[0]
        resultadosPartidos.append(match)
    return resultadosPartidos


###################################################################################################################################################################

def getPorcentaje(soupOfPage, itermax, listOfTeams, resultsRef, there_is_data):
    if there_is_data:
        valorInicialAcierto = 0  # % Porcentaje
        for numIter in range(1, itermax, 1):
            print('/////////////////////////////////////////////////////////////')
            porcentajeAcierto = maxProbability(soupOfPage, numIter, listOfTeams, resultsRef, there_is_data)
            print('El numero de partidos previos escogidos en esta iteracion es: ' + str(numIter))
            if porcentajeAcierto > valorInicialAcierto:
                valorInicialAcierto = porcentajeAcierto
                valorIterMaxAcierto = numIter
    else:
        for numIter in range(1, itermax, 1):
            print('/////////////////////////////////////////////////////////////')
            porcentajeAcierto = maxProbability(soupOfPage, numIter, listOfTeams, resultsRef, there_is_data)
            print('El numero de partidos previos escogidos en esta iteracion es: ' + str(numIter))
    print('/////////////////////////////////////////////////////////////')

###################################################################################################################################################################

def maxProbability(soupOfTeams, itermax, listOfTeams, journeyRefResults, there_is_data):
    if there_is_data:
        # resultados de la jornada de referencia
        resultadosTotal = lecturaDeJornada(soupOfTeams, journeyRefResults, listOfTeams, True, True, True)
    else:
        # resultados de la jornada de referencia
        resultadosTotal = lecturaDeJornada(soupOfTeams, journeyRefResults, listOfTeams, False, True, False)

    # resultados de las anteriores jornadas actualizandolo cada iteracion
    jornadasprevias, linkJP = getPreviousJourneys(soupOfTeams, itermax)
    print('/////////////////////////////////////////////////////////////')
    print('Resultados buscados en esta iteración: ' + str(linkJP))
    for numLink, link in enumerate(linkJP):
        ruta = getLinkHtml(link)
        resultados = getResults(ruta, True)
        resultadosR = lecturaDeJornada(soupOfTeams, resultados, listOfTeams, True, False, False)

    factoresDegenerativos = np.arange(0.1, 0.95, 0.05)
    factoresDegenerativosPosibles = {}
    valorDePuntos_Deg = 1
    for numDeg in factoresDegenerativos:
        addPointsStrengthWeakness(listOfTeams, True, valorDePuntos_Deg, numDeg)
        porcentajeAciertoFactorDeg = getProbabilityOfEachMatch(resultadosTotal, listOfTeams, there_is_data, False)
        factoresDegenerativosPosibles[numDeg] = porcentajeAciertoFactorDeg
    factorDegenerativosOptimo = max(factoresDegenerativosPosibles, key=factoresDegenerativosPosibles.get)
    print(factorDegenerativosOptimo)
    addPointsStrengthWeakness(listOfTeams, True, valorDePuntos_Deg, factorDegenerativosOptimo)
    porcentajeAcierto = getProbabilityOfEachMatch(resultadosTotal, listOfTeams, there_is_data, True)
    return porcentajeAcierto


###################################################################################################################################################################

def lecturaDeJornada(soupOfTeams, resultadosEstaJornada, listOfTeams, there_is_data, it_is_Reference, hayArbitro):
    for match in resultadosEstaJornada:
        arbitroSoup = soupOfTeams.find('p', {'class': 'styled__TextRegularStyled-sc-1raci4c-0 jbKUta'}).contents[0]
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

def getPreviousJourneys(routeRef, itermax):  # INWORK
    # busco la jornada actual
    journeys = routeRef.find('div', {'class': 'styled__SubHeaderCalendarGrid-sc-1engvts-8 iYpljZ'}).find('div', {
        'class': 'styled__DropdownContainer-d9k1bl-0 kmhQzc'})
    currentJourney = journeys.find('span').contents[0]
    # busco las jornadas
    eachjourney = journeys.find('ul', {'class': 'styled__ItemsList-d9k1bl-2 hkGQnA'}).find_all('a')
    lenJourneys = len(eachjourney)
    previousJourneys = []
    linkPreviousJourneys = []  # uso esto para buscar cada jornada
    for numday, day in enumerate(eachjourney):
        linkPreviousJourneys.append('https://www.laliga.com/' + day['href'])
        previousJourneys.append(day.contents[0])
        if day.contents[0] == currentJourney:
            del previousJourneys[:numday - itermax]
            previousJourneys = previousJourneys[:-1]
            del linkPreviousJourneys[:numday - itermax]
            linkPreviousJourneys = linkPreviousJourneys[:-1]
            break
    previousJourneys.reverse()
    linkPreviousJourneys.reverse()
    # enterPage = requests.get('https://www.laliga.com/' + linkPreviousJourneys[0])  # Get URL
    return previousJourneys, linkPreviousJourneys


###################################################################################################################################################################
def getProbabilityOfEachMatch(resultadosTotalDeReferencia, listOfTeams, there_is_data, printDataForMaxProb):
    # max_error_margen = 0.2  # variarlo si quiero
    max_error_margen = np.arange(0, 0.5, 0.01)
    porcentajeYMargenError = {}
    for iError in max_error_margen:
        porcentajeDeAcierto, margenDeError = calculatePointsAndPorcentaje(resultadosTotalDeReferencia, listOfTeams, there_is_data, iError, False, False)
        porcentajeYMargenError[margenDeError] = porcentajeDeAcierto
    maxValuePorcentajeYMargenError = max(porcentajeYMargenError, key=porcentajeYMargenError.get)
    porcentajeDeAciertoMaximo, margenDeErrorMaximo = calculatePointsAndPorcentaje(resultadosTotalDeReferencia, listOfTeams, there_is_data, maxValuePorcentajeYMargenError, True, printDataForMaxProb)
    if there_is_data and printDataForMaxProb:
        print('Para el numero de jornadas previas usadas obtengo un valor maximo de porcentaje de aciertos: ' + str(porcentajeDeAciertoMaximo) + ' con un margen de error para empates de: ' + str(margenDeErrorMaximo))
    return porcentajeDeAciertoMaximo


arbitroPage_Ref = getLinkHtml_Pirate('https://es.whoscored.com/Regions/206/Tournaments/4/Seasons/9149/Stages/21073/RefereeStatistics/Espa%C3%B1a-LaLiga-2022-2023')
def obtainArbitro(name):
    arbitroDict = {}
    listavacia_1 = []
    name_low = name.replace(' ', '-').lower()
    a = arbitroPage_Ref.find('div', {'id': 'referee-stats-alternate'}).find('tbody', {'id': 'referee-tournaments-table-body'}).find_all('tr')
    thisArbitro = 'Maimon'
    for ia in a:
        ib = ia.find_all('a', {'class': 'tournament-link'})
        for ic in ib:
            if name_low.lower() in ic['href'].lower():
                thisArbitro = ia
                break
    if thisArbitro == 'Maimon':
        for im in range(3):
            listavacia_1.append(33.3)
    else:
        for numff, ff in enumerate(thisArbitro.find_all('td')):
            if numff >1:
                listavacia_1.append(ff.contents[0])
    arbitroDict[name] = listavacia_1
    return arbitroDict


def calculatePointsAndPorcentaje(resultadosTotalDeReferencia, listOfTeams, there_is_data, margenDeError,printData, printDataForMaxProb):
    numHits = 0
    for partido in resultadosTotalDeReferencia:
        dataArbitros = obtainArbitro(partido['Arbitro'])
        llaves = list(partido.keys())
        team_1 = getEquipo(llaves[0], listOfTeams)
        team_2 = getEquipo(llaves[1], listOfTeams)
        pointsTeam_1 = (team_1.puntosDeFuerza + team_2.puntosDeDebilidad)*float(dataArbitros[partido['Arbitro']][0])/100
        pointsTeam_2 = (team_2.puntosDeFuerza + team_1.puntosDeDebilidad)*float(dataArbitros[partido['Arbitro']][1])/100
        minimumP = min([pointsTeam_1, pointsTeam_2])
        if minimumP == 0:
            minimumP = 1
        pointsTeam_1_Normalized = abs(round(pointsTeam_1 / minimumP, 5))
        pointsTeam_2_Normalized = abs(round(pointsTeam_2 / minimumP, 5))
        if there_is_data:
            if printData and printDataForMaxProb:
                print(team_1.name, round(pointsTeam_1_Normalized, 2), round(pointsTeam_2_Normalized, 2), team_2.name,
                  partido[llaves[2]])
            if abs(pointsTeam_1_Normalized - pointsTeam_2_Normalized) > margenDeError and pointsTeam_1_Normalized > pointsTeam_2_Normalized and \
                    partido[llaves[2]] == 1:
                numHits += 1
            if abs(pointsTeam_1_Normalized - pointsTeam_2_Normalized) > margenDeError and pointsTeam_1_Normalized < pointsTeam_2_Normalized and \
                    partido[llaves[2]] == 2:
                numHits += 1
            if abs(pointsTeam_1_Normalized - pointsTeam_2_Normalized) < margenDeError and partido[llaves[2]] == 'x':
                numHits += 1
        else:
            if printData and printDataForMaxProb:
                print(team_1.name, round(pointsTeam_1_Normalized, 2), round(pointsTeam_2_Normalized, 2), team_2.name, partido['Arbitro'])

    porcentajeAcierto = 100 * numHits / len(resultadosTotalDeReferencia)
    return porcentajeAcierto, margenDeError


###################################################################################################################################################################
# INPUT DATA #
URL_Ref = 'https://www.laliga.com/laliga-santander/resultados'
#Un ejemplo de URL con Resultados para comprobar el programa: 'https://www.laliga.com/laliga-santander/resultados/2022-23/jornada-26'
in_this_link_there_are_results_Ref = False
maxValueOfMatchsCalculated_Ref = 4

###################################################################################################################################################################
listOfPrimera = getDataOfMaxEfficiency(URL_Ref, in_this_link_there_are_results_Ref, maxValueOfMatchsCalculated_Ref)

