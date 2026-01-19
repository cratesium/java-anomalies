package com.java.anomalies;


/**
 * Anomaly: FinalizeUnpredictability
 * 
 * Example:
 * finalize()
 * 
 * Output:
 * Memory leaks or delayed cleanup
 * 
 * Solution:
 * The JVM does not guarantee when the garbage collector will run, or if it will run at all before the program exits. Relying on finalize() to close files or release resources is a classic mistake. Use try-with-resources instead.
 * 
 * Expected:
 * Immediate and guaranteed resource cleanup.
 */
public class FinalizeUnpredictability {
    public static void main(String[] args) {
        // finalize() doesn't work like C++ destructors.
        System.out.println("You can't rely on finalize() running promptly... or at all!");
    }
}
