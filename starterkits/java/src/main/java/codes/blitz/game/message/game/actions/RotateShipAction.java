package codes.blitz.game.message.game.actions;

public record RotateShipAction(double angle, ActionType type) implements Action {
    public RotateShipAction(double angle) {
        this(angle, ActionType.SHIP_ROTATE);
    }
}
