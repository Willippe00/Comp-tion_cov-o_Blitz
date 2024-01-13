package codes.blitz.game.message.game.constants;

import java.util.Map;

import codes.blitz.game.message.game.TurretType;

public record StationConstants(Map<TurretType, TurretsConstants> turretInfos, ShieldConstants shield, RadarConstants radar) {
}
