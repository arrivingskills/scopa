package com.example.scopa.model;

import org.junit.jupiter.api.Test;

import java.util.Arrays;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Tests for the lightweight `Table` class which represents cards on the table
 * and a simple event log used by the game engine.
 */
public class TableTest {

    @Test
    public void addAndRemoveCardsMaintainsListAndEvents() {
        Table table = new Table();

        Card a = new Card(Suit.CUPS, Rank.THREE);
        Card b = new Card(Suit.SWORDS, Rank.FOUR);

        table.addToTable(Arrays.asList(a, b));
        List<Card> on = table.getOnTable();
        assertEquals(2, on.size());

        table.removeFromTable(a);
        assertEquals(1, table.getOnTable().size());

        table.logEvent("Player1 captured 3+4");
        assertEquals(1, table.getEvents().size(), "Events should be recorded");
    }

    @Test
    public void clearAllRemovesCardsAndEvents() {
        Table table = new Table();
        table.addToTable(new Card(Suit.CLUBS, Rank.ACE));
        table.logEvent("something");
        table.clearAll();
        assertTrue(table.getOnTable().isEmpty());
        assertTrue(table.getEvents().isEmpty());
    }
}
