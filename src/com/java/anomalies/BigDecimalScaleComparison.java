package com.java.anomalies;
import java.math.BigDecimal;

/**
 * Anomaly: BigDecimalScaleComparison
 * 
 * Example:
 * new BigDecimal("1.0").equals(new BigDecimal("1.00"))
 * 
 * Output:
 * false\ntrue
 * 
 * Solution:
 * BigDecimal encapsulates both the value AND the 'scale' (the precision zeros). The .equals() method dictates that if the scales are different (1 decimal vs 2 decimals), they are completely different objects. To verify mathematical equality, always rely on compareTo().
 * 
 * Expected:
 * .equals() to be true because math says 1.0 = 1.00.
 */
public class BigDecimalScaleComparison {
    public static void main(String[] args) {
        BigDecimal a = new BigDecimal("1.0");
        BigDecimal b = new BigDecimal("1.00");
        
        System.out.println("Are they .equals()? " + a.equals(b));
        System.out.println("Are they .compareTo() equal? " + (a.compareTo(b) == 0));
    }
}
