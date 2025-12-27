import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;
import java.io.IOException;

public class JavaBackend {
    public static void main(String[] args) throws Exception {
        int port = 5000;
        System.out.println("JavaBackend: listening on port " + port);
        try (ServerSocket server = new ServerSocket(port)) {
            while (true) {
                Socket client = server.accept();
                new Thread(new ClientHandler(client)).start();
            }
        }
    }

    static class ClientHandler implements Runnable {
        private final Socket socket;

        ClientHandler(Socket socket) {
            this.socket = socket;
        }

        @Override
        public void run() {
            try (BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                 PrintWriter out = new PrintWriter(socket.getOutputStream(), true)) {

                String line;
                while ((line = in.readLine()) != null) {
                    System.out.println("Received: " + line);
                    line = line.trim();
                    if (line.equalsIgnoreCase("HELLO")) {
                        out.println("{\"status\":\"ok\",\"message\":\"Java backend ready\"}");
                    } else if (line.equalsIgnoreCase("START")) {
                        out.println("{\"status\":\"ok\",\"table\":[]}");
                    } else if (line.toUpperCase().startsWith("PLAY")) {
                        // echo back a simple acknowledgement
                        out.println("{\"status\":\"ok\",\"played\":true,\"cmd\":\"" + escape(line) + "\"}");
                    } else if (line.equalsIgnoreCase("QUIT")) {
                        out.println("{\"status\":\"bye\"}");
                        break;
                    } else {
                        out.println("{\"status\":\"error\",\"message\":\"unknown command\"}");
                    }
                }
            } catch (IOException e) {
                System.err.println("Client handler error: " + e.getMessage());
            } finally {
                try {
                    socket.close();
                } catch (IOException ignored) {}
            }
        }

        private String escape(String s) {
            return s.replace("\\", "\\\\").replace("\"", "\\\"");
        }
    }
}
