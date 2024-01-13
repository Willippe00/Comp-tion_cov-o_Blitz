package codes.blitz.game.message.game.actions;

import codes.blitz.game.message.game.Position;

public record MoveCrewAction(String crewMemberId, Position destination, ActionType type) implements Action {
    public MoveCrewAction(String crewMemberId, Position destination) {
        this(crewMemberId, destination, ActionType.CREW_MOVE);
    }
}
