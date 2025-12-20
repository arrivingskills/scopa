package com.example.scopa.game;

import com.example.scopa.model.Card;
import com.example.scopa.model.Deck;
import com.example.scopa.model.Table;
import com.example.scopa.player.Player;

import java.util.List;

/**
 * Minimal game orchestration for a two-player Scopa variant.
 * This provides just enough to deal cards and print the initial state.
 */
public class ScopaGame {
    private final Player p1;
    private final Player p2;
    private final Deck deck = new Deck();
    private final Table table = new Table();

    private ScopaGame(Player p1, Player p2) {
        this.p1 = p1;
        this.p2 = p2;
    }

    public static ScopaGame twoPlayer(Player p1, Player p2) {
        return new ScopaGame(p1, p2);
    }

    /**
     * Start a new round by resetting deck, clearing hands, dealing 3 to each player and 4 to the table.
     */
    public void startNewRound() {
        // Reset deck and hands
        deck.reset();
        p1.clearHand();
        p2.clearHand();
        table.clearAll();

        // Initial deal: 3 to each player, 4 to table
        p1.giveCards(deck.deal(3));
        p2.giveCards(deck.deal(3));
        List<Card> tableCards = deck.deal(4);
        for (Card c : tableCards) {
            table.addToTable(c);
        }
    }

    public void printState() {
        System.out.println("Table: " + tableString());
        System.out.println(p1.getName() + " hand: " + cardsString(p1.getHand()));
        System.out.println(p2.getName() + " hand: " + cardsString(p2.getHand()));
        System.out.println("Deck size remaining: " + deck.size());
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
