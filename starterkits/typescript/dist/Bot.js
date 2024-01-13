"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.Bot = void 0;
const GameInterface_1 = require("./GameInterface");
class Bot {
    constructor() {
        console.log("Initializing your super duper mega bot");
        // This method should be use to initialize some variables you will need throughout the game.
    }
    /*
     * Here is where the magic happens, for now the moves are random. I bet you can do better ;)
     */
    getNextMoves(gameMessage) {
        let actions = [];
        let team_id = gameMessage.currentTeamId;
        let my_ship = gameMessage.ships[team_id];
        let other_ships_ids = Object.keys(gameMessage.shipsPositions).filter(ship_id => ship_id != team_id);
        // Find who's not doing anything and try to give them a job.
        let idle_crewmates = my_ship.crew.filter(crewmate => crewmate.currentStation == null && crewmate.destination == null);
        for (let crewmate of idle_crewmates) {
            let visitable_stations = [...crewmate.distanceFromStations.shields, ...crewmate.distanceFromStations.turrets, ...crewmate.distanceFromStations.helms, ...crewmate.distanceFromStations.radars];
            let station_to_move_to = randomlyChoose(visitable_stations);
            actions.push({
                type: GameInterface_1.ActionTypes.CREW_MOVE,
                crewMemberId: crewmate.id,
                destination: station_to_move_to.stationPosition
            });
        }
        // Now crew members at stations should do something!
        let operatedTurretStations = my_ship.stations.turrets.filter(station => station.operator != null);
        for (let turret_station of operatedTurretStations) {
            let possible_actions = [
                {
                    type: GameInterface_1.ActionTypes.TURRET_LOOK_AT,
                    stationId: turret_station.id,
                    target: {
                        x: gameMessage.constants.world.width * Math.random(),
                        y: gameMessage.constants.world.height * Math.random(),
                    }
                },
                {
                    type: GameInterface_1.ActionTypes.TURRET_CHARGE,
                    stationId: turret_station.id,
                },
                {
                    type: GameInterface_1.ActionTypes.TURRET_CHARGE,
                    stationId: turret_station.id,
                },
            ];
            actions.push(randomlyChoose(possible_actions));
        }
        let operatedHelmStation = my_ship.stations.helms.filter(station => station.operator != null);
        if (operatedHelmStation.length > 0) {
            actions.push({
                type: GameInterface_1.ActionTypes.SHIP_ROTATE,
                angle: 360 * Math.random(),
            });
        }
        let operatedRadarStation = my_ship.stations.radars.filter(station => station.operator != null);
        for (let radar_station of operatedRadarStation) {
            actions.push({
                type: GameInterface_1.ActionTypes.RADAR_SCAN,
                stationId: radar_station.id,
                targetShip: randomlyChoose(other_ships_ids)
            });
        }
        // You can clearly do better than the random actions above. Have fun!!
        return actions;
    }
}
exports.Bot = Bot;
function randomlyChoose(arr) {
    return arr[Math.floor(arr.length * Math.random())];
}
//# sourceMappingURL=Bot.js.map