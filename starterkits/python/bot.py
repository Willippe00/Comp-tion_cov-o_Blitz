from game_message import *
from actions import *
import random

class Bot:
    def __init__(self):
        print("Initializing your super mega duper bot")


    def get_next_move(self, game_message: GameMessage):
        """
        Here is where the magic happens, for now the moves are not very good. I bet you can do better ;)
        """

        VitesseMissile = game_message.constants.ship.stations.turretInfos.rocketSpeed
        actions = []

        team_id = game_message.currentTeamId
        my_ship = game_message.ships.get(team_id)
        other_ships_ids = [shipId for shipId in game_message.shipsPositions.keys() if shipId != team_id]

        # Find who's not doing anything and try to give them a job?
        idle_crewmates = [crewmate for crewmate in my_ship.crew if crewmate.currentStation is None and crewmate.destination is None]

        for crewmate in idle_crewmates:
            visitable_stations = crewmate.distanceFromStations.shields + crewmate.distanceFromStations.turrets + crewmate.distanceFromStations.helms + crewmate.distanceFromStations.radars
            station_to_move_to = random.choice(visitable_stations)
            actions.append(CrewMoveAction(crewmate.id, station_to_move_to.stationPosition))

        # Now crew members at stations should do something!
        operatedTurretStations = [station for station in my_ship.stations.turrets if station.operator is not None]
        for turret_station in operatedTurretStations:
            possible_actions = [
                # Charge the turret.
                TurretChargeAction(turret_station.id),
                # Aim the turret itself.
                TurretLookAtAction(turret_station.id, 
                                   Vector(random.uniform(0, game_message.constants.world.width), random.uniform(0, game_message.constants.world.height))
                ),
                # Shoot!
                TurretShootAction(turret_station.id)
            ]

            actions.append(random.choice(possible_actions))

        operatedHelmStation = [station for station in my_ship.stations.helms if station.operator is not None]
        if operatedHelmStation:
            actions.append(ShipRotateAction(random.uniform(0, 360)))

        operatedRadarStation = [station for station in my_ship.stations.radars if station.operator is not None]
        for radar_station in operatedRadarStation:
            actions.append(RadarScanAction(radar_station.id, random.choice(other_ships_ids)))

        # You can clearly do better than the random actions above! Have fun!
        return actions



    def look_Target(self, turret_id):

        postion = self.AimBot(turret_id)

    def AimBot(self, AsteroideCible: GameMessage.debris, game_message: GameMessage, turret_id):
            diffVitesse = self.soustractionVecteur(AsteroideCible.velocity, self.volicityApproxyMissil(AsteroideCible))
            diffPosition = self.soustractionVecteur(self.PosCanon, AsteroideCible.position)
            TempsColision = self.produitScalaire(diffPosition, diffVitesse) / self.produitScalaire(diffVitesse,
                                                                                                   diffVitesse)

            posIntercept = self.additionVecteur(AsteroideCible.position,
                                                self.multiplicationVecteur(AsteroideCible.velocity, TempsColision))

            return posIntercept


    def norme(self,v):
        return (v.x**2 + v.y**2)**0.5
    def produitScalaire(self,v1, v2):
        return v1.x * v2.x + v1.y * v2.y


    def soustractionVecteur(self, v1, v2):
        return Vector(v1.x - v2.x, v1.y - v2.y)


    def additionVecteur(self,v1, v2):
        return Vector(v1.x + v2.x, v1.y + v2.y)


    def multiplicationVecteur(self, v, scalaire):
        return Vector(v.x * scalaire, v.y * scalaire)

    def volicityApproxyMissil(self, AsteroideCible: GameMessage.debris):
        positionEstimee = AsteroideCible.position

        for _ in range(70):  # 10 itérations pour convergence (ajuster si nécessaire)
            vecteur_vitesse_missile = self.volicityApproxyMissil_vers_position(positionEstimee)
            delta_temps = self.tempsImpact(positionEstimee, self.PosCanon, self.norme(vecteur_vitesse_missile))
            positionEstimee = self.estimerPosition(AsteroideCible.position, AsteroideCible.velocity, delta_temps)
        return self.volicityApproxyMissil_vers_position(positionEstimee)

    def volicityApproxyMissil_vers_position(self, position):
        """Version originale de la fonction pour obtenir la vélocité du missile vers une position donnée."""
        VecteurDirection = self.soustractionVecteur(position, self.PosCanon)
        longueur = self.norme(VecteurDirection)
        VecteurUnitaire = Vector(VecteurDirection.x / longueur, VecteurDirection.y / longueur)
        return Vector(self.VitesseMissile * VecteurUnitaire.x, self.VitesseMissile * VecteurUnitaire.y)

    def tempsImpact(self, position_cible, position_lanceur, vitesse_missile):
        """Estime le temps nécessaire pour que le missile atteigne la cible."""
        vecteur_direction = self.soustractionVecteur(position_cible, position_lanceur)
        longueur = self.norme(vecteur_direction)
        return longueur / vitesse_missile

    def estimerPosition(self, positionAsteroide, vitesseAsteroide, delta_temps):
        """Estime la nouvelle position de l'astéroïde après un certain temps."""
        return Vector(positionAsteroide.x + vitesseAsteroide.x * delta_temps,
                      positionAsteroide.y + vitesseAsteroide.y * delta_temps)