package com.java.anomalies;


/**
 * Anomaly: LocalClassVariableCapture
 * 
 * Example:
 * Method local class variable scoping
 * 
 * Output:
 * I can access the method variable: 10
 * 
 * Solution:
 * Method-local inner classes are essentially 'anonymous classes' with explicit names. They can access the local variables of their enclosing method, but Java strictly mandates those variables be 'effectively final'. This protects your memory against state drifting asynchronously if the local frame collapses.
 * 
 * Expected:
 * The class can see the variable no matter what.
 */
public class LocalClassVariableCapture {
    public static void main(String[] args) {
        int variable = 10;
        
        class LocalInternalWorker {
            void show() {
                System.out.println("I can access the method variable: " + variable);
            }
        }
        
        // variable = 20; // If I uncomment this, the class compile fails.
        new LocalInternalWorker().show();
    }
}
