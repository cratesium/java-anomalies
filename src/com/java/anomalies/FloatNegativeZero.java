package com.java.anomalies;


/**
 * Anomaly: FloatNegativeZero
 * 
 * Example:
 * 1.0 / -0.0
 * 
 * Output:
 * Is 0.0 == -0.0? true\n1.0 / 0.0 = Infinity\n1.0 / -0.0 = -Infinity
 * 
 * Solution:
 * In binary floating point, zero is represented with a sign bit intact. While logic operators (==) treat them as identical to comply with mathematical norms, functions like division expose the actual underlying bit distinction.
 * 
 * Expected:
 * Division should have the same result if they are truly equal.
 */
public class FloatNegativeZero {
    public static void main(String[] args) {
        // IEEE-754 is weird. Zero has a sign bit.
        System.out.println("Is 0.0 == -0.0? " + (0.0 == -0.0));
        
        System.out.println("But what if we divide 1 by them?");
        System.out.println("1.0 / 0.0 = " + (1.0 / 0.0));
        System.out.println("1.0 / -0.0 = " + (1.0 / -0.0));
    }
}
