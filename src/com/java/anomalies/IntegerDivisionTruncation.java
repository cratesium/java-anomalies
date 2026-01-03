package com.java.anomalies;


/**
 * Anomaly: IntegerDivisionTruncation
 * 
 * Example:
 * double d = 1 / 2
 * 
 * Output:
 * 0.0
 * 
 * Solution:
 * Java performs integer division because both 1 and 2 are integers. 1/2 becomes 0. Only *after* the division is the result cast to a double. To fix it, use 1.0 / 2 or (double) 1 / 2.
 * 
 * Expected:
 * 0.5
 */
public class IntegerDivisionTruncation {
    public static void main(String[] args) {
        // Simple math: 1 divided by 2 is 0.5, right?
        double value = 1 / 2;
        System.out.println("Result of 1/2 stored in a double: " + value);
    }
}
