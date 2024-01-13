package codes.blitz.game.message.game;

import java.util.List;
import java.util.Map;

import codes.blitz.game.message.game.constants.Constants;

public record GameMessage(int currentTickNumber,
                          List<String> lastTickErrors,
                          String currentTeamId,
                          Constants constants,
                          List<Debris> debris,
                          List<Projectile> rockets,
                          Map<String, Position> shipsPositions,
                          Map<String, Ship> ships) {
}
