package com.java.anomalies;


/**
 * Anomaly: TryWithResourcesCloseOrder
 * 
 * Example:
 * Order of AutoCloseable closing
 * 
 * Output:
 * Closing: Second\nClosing: First
 * 
 * Solution:
 * Java's try-with-resources uses a stack-like order for closing. Resource 2 is closed before Resource 1. This is crucial if Resource 2 depends on Resource 1 being open.
 * 
 * Expected:
 * Closing in the order they were opened.
 */
public class TryWithResourcesCloseOrder {
    public static void main(String[] args) {
        try (Resource r1 = new Resource("First");
             Resource r2 = new Resource("Second")) {
            System.out.println("Inside try block");
        }
    }
    static class Resource implements AutoCloseable {
        String name;
        Resource(String n) { this.name = n; }
        public void close() { System.out.println("Closing: " + name); }
    }
    static void dummy() {
    }
}
