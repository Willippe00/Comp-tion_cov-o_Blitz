package codes.blitz.game.message.game.actions;

import codes.blitz.game.message.game.Vector;

public record ShipLookAtAction(Vector target, ActionType type) implements Action {
    public ShipLookAtAction(Vector target) {
        this(target, ActionType.SHIP_LOOK_AT);
    }
}
