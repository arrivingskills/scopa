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
     * Calculate scores for a round based on Scopa scoring rules.
     * 
     * Scoring categories:
     * - Cards (Carte): 1 point for the player with most cards captured
     * - Coins (Denari): 1 point for the player with most coin suit cards
     * - Sette Bello: 1 point for capturing the 7 of Coins
     * - Primiera: 1 point for the best primiera (specific point calculation per suit)
     * - Scopa: 1 point for each scopa (clearing the table)
     */
    public static Score scoreRound(List<Card> p1Captured, int p1Scopas,
                                    List<Card> p2Captured, int p2Scopas) {
        int p1Points = 0;
        int p2Points = 0;

        // 1. Most cards (ties don't award points)
        if (p1Captured.size() > p2Captured.size()) {
            p1Points++;
        } else if (p2Captured.size() > p1Captured.size()) {
            p2Points++;
        }

        // 2. Most coins
        int p1Coins = countCoins(p1Captured);
        int p2Coins = countCoins(p2Captured);
        if (p1Coins > p2Coins) {
            p1Points++;
        } else if (p2Coins > p1Coins) {
            p2Points++;
        }

        // 3. Sette Bello (7 of Coins)
        if (hasSetteBello(p1Captured)) {
            p1Points++;
        } else if (hasSetteBello(p2Captured)) {
            p2Points++;
        }

        // 4. Primiera
        int primieraResult = calculatePrimiera(p1Captured, p2Captured);
        if (primieraResult > 0) {
            p1Points++;
        } else if (primieraResult < 0) {
            p2Points++;
        }

        // 5. Scopas
        p1Points += p1Scopas;
        p2Points += p2Scopas;

        return new Score(p1Points, p2Points);
    }

    private static int countCoins(List<Card> cards) {
        int count = 0;
        for (Card c : cards) {
            if (c.getSuit().getDisplayName().equals("Coins")) {
                count++;
            }
        }
        return count;
    }

    private static boolean hasSetteBello(List<Card> cards) {
        for (Card c : cards) {
            if (c.getSuit().getDisplayName().equals("Coins") && c.value() == 7) {
                return true;
            }
        }
        return false;
    }

    /**
     * Calculate primiera for both players.
     * Returns > 0 if player 1 wins, < 0 if player 2 wins, 0 for tie or if either lacks all suits.
     * 
     * Primiera points per card (by rank):
     * 7 = 21, 6 = 18, Ace = 16, 5 = 15, 4 = 14, 3 = 13, 2 = 12, face cards = 10
     */
    private static int calculatePrimiera(List<Card> p1Cards, List<Card> p2Cards) {
        Integer p1Score = getPrimieraScore(p1Cards);
        Integer p2Score = getPrimieraScore(p2Cards);

        // If either player doesn't have all four suits, no one gets the primiera point
        if (p1Score == null || p2Score == null) {
            return 0;
        }

        return Integer.compare(p1Score, p2Score);
    }

    private static Integer getPrimieraScore(List<Card> cards) {
        // Find best card in each suit
        Integer coinsScore = null;
        Integer cupsScore = null;
        Integer swordsScore = null;
        Integer clubsScore = null;

        for (Card c : cards) {
            int cardPrimiera = getPrimieraValue(c);
            String suit = c.getSuit().getDisplayName();

            switch (suit) {
                case "Coins":
                    if (coinsScore == null || cardPrimiera > coinsScore) {
                        coinsScore = cardPrimiera;
                    }
                    break;
                case "Cups":
                    if (cupsScore == null || cardPrimiera > cupsScore) {
                        cupsScore = cardPrimiera;
                    }
                    break;
                case "Swords":
                    if (swordsScore == null || cardPrimiera > swordsScore) {
                        swordsScore = cardPrimiera;
                    }
                    break;
                case "Clubs":
                    if (clubsScore == null || cardPrimiera > clubsScore) {
                        clubsScore = cardPrimiera;
                    }
                    break;
            }
        }

        // Must have at least one card from each suit
        if (coinsScore == null || cupsScore == null || swordsScore == null || clubsScore == null) {
            return null;
        }

        return coinsScore + cupsScore + swordsScore + clubsScore;
    }

    private static int getPrimieraValue(Card card) {
        int rank = card.value();
        switch (rank) {
            case 7: return 21;
            case 6: return 18;
            case 1: return 16;  // Ace
            case 5: return 15;
            case 4: return 14;
            case 3: return 13;
            case 2: return 12;
            default: return 10;  // Jack (8), Knight (9), King (10)
        }
    }

    /**
     * Simple Score holder class.
     */
    public static class Score {
        private final int player1Points;
        private final int player2Points;

        public Score(int player1Points, int player2Points) {
            this.player1Points = player1Points;
            this.player2Points = player2Points;
        }

        public int getPlayer1Points() {
            return player1Points;
        }

        public int getPlayer2Points() {
            return player2Points;
        }

        @Override
        public String toString() {
            return "Player 1: " + player1Points + " points, Player 2: " + player2Points + " points";
        }
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
