package codes.blitz.game.message.game;

public record Projectile(String id, 
                         String teamId, 
                         Vector position, 
                         Vector velocity, 
                         double radius,
                         double damage, 
                         double bonusShieldDamage, 
                         double bonusHullDamage) {
}
