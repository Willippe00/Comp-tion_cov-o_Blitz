package codes.blitz.game.message.game;

public record TurretStation(String id,
                            Vector worldPosition,
                            Position gridPosition,
                            double orientationDegrees,
                            double charge,
                            double cooldown,
                            String operator,
                            TurretType turretType)
{
}
