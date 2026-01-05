package com.java.anomalies;


/**
 * Anomaly: ShortIntegerOverflow
 * 
 * Example:
 * short val = 32767; val++
 * 
 * Output:
 * -32768
 * 
 * Solution:
 * This is standard wrap-around. Once you hit the maximum positive value for a signed type, adding one resets it to the minimum negative value. It's binary arithmetic at work.
 * 
 * Expected:
 * 32768
 */
public class ShortIntegerOverflow {
    public static void main(String[] args) {
        // Short is a 16-bit signed integer. 
        short val = 32767; // The maximum value
        val++;
        System.out.println("32767 + 1 = " + val);
    }
}
