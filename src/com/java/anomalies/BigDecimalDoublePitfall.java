package com.java.anomalies;
import java.math.BigDecimal;

/**
 * Anomaly: BigDecimalDoublePitfall
 * 
 * Example:
 * new BigDecimal(0.1)
 * 
 * Output:
 * 0.10000000000000000555111...\n0.1
 * 
 * Solution:
 * When you pass 0.1 as a double, you're passing an inexact value. BigDecimal faithfully stores that exact inexactness. Always use the String constructor for BigDecimal to get what you actually expect.
 * 
 * Expected:
 * Both should just be 0.1.
 */
public class BigDecimalDoublePitfall {
    public static void main(String[] args) {
        // If you want exact decimals, you use BigDecimal. 
        // But if you initialize it with a double, you're already in trouble.
        BigDecimal bad = new BigDecimal(0.1);
        BigDecimal good = new BigDecimal("0.1");
        
        System.out.println("Double init: " + bad);
        System.out.println("String init: " + good);
    }
}
