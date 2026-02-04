package com.java.anomalies;


/**
 * Anomaly: StackTracePerformance
 * 
 * Example:
 * new Throwable().getStackTrace()
 * 
 * Output:
 * Performance hit.
 * 
 * Solution:
 * Instantiating an Exception forces the JVM to walk backward through the call stack to capture class names, method names, and line numbers. Never use exceptions for normal control flow (like validating forms) because this stack walk kills performance.
 * 
 * Expected:
 * It's instantaneous.
 */
public class StackTracePerformance {
    public static void main(String[] args) {
        System.out.println("Generating an exception is fast.");
        System.out.println("But resolving the stack trace (Throwable::fillInStackTrace) is EXTREMELY slow!");
        
        // This takes milliseconds, which is an eternity in code.
        new RuntimeException("Whoops! Unwinding the C++ JVM stack frames now...");
    }
}
