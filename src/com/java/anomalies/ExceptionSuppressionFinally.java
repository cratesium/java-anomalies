package com.java.anomalies;


/**
 * Anomaly: ExceptionSuppressionFinally
 * 
 * Example:
 * try-with-resources with throwing close()
 * 
 * Output:
 * Caught: Primary Error!\nSuppressed: Close Error!
 * 
 * Solution:
 * Unlike old-school finally blocks that completely swallow primary exceptions, try-with-resources captures the primary 'try' exception, and neatly 'attaches' the secondary 'close()' exception as an array of 'suppressed' errors, preserving all debugging info.
 * 
 * Expected:
 * The 'close' exception wipes out the try block exception.
 */
public class ExceptionSuppressionFinally {
    public static void main(String[] args) {
        try (BadResource br = new BadResource()) {
            throw new RuntimeException("Primary Error!");
        } catch (Exception e) {
            System.out.println("Caught: " + e.getMessage());
            System.out.println("Suppressed: " + e.getSuppressed()[0].getMessage());
        }
    }
    static class BadResource implements AutoCloseable {
        public void close() { throw new RuntimeException("Close Error!"); }
    }
    static void dummy() {
    }
}
