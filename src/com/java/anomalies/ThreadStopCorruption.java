package com.java.anomalies;


/**
 * Anomaly: ThreadStopCorruption
 * 
 * Example:
 * Thread.stop()
 * 
 * Output:
 * Deprecated warning
 * 
 * Solution:
 * Thread.stop() forces the thread to throw a ThreadDeath error immediately. It releases all monitors (locks) the thread held, potentially exposing objects in an inconsistent, mid-update state to other threads.
 * 
 * Expected:
 * A clean termination of the thread.
 */
public class ThreadStopCorruption {
    public static void main(String[] args) {
        // Thread.stop() sounds useful, right?
        System.out.println("We shouldn't ever call Thread.stop(). It leaves monitors locked and state corrupted.");
        // t.stop();
    }
}
