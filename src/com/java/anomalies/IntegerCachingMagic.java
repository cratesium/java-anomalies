package com.java.anomalies;


/**
 * Anomaly: IntegerCachingMagic
 * 
 * Example:
 * Integer a=100, b=100; (a==b) vs Integer c=200, d=200; (c==d)
 * 
 * Output:
 * true\nfalse
 * 
 * Solution:
 * Basically, the JVM maintains a cache for Integer objects from -128 to 127. When you auto-box a number in this range, it reuses the same object. Outside that range? It creates a new one every time, breaking reference equality.
 * 
 * Expected:
 * You'd probably expect either 'true/true' or 'false/false' for consistency.
 */
public class IntegerCachingMagic {
    public static void main(String[] args) {
        // Most developers expect '==' to compare values, but for Objects it compares references.
        // However, Java does something clever (and confusing) with small numbers.
        Integer first = 100;
        Integer second = 100;
        System.out.println("Do 100 and 100 share the same object? " + (first == second)); // True!
        
        Integer third = 200;
        Integer fourth = 200;
        System.out.println("Do 200 and 200 share the same object? " + (third == fourth)); // False!
        
        // This is where it gets you!
    }
}
