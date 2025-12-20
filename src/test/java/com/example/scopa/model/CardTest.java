package com.example.scopa.model;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Unit tests for the immutable `Card` value object.
 *
 * These tests exercise basic accessors and the string representation so future
 * refactors of `toString()` or `value()` will be detected.
 */
public class CardTest {

    @Test
    public void valueAndToString_areConsistent() {
        // Arrange: create a known card
        Card card = new Card(Suit.COINS, Rank.SEVEN);

        // Act / Assert: `value()` must reflect the enum's declared integer value
        assertEquals(7, card.value(), "Card.value() must return the numeric rank value");

        // toString should contain both rank and suit display names and the numeric value
        String s = card.toString();
        assertTrue(s.contains("Seven"), "toString should contain rank display name");
        assertTrue(s.contains("Coins"), "toString should contain suit display name");
        assertTrue(s.contains("7") || s.contains("(7)"), "toString should mention numeric value");
    }
}
