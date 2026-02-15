package com.java.anomalies;


/**
 * Anomaly: AssertKeywordDisabled
 * 
 * Example:
 * assert false;
 * 
 * Output:
 * The program continues to run...
 * 
 * Solution:
 * In Java, assertions are completely skipped and ignored by the JVM by default to optimize runtime speeds. You MUST supply the '-ea' (enable assertions) flag to the Java executable on startup to actually trigger AssertionError evaluations.
 * 
 * Expected:
 * Immediate crash.
 */
public class AssertKeywordDisabled {
    public static void main(String[] args) {
        System.out.println("I'm going to assert that 1 == 0, which is totally false.");
        assert 1 == 0 : "Mathematics is broken!";
        System.out.println("The program continues to run without error!");
    }
}
