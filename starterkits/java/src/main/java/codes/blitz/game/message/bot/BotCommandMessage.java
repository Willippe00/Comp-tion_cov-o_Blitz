package codes.blitz.game.message.bot;

import java.util.List;

import codes.blitz.game.message.MessageType;
import codes.blitz.game.message.game.actions.Action;

public record BotCommandMessage(MessageType type, Number tick, List<Action> actions) {
    public BotCommandMessage(Number tick, List<Action> actions) {
        this(MessageType.COMMAND, tick, actions);
    }
}
