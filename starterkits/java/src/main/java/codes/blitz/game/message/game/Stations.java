package codes.blitz.game.message.game;

import java.util.List;

public record Stations(List<TurretStation> turrets, List<ShieldStation> shields, List<RadarStation> radars, List<HelmStation> helms) {
}
