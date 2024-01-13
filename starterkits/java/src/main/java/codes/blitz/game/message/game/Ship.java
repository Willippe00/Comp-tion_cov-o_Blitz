package codes.blitz.game.message.game;

import java.util.List;

public record Ship(String teamId,
                   Position worldPosition,
                   double currentHealth,
                   double currentShield,
                   double orientationDegrees,
                   List<Position> walkableTiles,
                   List<Crewmate> crew,
                   Stations stations) {
}
