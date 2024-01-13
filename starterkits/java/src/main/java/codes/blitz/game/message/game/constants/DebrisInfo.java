package codes.blitz.game.message.game.constants;

import java.util.List;

public record DebrisInfo(double radius, double approximateSpeed, double damage, List<ExplodesInto> explodesInto) {
}
