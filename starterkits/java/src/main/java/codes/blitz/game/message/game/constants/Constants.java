package codes.blitz.game.message.game.constants;

import java.util.Map;

import codes.blitz.game.message.game.DebrisType;

public record Constants(World world, Map<DebrisType, DebrisInfo> debrisInfos, ShipConstants ship) {
}
