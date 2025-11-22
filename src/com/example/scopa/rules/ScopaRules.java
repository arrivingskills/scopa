package com.example.scopa.rules;

import com.example.scopa.model.Card;

import java.util.Collections;
import java.util.List;

/**
 * Rules helper for Scopa. This is deliberately minimal and includes TODOs to guide further work.
 */
public final class ScopaRules {

    private ScopaRules() {}

    /**
     * Placeholder for determining which table cards can be captured with a played card.
     * In Scopa, you may capture cards whose values sum to the value of the played card, or a single
     * card matching value. Full rules include precedence for exact match, etc.
     *
     * TODO: Implement full capture logic and tie-breaking rules.
     */
    public static List<List<Card>> possibleCaptures(Card playedCard, List<Card> tableCards) {
        // Returning empty for now. Implement search for combinations that sum to playedCard.value().
        return Collections.emptyList();
    }

    /**
     * Placeholder for scoring at the end of a round.
     *
     * Common scoring categories in Scopa:
     * - Most cards
     * - Most coins (denari)
     * - Sete bello (7 of coins)
     * - Primiera
     * - Scopa bonuses (capturing the last card on table)
     *
     * TODO: Design a Score object and compute totals per player/team.
     */
    public static void scoreRound() {
        // Intentionally empty starter method
    }
}
