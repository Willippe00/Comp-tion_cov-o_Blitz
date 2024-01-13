package codes.blitz.game.message.game.constants;

public record TurretsConstants(boolean rotatable,
                               int rocketChargeCost,
                               int maxCharge,
                               Double rocketSpeed,
                               Double rocketRadius,
                               Double rocketDamage,
                               Double rocketBonusShieldDamage,
                               Double rocketBonusHullDamage)
{
}
