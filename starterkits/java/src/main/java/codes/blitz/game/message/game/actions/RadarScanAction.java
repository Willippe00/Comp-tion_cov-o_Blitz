package codes.blitz.game.message.game.actions;

public record RadarScanAction(String stationId, String targetShip, ActionType type) implements Action {
    public RadarScanAction(String stationId, String targetShip) {
        this(stationId, targetShip, ActionType.RADAR_SCAN);
    }
}
