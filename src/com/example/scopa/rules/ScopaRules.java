package com.example.scopa.rules;

import com.example.scopa.model.Card;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/**
 * Rules helper for Scopa. This is deliberately minimal and includes TODOs to guide further work.
 */
public final class ScopaRules {

    private ScopaRules() {}

    /**
     * Compute all legal capture selections for a played card given the cards currently on the table.
     *
     * Scopa capture essentials implemented here:
     * - If there is any single card on the table whose value exactly matches the played card's value,
     *   that exact-match capture takes precedence and MUST be chosen over any multi-card sums. In that
     *   situation, only those single-card captures are returned.
     * - Otherwise, you may capture any non-empty combination of table cards whose values sum exactly
     *   to the value of the played card. All such combinations are returned.
     *
     * Notes / Simplifications:
     * - We only consider numeric values (Rank.getValue) for matching/summing. Suit does not matter
     *   for capture selection.
     * - We do not resolve further tie-breakers here (e.g., strategy of which combination to prefer);
     *   instead we return all legal options so a UI or higher-level logic can choose among them.
     * - Ordering of returned options: if exact matches exist, only singletons are returned; otherwise
     *   combinations are returned in lexicographic index order based on their position in tableCards.
     */
    public static List<List<Card>> possibleCaptures(Card playedCard, List<Card> tableCards) {
        if (playedCard == null || tableCards == null || tableCards.isEmpty()) {
            return Collections.emptyList();
        }

        final int target = playedCard.value();

        // 1) Exact-match precedence: gather all single cards equal to target.
        List<List<Card>> exactMatches = new ArrayList<>();
        for (Card c : tableCards) {
            if (c.value() == target) {
                // Wrap each match in its own list to represent a capture selection of that single card
                List<Card> singleton = new ArrayList<>(1);
                singleton.add(c);
                exactMatches.add(singleton);
            }
        }

        // If any exact single-card matches exist, they are the only legal captures.
        if (!exactMatches.isEmpty()) {
            return exactMatches;
        }

        // 2) Otherwise, find all combinations (size >= 1) whose sum equals target.
        //    We exclude singletons here implicitly since no singletons matched target (handled above),
        //    but the algorithm itself doesn't need to special-case that.
        List<List<Card>> results = new ArrayList<>();
        backtrackSums(tableCards, 0, target, new ArrayList<>(), 0, results);
        return results;
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

    // -------------------------
    // Internal helper methods
    // -------------------------

    /**
     * Backtracking helper to generate all combinations of table cards that sum to the target.
     *
     * We iterate with an index to avoid duplicate combinations and keep a deterministic order.
     *
     * @param table       the list of cards on the table
     * @param startIdx    the current index to consider from table
     * @param target      the remaining sum we need to reach
     * @param current     the working combination being built
     * @param currentSum  the sum of values in the current combination
     * @param results     the output list for all found combinations
     */
    private static void backtrackSums(List<Card> table,
                                      int startIdx,
                                      int target,
                                      List<Card> current,
                                      int currentSum,
                                      List<List<Card>> results) {
        if (currentSum == target) {
            // Found a valid combination; copy to results
            results.add(new ArrayList<>(current));
            // Do not return immediately; continuing would only add positive values and exceed target.
            // But we can early return since all ranks are positive (1..10) in this deck.
            return;
        }

        // Early termination: since all card values are >= 1, exceeding target means no further progress
        if (currentSum > target) {
            return;
        }

        for (int i = startIdx; i < table.size(); i++) {
            Card next = table.get(i);
            current.add(next);
            backtrackSums(table, i + 1, target, current, currentSum + next.value(), results);
            current.remove(current.size() - 1);
        }
    }
}
