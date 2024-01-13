from game_message import *
from actions import *
import random

class Bot:
    def __init__(self):
        print("Initializing your super mega duper bot")

    def interest_debris(self, target: Debris):

        if target.debrisType == "LARGE":
            interest = 0
        elif target.debrisType == "MEDIUM":
            interest = 1
        elif target.debrisType == "SMALL":
            interest = 2
        else:
            interest = 3

        return interest

    def interest_ship(self, target: Ship):

        if target.currentShield < 0:
            interest = 0
        elif target.currentShield < 0.25:
            interest = 1
        elif target.currentShield < 0.5:
            interest = 2
        else:
            interest = 3

        return interest

    def Turret_Station_Position(self, game_message: GameMessage, team_id: str, turret_id: str):
        if team_id in game_message.shipsPositions:
            team = game_message.ships.get(team_id)

            if team:
                turrets = team['stations']['turrets']

                specific_turret = next((turret for turret in turrets if turret['id'] == turret_id), None)

                if specific_turret:
                    turret_position = specific_turret['worldPosition']
                    return turret_position
                else:
                    print("Specific turret not found")
                    return

            else:
                print("Team not found")
                return
        else:
            print("Team ID not found")
            return

    def get_next_move(self, game_message: GameMessage):
        """
        Here is where the magic happens, for now the moves are not very good. I bet you can do better ;)
        """
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
