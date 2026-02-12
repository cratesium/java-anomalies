package com.java.anomalies;


/**
 * Anomaly: StackOverflowRecursion
 * 
 * Example:
 * void recurse(){ recurse(); }
 * 
 * Output:
 * java.lang.StackOverflowError
 * 
 * Solution:
 * Each method invocation carves out a 'stack frame' to hold its local primitives and pointers. The JVM only allows a fixed depth (a few thousand frames). Infinite loops push frames until you slam into the roof.
 * 
 * Expected:
 * An eventual OutOfMemoryException.
 */
public class StackOverflowRecursion {
    public static void main(String[] args) {
        System.out.println("JVM memory is split into Heap (objects) and Stack (method calls).");
        System.out.println("Infinite recursion doesn't out-of-memory the heap... it blows up the Stack!");
        // We'd write an infinite recursive method here, but we don't want to crash.
        // recurse();
    }
}
