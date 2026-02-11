package com.java.anomalies;


/**
 * Anomaly: VolatileVisibilityGuarantee
 * 
 * Example:
 * private volatile boolean shutdown;
 * 
 * Output:
 * Cross-thread alignment
 * 
 * Solution:
 * 'volatile' establishes a formal 'happens-before' edge. Writes to the variable are immediately flushed across the memory barrier, invalidating the caches for all other threads. It's the cheapest but most subtle synchronization tool.
 * 
 * Expected:
 * All threads see memory exactly the same all the time.
 */
public class VolatileVisibilityGuarantee {
    public static void main(String[] args) {
        // 1. Thread A sets: done = true
        // 2. Thread B checking an old CPU cache loop never sees it!
        System.out.println("Normally, CPUs cache data aggressively.");
        System.out.println("Marking a variable 'volatile' forces the thread to bypass local cache and read/write directly to main RAM.");
    }
}
