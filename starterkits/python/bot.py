import game_message
from game_message import *
from actions import *
import random


class Bot:
    def __init__(self):
        print("Initializing your super mega duper bot")

    def get_my_ship(self, game_message: GameMessage) -> Optional[Ship]:
        current_team_id = game_message.currentTeamId
        return game_message.ships.get(current_team_id)

    def is_in_same_quadrant(self, debris: Debris, ship: Ship, game_message: GameMessage):
        # Determiner si les positions existent
        if ship.worldPosition is None or debris.position is None:
            return False

        # Determiner le point milieu de la map
        demi_x = game_message.constants.world.width
        demi_y = game_message.constants.world.height

        # Etablir les quadrants du debris et du ship
        ship_quadrant = (ship.worldPosition.x >= demi_x, ship.worldPosition.y >= demi_y)
        debris_quadrant = (debris.position.x >= demi_x, debris.position.y >= demi_y)

        # Etablir la correspondance
        return ship_quadrant == debris_quadrant

    def interest_debris(self, target: Debris, ship: Ship, game_message: GameMessage):

        if target.debrisType == "LARGE" and self.is_in_same_quadrant(target, ship, game_message):
            return 0

        elif target.debrisType == "MEDIUM" and self.is_in_same_quadrant(target, ship, game_message):
            return 4
        elif target.debrisType == "LARGE":
            return 6
        else:
            return 7


    def interest_ship(self, target: Ship):

        if target.currentShield < 0:
            return 1
        elif target.currentShield < 50:
            return 2
        elif target.currentShield < 100:
            return 3
        else:
            return 5

    def target_priorities(self, game_message: GameMessage):
        targets = {}

        for team_id, ship in game_message.ships.items():
            if team_id != game_message.currentTeamId:
                targets[ship.teamId] = {
                    'interest': self.interest_ship(ship),
                    'position': ship.worldPosition
                }

        for debris in game_message.debris:
            targets[debris.id] = {
                'interest': self.interest_debris(debris, game_message),
                'position': debris.position
            }

        sorted_targets = dict(sorted(targets.items(), key=lambda item: item[1]))
        return sorted_targets

    def turret_station_position(self, game_message: GameMessage, team_id: str, turret_id: str):
        if team_id in game_message.shipsPositions:
            team = game_message.ships.get(team_id)

            if team:
                stations_data = team.stations
                if stations_data:
                    turrets = stations_data.turrets

                    specific_turret = next((turret for turret in turrets if turret.id == turret_id), None)

                    if specific_turret:
                        return specific_turret.worldPosition
        return None




    def get_next_move(self, game_message: GameMessage):
        """
        Here is where the magic happens, for now the moves are not very good. I bet you can do better ;)
        """

        actions = []

        team_id = game_message.currentTeamId
        my_ship = game_message.ships.get(team_id)
        other_ships_ids = [shipId for shipId in game_message.shipsPositions.keys() if shipId != team_id]

        # Find who's not doing anything and try to give them a job?
        idle_crewmates = [crewmate for crewmate in my_ship.crew if
                          crewmate.currentStation is None and crewmate.destination is None]

        for crewmate in idle_crewmates:
            visitable_stations = crewmate.distanceFromStations.shields + crewmate.distanceFromStations.turrets + crewmate.distanceFromStations.helms + crewmate.distanceFromStations.radars
            station_to_move_to = random.choice(visitable_stations)
            actions.append(CrewMoveAction(crewmate.id, station_to_move_to.stationPosition))

        # Now crew members at stations should do something!
        operatedTurretStations = [station for station in my_ship.stations.turrets if station.operator is not None]
        print("action")
        for turret_station in operatedTurretStations:
            possible_actions = [
                # Charge the turret.
                TurretChargeAction(turret_station.id),
                # Aim the turret itself.
                TurretLookAtAction(turret_station.id,
                                   self.look_Target(turret_station.id, game_message)
                                   ),

                # Shoot!
                TurretShootAction(turret_station.id)
            ]

            actions.append(random.choice(possible_actions))

        operatedHelmStation = [station for station in my_ship.stations.helms if station.operator is not None]
        if operatedHelmStation:
           # actions.append(ShipRotateAction(random.uniform(0, 360)))
           print("tourne")

        operatedRadarStation = [station for station in my_ship.stations.radars if station.operator is not None]
        for radar_station in operatedRadarStation:
            actions.append(RadarScanAction(radar_station.id, random.choice(other_ships_ids)))

        # You can clearly do better than the random actions above! Have fun!
        return actions

    def look_Target(self, turret_id, game_message: GameMessage):
        cible = None
        cicle_indect =0
        for debris in game_message.debris:
            index = self.interest_debris(debris, self.get_my_ship(game_message), game_message)
            if index > cicle_indect:
                cible = debris
                cicle_indect = index
                print(index)
        return self.AimBot(cible, game_message, turret_id)

    def AimBot(self, AsteroideCible: Debris, game_message: GameMessage, turret_id):
        
        diffVitesse = self.soustractionVecteur(AsteroideCible.velocity,
                                               self.volicityApproxyMissil(AsteroideCible, game_message, turret_id))
        diffPosition = self.soustractionVecteur(
            self.Turret_Station_Position(game_message, game_message.currentTeamId, turret_id), AsteroideCible.position)
        TempsColision = self.produitScalaire(diffPosition, diffVitesse) / self.produitScalaire(diffVitesse,
                                                                                               diffVitesse)

        posIntercept = self.additionVecteur(AsteroideCible.position,
                                            self.multiplicationVecteur(AsteroideCible.velocity, TempsColision))

        return posIntercept

    def norme(self, v):
        return (v.x ** 2 + v.y ** 2) ** 0.5

    def produitScalaire(self, v1, v2):
        return v1.x * v2.x + v1.y * v2.y

    def soustractionVecteur(self, v1, v2):
        return Vector(v1.x - v2.x, v1.y - v2.y)

    def additionVecteur(self, v1, v2):
        return Vector(v1.x + v2.x, v1.y + v2.y)

    def multiplicationVecteur(self, v, scalaire):
        return Vector(v.x * scalaire, v.y * scalaire)

    def volicityApproxyMissil(self, AsteroideCible: Debris, game_message: GameMessage, turet_id):
        positionEstimee = AsteroideCible.position

        for _ in range(70):  # 10 itérations pour convergence (ajuster si nécessaire)
            vecteur_vitesse_missile = self.volicityApproxyMissil_vers_position(positionEstimee, game_message, turet_id)
            delta_temps = self.tempsImpact(positionEstimee,
                                           self.Turret_Station_Position(game_message, game_message.currentTeamId,
                                                                        turet_id), self.norme(vecteur_vitesse_missile))
            positionEstimee = self.estimerPosition(AsteroideCible.position, AsteroideCible.velocity, delta_temps)
        return self.volicityApproxyMissil_vers_position(positionEstimee, game_message, turet_id)

    def volicityApproxyMissil_vers_position(self, position, game_message: GameMessage, turet_id):
        VitesseMissile = game_message.constants.ship.stations.turretInfos[turet_id].rocketSpeed

        """Version originale de la fonction pour obtenir la vélocité du missile vers une position donnée."""
        VecteurDirection = self.soustractionVecteur(position, self.turret_station_position(game_message,
                                                                                           game_message.currentTeamId,
                                                                                           turet_id))
        longueur = self.norme(VecteurDirection)
        VecteurUnitaire = Vector(VecteurDirection.x / longueur, VecteurDirection.y / longueur)
        return Vector(VitesseMissile * VecteurUnitaire.x, VitesseMissile * VecteurUnitaire.y)

    def tempsImpact(self, position_cible, position_lanceur, vitesse_missile):
        """Estime le temps nécessaire pour que le missile atteigne la cible."""
        vecteur_direction = self.soustractionVecteur(position_cible, position_lanceur)
        longueur = self.norme(vecteur_direction)
        return longueur / vitesse_missile

    def estimerPosition(self, positionAsteroide, vitesseAsteroide, delta_temps):
        """Estime la nouvelle position de l'astéroïde après un certain temps."""
        return Vector(positionAsteroide.x + vitesseAsteroide.x * delta_temps,
                      positionAsteroide.y + vitesseAsteroide.y * delta_temps)


