package codes.blitz.game;

import java.io.IOException;
import java.net.URI;
import java.util.concurrent.CountDownLatch;

import org.glassfish.tyrus.client.ClientManager;

import codes.blitz.game.websocket.WebsocketClient;
import jakarta.websocket.DeploymentException;

public class Blitz2024Application
{
    public static void main(String[] args)
    {
        CountDownLatch latch = new CountDownLatch(1);

        ClientManager client = ClientManager.createClient();
        try {
            client.connectToServer(new WebsocketClient(latch), URI.create("ws://127.0.0.1:8765"));
            latch.await();

        } catch (InterruptedException | IOException | DeploymentException e) {
            throw new RuntimeException(e);
        }
    }
}