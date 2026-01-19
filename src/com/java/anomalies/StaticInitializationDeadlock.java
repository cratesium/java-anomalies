package com.java.anomalies;


/**
 * Anomaly: StaticInitializationDeadlock
 * 
 * Example:
 * Circular static blocks
 * 
 * Output:
 * App hangs on startup
 * 
 * Solution:
 * When loading a class, the JVM acquires a lock for that class. If two classes try to load each other in their static initialization blocks, they will wait for each other's locks forever.
 * 
 * Expected:
 * A runtime error indicating a circular dependency.
 */
public class StaticInitializationDeadlock {
    public static void main(String[] args) {
        // Circular static dependencies can freeze your app.
        System.out.println("If class A's static block calls class B, and B calls A, you get a deadlock on the class monitor.");
    }
}
