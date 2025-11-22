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

    public void clearHand() {
        hand.clear();
    }
}
