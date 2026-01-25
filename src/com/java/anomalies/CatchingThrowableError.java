package com.java.anomalies;


/**
 * Anomaly: CatchingThrowableError
 * 
 * Example:
 * catch (Throwable t)
 * 
 * Output:
 * Caught a Throwable! This is dangerous.
 * 
 * Solution:
 * Throwable is the parent of both Exception and Error. Errors (like OutOfMemoryError or StackOverflowError) are thrown by the JVM when the environment is fundamentally broken. Catching Throwable means you're swallowing these fatal errors instead of letting the app die cleanly.
 * 
 * Expected:
 * Catching Exception is usually enough.
 */
public class CatchingThrowableError {
    public static void main(String[] args) {
        try {
            // Running some code...
            throw new OutOfMemoryError("Fake OOM");
        } catch (Exception e) {
            System.out.println("Caught an Exception");
        } catch (Throwable t) {
            System.out.println("Caught a Throwable! This is dangerous.");
        }
    }
}
