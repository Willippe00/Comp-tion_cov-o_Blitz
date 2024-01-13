package codes.blitz.game.message.game;

public record Crewmate(String id,
                       Position gridPosition,
                       String name,
                       int age,
                       String socialInsurance,
                       Position destination,
                       String currentStation,
                       DistanceFromStations distanceFromStations) {
}
