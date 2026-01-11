package com.java.anomalies;


/**
 * Anomaly: LambdaVariableCapture
 * 
 * Example:
 * Modify variable inside lambda
 * 
 * Output:
 * Compile Error
 * 
 * Solution:
 * Local variables used in a lambda must be 'final' or 'effectively final'. This is because lambdas can run later, and Java needs to ensure the value doesn't change unexpectedly after being captured.
 * 
 * Expected:
 * Direct access like any other variable.
 */
public class LambdaVariableCapture {
    public static void main(String[] args) {
        int counter = 0;
        // Runnable r = () -> System.out.println(counter); // Error!
        System.out.println("Lambda can only see variables that don't change.");
    }
}
