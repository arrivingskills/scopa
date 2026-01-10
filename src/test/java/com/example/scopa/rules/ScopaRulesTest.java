package com.example.scopa.rules;

import com.example.scopa.model.Card;
import com.example.scopa.model.Rank;
import com.example.scopa.model.Suit;
import org.junit.jupiter.api.Test;

import java.util.Arrays;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Focused tests for the `ScopaRules.possibleCaptures` helper.
 *
 * We validate the exact-match precedence rule and combination-generation when
 * exact matches are absent. The tests avoid asserting ordering beyond the
 * documented contract (singletons-only when exact matches exist).
 */
public class ScopaRulesTest {

    private int sum(List<Card> combo) {
        return combo.stream().mapToInt(Card::value).sum();
    }

    @Test
    public void noTableValues_returnsEmpty() {
        Card played = new Card(Suit.CUPS, Rank.FIVE);
        List<List<Card>> res = ScopaRules.possibleCaptures(played, Arrays.asList());
        assertTrue(res.isEmpty(), "No table cards -> no captures");
    }

    @Test
    public void exactMatchPrecedence_returnsOnlySingletons() {
        Card played = new Card(Suit.CUPS, Rank.SEVEN);
        Card seven = new Card(Suit.COINS, Rank.SEVEN);
        Card three = new Card(Suit.SWORDS, Rank.THREE);
        Card four = new Card(Suit.CLUBS, Rank.FOUR);

        // Although 3+4 == 7, the presence of a 7 on the table means only singleton
        // captures of the 7 should be legal according to the documented rule.
        List<List<Card>> res = ScopaRules.possibleCaptures(played, Arrays.asList(seven, three, four));
        assertFalse(res.isEmpty());
        // Every returned option must be a singleton with value == 7
        for (List<Card> opt : res) {
            assertEquals(1, opt.size(), "Exact-match precedence: only single-card captures returned");
            assertEquals(7, sum(opt));
        }
    }

    @Test
    public void combinationsReturned_whenNoExactMatch() {
        Card played = new Card(Suit.CUPS, Rank.SEVEN);
        Card a = new Card(Suit.COINS, Rank.THREE);
        Card b = new Card(Suit.SWORDS, Rank.FOUR);
        Card c = new Card(Suit.CLUBS, Rank.TWO);
        Card d = new Card(Suit.CUPS, Rank.FIVE);

        // No single 7 on table: allowed captures are combos summing to 7: 3+4 and 2+5
        List<List<Card>> res = ScopaRules.possibleCaptures(played, Arrays.asList(a, b, c, d));
        assertFalse(res.isEmpty(), "Should find combinations that sum to target");

        boolean found34 = res.stream().anyMatch(list -> list.size() == 2 && list.contains(a) && list.contains(b));
        boolean found25 = res.stream().anyMatch(list -> list.size() == 2 && list.contains(c) && list.contains(d));

        assertTrue(found34, "Combination 3+4 should be present");
        assertTrue(found25, "Combination 2+5 should be present");
        // Sanity: every returned combo must sum to 7
        for (List<Card> combo : res) {
            assertEquals(7, sum(combo), "Every capture candidate must sum to the played card's value");
        }
    }

    @Test
    public void whoTakesLast(){
        boolean p1_takes = ;
        


    }
}
