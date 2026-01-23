package com.java.anomalies;


/**
 * Anomaly: LongMultiplicationOverflow
 * 
 * Example:
 * long l = 1000 * 1000 * 1000 * 1000;
 * 
 * Output:
 * -727379968\n1000000000000
 * 
 * Solution:
 * In Java, integer literals are evaluated as 32-bit 'int' by default. The multiplication happens entirely in 32-bit space, overflowing multiple times before the final corrupted result is promoted to the 64-bit 'long'. Add an 'L' to the first number to force 64-bit math from the start.
 * 
 * Expected:
 * 1000000000000
 */
public class LongMultiplicationOverflow {
    public static void main(String[] args) {
        // Trying to calculate a trillion.
        long trillion = 1000 * 1000 * 1000 * 1000;
        System.out.println("1000^4 without the 'L' suffix: " + trillion);
        
        long rightWay = 1000L * 1000 * 1000 * 1000;
        System.out.println("With the 'L' suffix on the first number: " + rightWay);
    }
}
