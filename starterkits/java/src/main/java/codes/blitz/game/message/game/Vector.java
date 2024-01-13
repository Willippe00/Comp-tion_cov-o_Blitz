package codes.blitz.game.message.game;

public record Vector(double x, double y)
{
    public Position toPosition()
    {
        return new Position((int) x, (int) y);
    }
}