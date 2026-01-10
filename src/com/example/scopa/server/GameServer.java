package com.example.scopa.server;

import com.example.scopa.game.ScopaGame;
import com.example.scopa.model.Card;
import com.example.scopa.player.HumanPlayer;
import com.example.scopa.rules.ScopaRules;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;
import java.io.IOException;
import java.util.List;

/**
 * GameServer that handles Scopa game logic and communicates with the frontend via JSON over TCP.
 */
public class GameServer {
    private static final int PORT = 5000;
    
    public static void main(String[] args) throws Exception {
        System.out.println("Scopa GameServer: listening on port " + PORT);
        try (ServerSocket server = new ServerSocket(PORT)) {
            while (true) {
                Socket client = server.accept();
                new Thread(new GameHandler(client)).start();
            }
        }
    }

    static class GameHandler implements Runnable {
        private final Socket socket;
        private ScopaGame game;

        GameHandler(Socket socket) {
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
                    
                    String response = handleCommand(line);
                    out.println(response);
                }
            } catch (IOException e) {
                System.err.println("Client handler error: " + e.getMessage());
            } finally {
                try {
                    socket.close();
                } catch (IOException ignored) {}
            }
        }

        private String handleCommand(String cmd) {
            String[] parts = cmd.split(" ", 2);
            String action = parts[0].toUpperCase();

            try {
                switch (action) {
                    case "HELLO":
                        return "{\"status\":\"ok\",\"message\":\"Scopa Game Server Ready\"}";
                    
                    case "START":
                        return handleStart();
                    
                    case "STATE":
                        return handleGetState();
                    
                    case "PLAY":
                        if (parts.length < 2) {
                            return "{\"status\":\"error\",\"message\":\"PLAY requires parameters: handIndex captureIndex\"}";
                        }
                        return handlePlay(parts[1]);
                    
                    case "CAPTURES":
                        if (parts.length < 2) {
                            return "{\"status\":\"error\",\"message\":\"CAPTURES requires parameter: handIndex\"}";
                        }
                        return handleGetCaptures(parts[1]);
                    
                    case "FINALIZE":
                        return handleFinalize();
                    
                    case "SCORE":
                        return handleScore();
                    
                    case "QUIT":
                        return "{\"status\":\"bye\"}";
                    
                    default:
                        return "{\"status\":\"error\",\"message\":\"Unknown command: " + escape(action) + "\"}";
                }
            } catch (Exception e) {
                return "{\"status\":\"error\",\"message\":\"" + escape(e.getMessage()) + "\"}";
            }
        }

        private String handleStart() {
            game = ScopaGame.twoPlayer(
                new HumanPlayer("Player 1"),
                new HumanPlayer("Player 2")
            );
            game.startNewRound();
            return buildStateJson();
        }

        private String handleGetState() {
            if (game == null) {
                return "{\"status\":\"error\",\"message\":\"Game not started. Use START command first.\"}";
            }
            return buildStateJson();
        }

        private String handlePlay(String params) {
            if (game == null) {
                return "{\"status\":\"error\",\"message\":\"Game not started\"}";
            }

            try {
                String[] parts = params.split(" ");
                int handIndex = Integer.parseInt(parts[0]);
                int captureIndex = parts.length > 1 ? Integer.parseInt(parts[1]) : -1;

                boolean success = game.playCard(handIndex, captureIndex);
                if (!success) {
                    return "{\"status\":\"error\",\"message\":\"Invalid play\"}";
                }

                return buildStateJson();
            } catch (NumberFormatException e) {
                return "{\"status\":\"error\",\"message\":\"Invalid parameters\"}";
            }
        }

        private String handleGetCaptures(String handIndexStr) {
            if (game == null) {
                return "{\"status\":\"error\",\"message\":\"Game not started\"}";
            }

            try {
                int handIndex = Integer.parseInt(handIndexStr.trim());
                List<Card> hand = game.getCurrentPlayer().getHand();
                
                if (handIndex < 0 || handIndex >= hand.size()) {
                    return "{\"status\":\"error\",\"message\":\"Invalid hand index\"}";
                }

                Card card = hand.get(handIndex);
                List<List<Card>> captures = ScopaRules.possibleCaptures(card, game.getTable().getOnTable());
                
                StringBuilder json = new StringBuilder();
                json.append("{\"status\":\"ok\",\"captures\":[");
                for (int i = 0; i < captures.size(); i++) {
                    if (i > 0) json.append(",");
                    json.append("[");
                    List<Card> capture = captures.get(i);
                    for (int j = 0; j < capture.size(); j++) {
                        if (j > 0) json.append(",");
                        json.append(cardToJson(capture.get(j)));
                    }
                    json.append("]");
                }
                json.append("]}");
                return json.toString();
            } catch (NumberFormatException e) {
                return "{\"status\":\"error\",\"message\":\"Invalid hand index\"}";
            }
        }

        private String handleFinalize() {
            if (game == null) {
                return "{\"status\":\"error\",\"message\":\"Game not started\"}";
            }
            
            if (!game.isRoundOver()) {
                return "{\"status\":\"error\",\"message\":\"Round not over yet\"}";
            }

            game.finalizeRound();
            return buildStateJson();
        }

        private String handleScore() {
            if (game == null) {
                return "{\"status\":\"error\",\"message\":\"Game not started\"}";
            }

            ScopaRules.Score score = game.calculateScore();
            return String.format("{\"status\":\"ok\",\"player1Score\":%d,\"player2Score\":%d}",
                score.getPlayer1Points(), score.getPlayer2Points());
        }

        private String buildStateJson() {
            StringBuilder json = new StringBuilder();
            json.append("{\"status\":\"ok\",");
            
            // Table cards
            json.append("\"table\":[");
            List<Card> tableCards = game.getTable().getOnTable();
            for (int i = 0; i < tableCards.size(); i++) {
                if (i > 0) json.append(",");
                json.append(cardToJson(tableCards.get(i)));
            }
            json.append("],");
            
            // Player 1
            json.append("\"player1\":{");
            json.append("\"name\":\"").append(escape(game.getPlayer1().getName())).append("\",");
            json.append("\"hand\":[");
            List<Card> p1Hand = game.getPlayer1().getHand();
            for (int i = 0; i < p1Hand.size(); i++) {
                if (i > 0) json.append(",");
                json.append(cardToJson(p1Hand.get(i)));
            }
            json.append("],");
            json.append("\"captured\":").append(game.getPlayer1().getCapturedCards().size()).append(",");
            json.append("\"scopas\":").append(game.getPlayer1().getScopaCount());
            json.append("},");
            
            // Player 2
            json.append("\"player2\":{");
            json.append("\"name\":\"").append(escape(game.getPlayer2().getName())).append("\",");
            json.append("\"hand\":[");
            List<Card> p2Hand = game.getPlayer2().getHand();
            for (int i = 0; i < p2Hand.size(); i++) {
                if (i > 0) json.append(",");
                json.append(cardToJson(p2Hand.get(i)));
            }
            json.append("],");
            json.append("\"captured\":").append(game.getPlayer2().getCapturedCards().size()).append(",");
            json.append("\"scopas\":").append(game.getPlayer2().getScopaCount());
            json.append("},");
            
            // Current player and game state
            json.append("\"currentPlayer\":\"").append(escape(game.getCurrentPlayer().getName())).append("\",");
            json.append("\"deckSize\":").append(game.getDeck().size()).append(",");
            json.append("\"roundOver\":").append(game.isRoundOver());
            
            json.append("}");
            return json.toString();
        }

        private String cardToJson(Card card) {
            return String.format("{\"suit\":\"%s\",\"rank\":\"%s\",\"value\":%d}",
                escape(card.getSuit().getDisplayName()),
                escape(card.getRank().getDisplayName()),
                card.value());
        }

        private String escape(String s) {
            if (s == null) return "";
            return s.replace("\\", "\\\\")
                   .replace("\"", "\\\"")
                   .replace("\n", "\\n")
                   .replace("\r", "\\r")
                   .replace("\t", "\\t");
        }
    }
}
