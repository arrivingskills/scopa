package com.example.scopa.model;

import java.util.Objects;

/**
 * A single card from an Italian 40-card deck used in Scopa.
 */
public final class Card {
    private final Suit suit;
    private final Rank rank;

    public Card(Suit suit, Rank rank) {
        this.suit = Objects.requireNonNull(suit, "suit");
        this.rank = Objects.requireNonNull(rank, "rank");
    }

    public Suit getSuit() {
        return suit;
    }

    public Rank getRank() {
        return rank;
    }

    public int value() {
        return rank.getValue();
    }

    @Override
    public String toString() {
        // Example: Ace of Coins (1)
        return rank.getDisplayName() + " of " + suit.getDisplayName() + " (" + rank.getValue() + ")";
    }
}
