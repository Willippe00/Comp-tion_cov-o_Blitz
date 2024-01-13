package codes.blitz.game.bot;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

import codes.blitz.game.message.game.*;
import codes.blitz.game.message.game.actions.*;

public class Bot {
    public Bot() {
        System.out.println("Initializing your super duper mega bot.");
    }

    /*
     * Here is where the magic happens. I bet you can do better ;)
     */
    public List<Action> getActions(GameMessage gameMessage) {
        List<Action> actions = new ArrayList<>();

        Ship myShip = gameMessage.ships().get(gameMessage.currentTeamId());
        List<String> otherShipsIds = new ArrayList<>(gameMessage.shipsPositions().keySet());
        otherShipsIds.removeIf(shipId -> shipId == gameMessage.currentTeamId());

        // Find who's not doing anything and try to give them a job.
        List<Crewmate> idleCrewmates = new ArrayList<>(myShip.crew());
        idleCrewmates.removeIf(crewmate -> crewmate.currentStation() != null || crewmate.destination() != null);

        for (Crewmate crewmate : idleCrewmates) {
            List<StationDistance> visitableStations = new ArrayList<>();
            visitableStations.addAll(crewmate.distanceFromStations().shields());
            visitableStations.addAll(crewmate.distanceFromStations().turrets());
            visitableStations.addAll(crewmate.distanceFromStations().helms());
            visitableStations.addAll(crewmate.distanceFromStations().radars());

            StationDistance stationToMoveTo = visitableStations.get(new Random().nextInt(visitableStations.size()));
            
            actions.add(new MoveCrewAction(crewmate.id(), stationToMoveTo.stationPosition()));
        }

        // Now crew members at stations should do something!
        List<TurretStation> operatedTurretStations = new ArrayList<>(myShip.stations().turrets());
        operatedTurretStations.removeIf(turretStation -> turretStation.operator() == null);
        for (TurretStation turretStation : operatedTurretStations) {
            int switchAction = new Random().nextInt(3);
            switch (switchAction) {
                case 0:
                    // Charge the turret
                    actions.add(new TurretChargeAction(turretStation.id()));
                    break;
                case 1:
                    // Aim at the turret itself
                    actions.add(new TurretLookAtAction(turretStation.id(), new Vector(gameMessage.constants().world().width() * Math.random(), gameMessage.constants().world().width() * Math.random())));
                    break;
                case 2:
                    // Shoot!
                    actions.add(new TurretShootAction(turretStation.id()));
                    break;
            }
        }

        List<HelmStation> operatedHelmStation = new ArrayList<>(myShip.stations().helms());
        operatedHelmStation.removeIf(helmStation -> helmStation.operator() == null);
        for (HelmStation helmStation : operatedHelmStation) {
            actions.add(new RotateShipAction(360 * Math.random()));
        }

        List<RadarStation> operatedRadarStations = new ArrayList<>(myShip.stations().radars());
        operatedRadarStations.removeIf(radarStation -> radarStation.operator() == null);
        for (RadarStation radarStation : operatedRadarStations) {
            actions.add(new RadarScanAction(radarStation.id(), otherShipsIds.get(new Random().nextInt(otherShipsIds.size()))));
        }

        // You can clearly do better than the random actions above. Have fun!!
        return actions;
    }
}