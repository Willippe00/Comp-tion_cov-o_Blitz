package codes.blitz.game.message.game;

public record Position(int x, int y) {
    public Vector toVector() {
        return new Vector(x, y);
    }
}
