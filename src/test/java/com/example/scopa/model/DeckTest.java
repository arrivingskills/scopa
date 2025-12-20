package com.example.scopa.model;

import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Tests for `Deck` behaviour: resetting, shuffling (implicit), and dealing.
 *
 * Note: Because `shuffle()` uses randomness, we only assert deterministic
 * properties (counts, non-empty deals, and correct handling when fewer cards
 * are available than requested).
 */
public class DeckTest {

    @Test
    public void resetCreatesFortyCards() {
        Deck deck = new Deck();
        // By contract: an Italian Scopa deck contains 40 cards
        assertEquals(40, deck.size(), "Deck.reset() should initialize 40 cards");
    }

    @Test
    public void dealingReducesSizeAndReturnsRequestedNumber() {
        Deck deck = new Deck();
        List<Card> hand = deck.deal(3);
        assertEquals(3, hand.size(), "deal(3) should return three cards when available");
        assertEquals(37, deck.size(), "deck size should reduce by number of dealt cards");
    }

    @Test
    public void dealWhenNotEnoughCards_returnsRemaining() {
        Deck deck = new Deck();
        // Drain the deck fully by dealing 40
        List<Card> all = deck.deal(40);
        assertEquals(40, all.size());
        assertTrue(deck.isEmpty());

        // Request more than available (0 left) - should return an empty list
        List<Card> none = deck.deal(3);
        assertEquals(0, none.size());
    }
}
