package codes.blitz.game.message.serialization;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.json.JsonMapper;

import codes.blitz.game.message.game.GameMessage;
import jakarta.websocket.DecodeException;
import jakarta.websocket.Decoder;

public class MessageDecoder implements Decoder.Text<GameMessage> {
    private static final JsonMapper jsonMapper = JsonMapperInstanceHolder.getInstance();

    @Override
    public GameMessage decode(String message) throws DecodeException {
        try {
            return jsonMapper.readValue(message, GameMessage.class);
        } catch (JsonProcessingException e) {
            throw new DecodeException(message, e.getMessage(), e);
        }
    }

    @Override
    public boolean willDecode(String s) {
        return (s != null);
    }
}