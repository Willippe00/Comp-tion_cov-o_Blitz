package codes.blitz.game.message.game;

import java.util.List;

public record DistanceFromStations(List<StationDistance> turrets, List<StationDistance> shields,
                                   List<StationDistance> radars, List<StationDistance> helms) {
}
