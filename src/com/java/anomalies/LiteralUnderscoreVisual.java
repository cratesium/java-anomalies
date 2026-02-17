package com.java.anomalies;


/**
 * Anomaly: LiteralUnderscoreVisual
 * 
 * Example:
 * int num = 1_000_000;
 * 
 * Output:
 * Are these numbers literally identical to the compiler? true
 * 
 * Solution:
 * Adding underscores to numbers doesn't change the byte-data. It's an excellent, free syntactic sugar tool to break up long financial figures, hexadecimal padding, or binary strings so developers can read them without squinting.
 * 
 * Expected:
 * It's treated as a String or causes an error.
 */
public class LiteralUnderscoreVisual {
    public static void main(String[] args) {
        int massiveA = 1000000;
        int massiveB = 1_000_000;
        
        System.out.println("Are these numbers literally identical to the compiler? " + (massiveA == massiveB));
    }
}
