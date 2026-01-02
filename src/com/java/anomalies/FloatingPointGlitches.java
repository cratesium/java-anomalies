package com.java.anomalies;


/**
 * Anomaly: FloatingPointGlitches
 * 
 * Example:
 * 0.1 + 0.2 == 0.3
 * 
 * Output:
 * 0.30000000000000004\nfalse
 * 
 * Solution:
 * Decimals like 0.1 cannot be represented exactly in binary. It's like trying to write 1/3 as a decimal (0.333...). These tiny rounding errors add up, making direct equality checks dangerous.
 * 
 * Expected:
 * 0.3 and true
 */
public class FloatingPointGlitches {
    public static void main(String[] args) {
        // We all know 0.1 + 0.2 = 0.3, right? Not in binary floating point math.
        double result = 0.1 + 0.2;
        System.out.println("0.1 + 0.2 = " + result);
        System.out.println("Is it exactly 0.3? " + (result == 0.3));
    }
}
