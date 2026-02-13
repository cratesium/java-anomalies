package com.java.anomalies;


/**
 * Anomaly: MathHypotOverflow
 * 
 * Example:
 * Math.hypot(a, b)
 * 
 * Output:
 * ...Math.hypot() works perfectly: 1.414213562373095E300
 * 
 * Solution:
 * Math.hypot performs intermediate scaling. Instead of immediately squaring gigantic values and overflowing the double space, it scales the arguments down, computes the square root safely, and scales back up. Brilliant core library engineering.
 * 
 * Expected:
 * Infinity due to early square overflow.
 */
public class MathHypotOverflow {
    public static void main(String[] args) {
        // Pythagoras formula: a^2 + b^2 = c^2 (sqrt)
        double max = 1.0E300; // Almost overflow!
        
        System.out.println("A naive calc (max * max) would explode immediately into Infinity.");
        System.out.println("But Math.hypot(max, max) works perfectly: " + Math.hypot(max, max));
    }
}
