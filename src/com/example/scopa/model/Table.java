package com.example.scopa.model;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/**
 * Representation of the table state in Scopa: cards on the table and a simple log of captures.
 * This is intentionally lightweight as a starting point.
 */
public class Table {
    private final List<Card> onTable = new ArrayList<>();
    private final List<String> events = new ArrayList<>();

    public List<Card> getOnTable() {
        return Collections.unmodifiableList(onTable);
    }

    public void addToTable(List<Card> cards) {
        onTable.addAll(cards);
    }

    public void addToTable(Card card) {
        onTable.add(card);
    }

    public void removeFromTable(Card card) {
        onTable.remove(card);
    }

    public void logEvent(String event) {
        events.add(event);
    }

    public List<String> getEvents() {
        return Collections.unmodifiableList(events);
    }

    /**
     * Clear table cards and events for a fresh round.
     */
    public void clearAll() {
        onTable.clear();
        events.clear();
    }
}
