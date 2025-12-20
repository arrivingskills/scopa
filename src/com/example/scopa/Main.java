package com.example.scopa;

import com.example.scopa.game.ScopaGame;
import com.example.scopa.player.HumanPlayer;

/**
 * Entry point for a simple Scopa starter program.
 *
 * This is a minimal framework intended to help you start building a Scopa game.
 * The code compiles and runs, prints the initial table and hands after the deal,
 * and leaves TODOs where you can implement full game logic (captures, scoring, etc.).
 *
 * I implemented capture selection in ScopaRules.possibleCaptures using
 * exact-match precedence and a backtracking search for sum-equal combinations.
 * Added inline comments and a small helper.
 * https://www.geeksforgeeks.org/dsa/introduction-to-backtracking-2/
 *
 * Enforcing exact match precedence. This rule states that if you can capture
 * a single card of the same rank, you must do so, rather than capturing a
 * group of cards that sum to that rank.
 *
 * FUNCTION GetAllowedCaptures(played_card, cards_on_table):
 *     Initialize "results" as an empty list
 *
 *     # Step 1: Scan for Exact Matches
 *     FOR each card in cards_on_table:
 *         IF card.value equals played_card.value:
 *             Add [card] to "results"
 *
 *     # Step 2: Enforce Precedence
 *     IF "results" is NOT empty:
 *         # An exact match was found.
 *         # The rule requires we take the single card match.
 *         # We return immediately, ignoring any sum combinations.
 *         RETURN "results"
 *
 *     # Step 3: Fallback to Sum Combinations
 *     # If we are here, no single card matched the played card.
 *     # Now we search for combinations summing to the value.
 *
 *     CALL FindCombinations(cards_on_table, target=played_card.value) -> store in "sum_matches"
 *
 *     Add "sum_matches" to "results"
 *
 *     RETURN "results"
 *
 * Backtracking:
 * FUNCTION FindCombinations(cards_on_table, target_sum):
 *     Initialize an empty list called "results"
 *     Initialize an empty list called "current_path"
 *
 *     CALL Backtrack(cards_on_table, start_index=0, target_sum, current_path, results)
 *
 *     RETURN "results"
 *
 * FUNCTION Backtrack(cards, index, target, current_path, results):
 *     Calculate sum of cards in "current_path"
 *
 *     # Base Case: Success
 *     IF sum equals target:
 *         Add a copy of "current_path" to "results"
 *         RETURN
 *
 *     # Base Case: Failure (sum too high)
 *     IF sum is greater than target:
 *         RETURN
 *
 *     # Recursive Step: Try every card starting from the current index
 *     FOR i from index to length of cards:
 *         Get card at position i
 *
 *         # 1. Choose: Add card to the current path
 *         Add card to "current_path"
 *
 *         # 2. Explore: Recurse with the next index
 *         CALL Backtrack(cards, i + 1, target, current_path, results)
 *
 *         # 3. Un-choose: Remove the last card added (Backtrack)
 *         Remove card from "current_path"
 *
 */
public class Main {
    public static void main(String[] args) {
        ScopaGame game = ScopaGame.twoPlayer(
                new HumanPlayer("Player 1"),
                new HumanPlayer("Player 2")
        );

        game.startNewRound();
        game.printState();

        System.out.println();
        System.out.println("Next steps: implement capture selection(done), turn loop, and scoring in ScopaRules.");
    }
}
