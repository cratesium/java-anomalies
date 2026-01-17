package com.java.anomalies;


/**
 * Anomaly: TheRoundingSurprise
 * 
 * Example:
 * Math.round(2.5) vs Math.round(-2.5)
 * 
 * Output:
 * 3\n-2
 * 
 * Solution:
 * Math.round(x) is actually floor(x + 0.5). For 2.5, it's floor(3.0) = 3. For -2.5, it's floor(-2.0) = -2. It always rounds towards positive infinity in 'tie' cases.
 * 
 * Expected:
 * -3 for the negative case.
 */
public class TheRoundingSurprise {
    public static void main(String[] args) {
        // Math.round is a bit simpler than you'd think.
        System.out.println("Round 2.5: " + Math.round(2.5));
        System.out.println("Round -2.5: " + Math.round(-2.5));
    }
}
