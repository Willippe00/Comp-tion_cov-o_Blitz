package codes.blitz.game.message.game.actions;

public record RotateTurretAction(String stationId, double angle, ActionType type) implements Action {
    public RotateTurretAction(String stationId, double angle) {
        this(stationId, angle, ActionType.TURRET_ROTATE);
    }
}
