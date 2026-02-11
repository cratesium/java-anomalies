package com.java.anomalies;


/**
 * Anomaly: SynchronizedBlockNull
 * 
 * Example:
 * synchronized(null) { ... }
 * 
 * Output:
 * You can't lock on a null object!
 * 
 * Solution:
 * Every object in Java comes with a hidden monitor (lock) attached to the memory allocation. A null reference points to absolutely nothing, meaning there is no monitor to acquire. The JVM immediately responds with a NullPointerException.
 * 
 * Expected:
 * Sleeps until the lock is initialized.
 */
public class SynchronizedBlockNull {
    public static void main(String[] args) {
        Object lock = null;
        try {
            synchronized(lock) {
                System.out.println("In lock.");
            }
        } catch (NullPointerException e) {
            System.out.println("You can't lock on a null object!");
        }
    }
}
