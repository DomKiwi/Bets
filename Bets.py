def getProbabilityOfEachMatch(resultadosTotalDeReferencia, listOfTeams, there_is_data):
    numHits = 0
    max_error_margen = 0.5  # variar Dinamicamente
    porcentajeYMargenError = {}
    for iError in range(1, max_error_margen, 0.01):
        porcentajeDeAcierto, margenDeError = calculatePointsAndPorcentaje(resultadosTotalDeReferencia, listOfTeams, there_is_data, iError)
        porcentajeYMargenError[margenDeError] = porcentajeDeAcierto
    maxValuePorcentajeYMargenError = max(porcentajeYMargenError)
    porcentajeDeAciertoMaximo, margenDeErrorMaximo = calculatePointsAndPorcentaje(resultadosTotalDeReferencia, listOfTeams, there_is_data, porcentajeYMargenError[maxValuePorcentajeYMargenError])
    print('Para el numero de jornadas previas usadas obtengo un valor maximo de porcentaje de aciertos: ' + str(porcentajeDeAciertoMaximo) + ' con un margen de error para empates de: ' + str(margenDeErrorMaximo))

def calculatePointsAndPorcentaje(resultadosTotalDeReferencia, listOfTeams, there_is_data, margenDeError):
    numHits = 0
    for partido in resultadosTotalDeReferencia:
        llaves = list(partido.keys())
        team_1 = getEquipo(llaves[0], listOfTeams)
        team_2 = getEquipo(llaves[1], listOfTeams)
        pointsTeam_1 = team_1.puntosDeFuerza + team_2.puntosDeDebilidad
        pointsTeam_2 = team_2.puntosDeFuerza + team_1.puntosDeDebilidad
        minimumP = min([pointsTeam_1, pointsTeam_2])
        if minimumP == 0:
            minimumP = 1
        pointsTeam_1_Normalized = round(pointsTeam_1 / minimumP, 5)
        pointsTeam_2_Normalized = round(pointsTeam_2 / minimumP, 5)
        if there_is_data:
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
            print(team_1.name, round(pointsTeam_1_Normalized, 2), round(pointsTeam_2_Normalized, 2), team_2.name)

    porcentajeAcierto = 100 * numHits / len(resultadosTotalDeReferencia)
    return porcentajeAcierto, margenDeError