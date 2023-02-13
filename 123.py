import pandas


class Equipo:
    name = ""
    equiposQueHaGanado = []
    equiposQueHaPerdido = []
    puntosGanados = 0
    puntosPerdidos = 0

    def __init__(self, name, ganados, perdidos):
        self.name = name
        self.equiposQueHaGanado = ganados
        self.equiposQueHaPerdido = perdidos


listaDeEquipos = []
excel = pandas.read_excel("Bets.xlsx", header=None).to_numpy()
equiposGanadosIterados = []
equiposPerdidosIterados = []

#  Creacion de equipos
for row in excel[1:]:
    equipo = Equipo(row[0], [],[])
    listaDeEquipos.append(equipo)

#   A que equipos ha ganado y perdido cada equipo
for i in range(len(excel)):
    for j in range(len(excel)):
        if excel[i][j] == "G":
            listaDeEquipos[i - 1].equiposQueHaGanado.append(listaDeEquipos[j - 1])
        elif str(excel[i][j]) == "nan":
            listaDeEquipos[i - 1].equiposQueHaPerdido.append(listaDeEquipos[j - 1])


    def CalculatePoints(iteraciones):
        for equipo in listaDeEquipos:
            calculateWinningPoints(iteraciones, equipo, equipo, [])
            calculateLosingPoints(iteraciones, equipo, equipo, [])


    def calculateWinningPoints(iteration, teamToCheck, teamToAddPoints, teamsCountedAlready):
        if (iteration <= 0): return
        for winAgainst in teamToCheck.equiposQueHaGanado:
            teamToAddPoints.puntosGanados += 1
            if winAgainst in teamsCountedAlready:
                continue
            iteration -= 1
            teamsCountedAlready.append(winAgainst)
            calculateWinningPoints(iteration, winAgainst, teamToAddPoints, teamsCountedAlready)

    def calculateLosingPoints(iteration, teamToCheck, teamToAddPoints, teamsCountedAlready):
        if (iteration <= 0): return
        for lostAgainst in teamToCheck.equiposQueHaPerdido:
            teamToAddPoints.puntosPerdidos += 1
            if lostAgainst in teamsCountedAlready:
                continue
            iteration -= 1
            teamsCountedAlready.append(lostAgainst)
            calculateLosingPoints(iteration, lostAgainst, teamToAddPoints, teamsCountedAlready)

CalculatePoints(500)

#   Imprime por pantalla el resultado
listaDeEquipos.sort(key=lambda x: x.puntosGanados, reverse=True)
for equipo in listaDeEquipos:
    print(equipo.name, ": ", equipo.puntosGanados, equipo.puntosPerdidos)
