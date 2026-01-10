package com.example.scopa.player;

import com.example.scopa.model.Card;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Objects;

/**
 * Base player with a name and a hand of cards.
 */
public abstract class Player {
    private final String name;
    private final List<Card> hand = new ArrayList<>();
    private final List<Card> capturedCards = new ArrayList<>();
    private int scopaCount = 0;

    protected Player(String name) {
        this.name = Objects.requireNonNull(name, "name");
    }

    public String getName() {
        return name;
    }

    public List<Card> getHand() {
        return Collections.unmodifiableList(hand);
    }

    public void giveCards(List<Card> cards) {
        hand.addAll(cards);
    }

    public Card removeFromHand(int index) {
        if (index < 0 || index >= hand.size()) {
            throw new IllegalArgumentException("Invalid hand index: " + index);
        }
        return hand.remove(index);
    }

    public void addCapturedCards(List<Card> cards) {
        capturedCards.addAll(cards);
    }

    public List<Card> getCapturedCards() {
        return Collections.unmodifiableList(capturedCards);
    }

    public void incrementScopa() {
        scopaCount++;
    }

    public int getScopaCount() {
        return scopaCount;
    }

    public void clearHand() {
        hand.clear();
    }

    public void clearCaptured() {
        capturedCards.clear();
        scopaCount = 0;
    }
}
