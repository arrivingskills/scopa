package com.example.scopa.game;

import com.example.scopa.model.Card;
import com.example.scopa.model.Deck;
import com.example.scopa.model.Table;
import com.example.scopa.player.Player;
import com.example.scopa.rules.ScopaRules;

import java.util.List;

/**
 * Complete game orchestration for a two-player Scopa game.
 */
public class ScopaGame {
    private final Player p1;
    private final Player p2;
    private final Deck deck = new Deck();
    private final Table table = new Table();
    private int currentPlayerIndex = 0;  // 0 for p1, 1 for p2
    private Player lastCapturePlayer = null;

    private ScopaGame(Player p1, Player p2) {
        this.p1 = p1;
        this.p2 = p2;
    }

    public static ScopaGame twoPlayer(Player p1, Player p2) {
        return new ScopaGame(p1, p2);
    }

    public Player getPlayer1() {
        return p1;
    }

    public Player getPlayer2() {
        return p2;
    }

    public Player getCurrentPlayer() {
        return currentPlayerIndex == 0 ? p1 : p2;
    }

    public Table getTable() {
        return table;
    }

    public Deck getDeck() {
        return deck;
    }

    /**
     * Start a new round by resetting deck, clearing hands, dealing 3 to each player and 4 to the table.
     */
    public void startNewRound() {
        // Reset deck and hands
        deck.reset();
        p1.clearHand();
        p2.clearHand();
        p1.clearCaptured();
        p2.clearCaptured();
        table.clearAll();
        currentPlayerIndex = 0;
        lastCapturePlayer = null;

        // Initial deal: 3 to each player, 4 to table
        p1.giveCards(deck.deal(3));
        p2.giveCards(deck.deal(3));
        List<Card> tableCards = deck.deal(4);
        for (Card c : tableCards) {
            table.addToTable(c);
        }
    }

    /**
     * Play a card from the current player's hand.
     * @param handIndex index of card in player's hand
     * @param captureIndex index of capture option (from possibleCaptures), or -1 for no capture
     * @return true if the play was successful
     */
    public boolean playCard(int handIndex, int captureIndex) {
        Player current = getCurrentPlayer();
        
        if (handIndex < 0 || handIndex >= current.getHand().size()) {
            return false;
        }

        Card playedCard = current.removeFromHand(handIndex);
        List<List<Card>> captures = ScopaRules.possibleCaptures(playedCard, table.getOnTable());

        if (captureIndex >= 0 && captureIndex < captures.size()) {
            // Player makes a capture
            List<Card> capturedCards = captures.get(captureIndex);
            table.removeFromTable(capturedCards);
            
            // Add played card and captured cards to player's pile
            current.addCapturedCards(List.of(playedCard));
            current.addCapturedCards(capturedCards);
            
            lastCapturePlayer = current;
            
            // Check for scopa (table is now empty after capture)
            if (table.isEmpty() && !deck.isEmpty()) {
                current.incrementScopa();
                table.logEvent(current.getName() + " scored a SCOPA!");
            }
            
            table.logEvent(current.getName() + " played " + playedCard + " and captured " + capturedCards.size() + " card(s)");
        } else {
            // No capture, card goes to table
            table.addToTable(playedCard);
            table.logEvent(current.getName() + " played " + playedCard + " (no capture)");
        }

        // Switch to next player
        currentPlayerIndex = 1 - currentPlayerIndex;
        
        // Check if we need to deal more cards
        if (p1.getHand().isEmpty() && p2.getHand().isEmpty() && !deck.isEmpty()) {
            dealNextRound();
        }

        return true;
    }

    /**
     * Deal 3 cards to each player.
     */
    private void dealNextRound() {
        if (!deck.isEmpty()) {
            p1.giveCards(deck.deal(3));
            p2.giveCards(deck.deal(3));
        }
    }

    /**
     * Check if the round is over (no more cards to play).
     */
    public boolean isRoundOver() {
        return deck.isEmpty() && p1.getHand().isEmpty() && p2.getHand().isEmpty();
    }

    /**
     * Finalize the round: remaining table cards go to last capture player.
     */
    public void finalizeRound() {
        if (!table.isEmpty() && lastCapturePlayer != null) {
            List<Card> remaining = List.copyOf(table.getOnTable());
            lastCapturePlayer.addCapturedCards(remaining);
            table.getOnTable().forEach(c -> table.removeFromTable(c));
            table.logEvent("Remaining cards go to " + lastCapturePlayer.getName());
        }
    }

    /**
     * Calculate and return the score for this round.
     */
    public ScopaRules.Score calculateScore() {
        return ScopaRules.scoreRound(
            p1.getCapturedCards(), p1.getScopaCount(),
            p2.getCapturedCards(), p2.getScopaCount()
        );
    }

    public void printState() {
        System.out.println("Table: " + tableString());
        System.out.println(p1.getName() + " hand: " + cardsString(p1.getHand()) + 
                          " | Captured: " + p1.getCapturedCards().size() + " | Scopas: " + p1.getScopaCount());
        System.out.println(p2.getName() + " hand: " + cardsString(p2.getHand()) + 
                          " | Captured: " + p2.getCapturedCards().size() + " | Scopas: " + p2.getScopaCount());
        System.out.println("Deck size remaining: " + deck.size());
        System.out.println("Current player: " + getCurrentPlayer().getName());
    }

    private String tableString() {
        return cardsString(table.getOnTable());
    }

    private String cardsString(List<Card> cards) {
        if (cards.isEmpty()) return "(empty)";
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < cards.size(); i++) {
            if (i > 0) sb.append(", ");
            sb.append(cards.get(i));
        }
        return sb.toString();
    }

    public String playGame() {
        startNewRound();

        // Minimal "game loop" placeholder:
        // whenever both players have no cards, deal 3 each (if possible).
        while (!deck.isEmpty()) {
            if (p1.getHand().isEmpty() && p2.getHand().isEmpty()) {
                p1.giveCards(deck.deal(3));
                p2.giveCards(deck.deal(3));
            }

            // TODO: implement turns: each player plays a card, apply captures using ScopaRules, etc.
            break; // remove once turn logic is implemented
        }

        return "Game loop not implemented yet (dealing works, turns/captures still TODO).";
    }
}
