package com.java.anomalies;
import java.util.concurrent.locks.*;

/**
 * Anomaly: LockedFairnessCost
 * 
 * Example:
 * new ReentrantLock(true)
 * 
 * Output:
 * Slower performance
 * 
 * Solution:
 * A fair lock gives it to the longest-waiting thread. This requires more context switching and overhead than a non-fair lock, which allows 'barging'—where a thread that just arrived can grab the lock if it's open.
 * 
 * Expected:
 * Same speed as normal locking.
 */
public class LockedFairnessCost {
    public static void main(String[] args) {
        // Fair locks prevent starvation but kill performance.
        Lock fairLock = new ReentrantLock(true);
        System.out.println("Fair locking enabled. Throughput will drop significantly.");
    }
}
