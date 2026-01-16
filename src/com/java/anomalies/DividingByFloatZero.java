package com.java.anomalies;


/**
 * Anomaly: DividingByFloatZero
 * 
 * Example:
 * 1.0 / 0.0 vs 1 / 0
 * 
 * Output:
 * Infinity\nNaN
 * 
 * Solution:
 * Floating point arithmetic (IEEE 754) defines Infinity and NaN (Not-a-Number). It tries to give a symbolic result instead of crashing. Integers don't have these symbols, so they throw an ArithmeticException.
 * 
 * Expected:
 * Exception for both.
 */
public class DividingByFloatZero {
    public static void main(String[] args) {
        // Integer 1/0 throws error. Float 1.0/0.0 is different.
        System.out.println("1.0 / 0.0 = " + (1.0 / 0.0));
        System.out.println("0.0 / 0.0 = " + (0.0 / 0.0));
    }
}
