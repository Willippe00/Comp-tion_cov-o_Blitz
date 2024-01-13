package codes.blitz.game.message.game.actions;

import codes.blitz.game.message.game.Vector;

public record TurretLookAtAction(String stationId, Vector target, ActionType type) implements Action {
    public TurretLookAtAction(String stationId, Vector target) {
        this(stationId, target, ActionType.TURRET_LOOK_AT);
    }
}
