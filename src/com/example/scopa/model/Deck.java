package com.example.scopa.model;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/**
 * A standard Italian 40-card deck for Scopa.
 */
public class Deck {
    private final List<Card> cards = new ArrayList<>();

    public Deck() {
        reset();
    }

    /**
     * Recreate a full 40-card deck in a canonical order and shuffle it.
     */
    public final void reset() {
        cards.clear();
        for (Suit suit : Suit.values()) {
            for (Rank rank : Rank.values()) {
                cards.add(new Card(suit, rank));
            }
        }
        shuffle();
    }

    public void shuffle() {
        Collections.shuffle(cards);
    }

    public boolean isEmpty() {
        return cards.isEmpty();
    }

    public int size() {
        return cards.size();
    }

    /**
     * Deal up to n cards. Returns a new list with the dealt cards.
     */
    public List<Card> deal(int n) {
        int count = Math.min(n, cards.size());
        List<Card> hand = new ArrayList<>(count);
        for (int i = 0; i < count; i++) {
            hand.add(cards.remove(cards.size() - 1));
        }
        return hand;
    }
}
