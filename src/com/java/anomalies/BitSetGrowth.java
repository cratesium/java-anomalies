package com.java.anomalies;
import java.util.BitSet;

/**
 * Anomaly: BitSetGrowth
 * 
 * Example:
 * new BitSet().set(100_000)
 * 
 * Output:
 * Internal size: 64\nIt elasticity grew! Internal size: 100032
 * 
 * Solution:
 * A BitSet uses a 'long' array to store bits efficiently. If you set a bit way out of bounds, it silently creates massive backing arrays to cover the distance. Passing an external ID as an index could trigger a huge memory spike.
 * 
 * Expected:
 * Out of bounds error.
 */
public class BitSetGrowth {
    public static void main(String[] args) {
        BitSet bits = new BitSet();
        bits.set(0);
        System.out.println("Internal size: " + bits.size());
        
        bits.set(100_000);
        System.out.println("It elasticity grew! Internal size: " + bits.size());
    }
}
