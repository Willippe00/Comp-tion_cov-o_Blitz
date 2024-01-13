package codes.blitz.game.message.game.actions;

public record TurretShootAction(String stationId, ActionType type) implements Action {
    public TurretShootAction(String stationId) {
        this(stationId, ActionType.TURRET_SHOOT);
    }
}
