package com.example.scopa.model;

/**
 * Ranks for an Italian 40-card deck used in Scopa.
 * Values range from 1 (Ace) to 10 (King).
 */
public enum Rank {
    ACE(1, "Ace"),
    TWO(2, "Two"),
    THREE(3, "Three"),
    FOUR(4, "Four"),
    FIVE(5, "Five"),
    SIX(6, "Six"),
    SEVEN(7, "Seven"),
    EIGHT(8, "Jack"),
    NINE(9, "Knight"),
    TEN(10, "King");

    private final int value;
    private final String displayName;

    Rank(int value, String displayName) {
        this.value = value;
        this.displayName = displayName;
    }

    public int getValue() {
        return value;
    }

    public String getDisplayName() {
        return displayName;
    }
}
