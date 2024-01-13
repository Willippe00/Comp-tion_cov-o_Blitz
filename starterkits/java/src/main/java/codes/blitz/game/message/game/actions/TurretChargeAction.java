package codes.blitz.game.message.game.actions;

public record TurretChargeAction(String stationId, ActionType type) implements Action {
    public TurretChargeAction(String stationId) {
        this(stationId, ActionType.TURRET_CHARGE);
    }
}
