package codes.blitz.game.message.game;

public record Debris(String id,
                     DebrisType debrisType,
                     String teamId,
                     Vector position,
                     Vector velocity,
                     double radius,
                     double damage, 
                     double bonusShieldDamage, 
                     double bonusHullDamage) {
}
