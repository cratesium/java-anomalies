package com.java.anomalies;
import java.util.concurrent.atomic.*;

/**
 * Anomaly: AtomicIntegerABA
 * 
 * Example:
 * compareAndSet(1, 3)
 * 
 * Output:
 * Did we succeed? true\nBUT WE MISSED...
 * 
 * Solution:
 * This is the classic ABA problem in lock-free programming. If variable 'a' is changed to 'b' and back to 'a', compareAndSet thinks nothing ever changed. To solve this in deep algorithms, Java provides AtomicStampedReference, which attaches a version counter to the object.
 * 
 * Expected:
 * It shouldn't succeed if something modified it in the interim.
 */
public class AtomicIntegerABA {
    public static void main(String[] args) {
        // We want to update an atomic value from 1 to 3, but only if it's currently 1.
        AtomicInteger val = new AtomicInteger(1);
        
        // Sneaky thread does: val.set(2); then quickly val.set(1);
        
        boolean success = val.compareAndSet(1, 3);
        System.out.println("Did we succeed? " + success);
        System.out.println("BUT WE MISSED THE INTERMEDIATE CHANGES!");
    }
}
