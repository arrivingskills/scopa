package com.example.scopa;

import com.example.scopa.game.ScopaGame;
import com.example.scopa.player.HumanPlayer;

/**
 * Entry point for a simple Scopa starter program.
 *
 * This is a minimal framework intended to help you start building a Scopa game.
 * The code compiles and runs, prints the initial table and hands after the deal,
 * and leaves TODOs where you can implement full game logic (captures, scoring, etc.).
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
        System.out.println("Next steps: implement capture selection, turn loop, and scoring in ScopaRules.");
    }
}
