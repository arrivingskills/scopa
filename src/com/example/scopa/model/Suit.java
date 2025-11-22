package com.example.scopa.model;

/**
 * Italian suits for a 40-card Scopa deck.
 */
public enum Suit {
    COINS("Coins"),
    CUPS("Cups"),
    SWORDS("Swords"),
    CLUBS("Clubs");

    private final String displayName;

    Suit(String displayName) {
        this.displayName = displayName;
    }

    public String getDisplayName() {
        return displayName;
    }
}
