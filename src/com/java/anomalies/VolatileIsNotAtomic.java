package com.java.anomalies;


/**
 * Anomaly: VolatileIsNotAtomic
 * 
 * Example:
 * volatile int count++;
 * 
 * Output:
 * Race condition potential
 * 
 * Solution:
 * Volatile only ensures that different threads see the latest value. It doesn't prevent two threads from reading the same value and trying to increment it simultaneously. Use AtomicInteger instead.
 * 
 * Expected:
 * Atomic updates.
 */
public class VolatileIsNotAtomic {
    public static void main(String[] args) {
        // Volatile makes things visible, but not safe for updates like count++.
        System.out.println("Volatile count++ is not thread-safe. It's a read-modify-write operation.");
    }
}
