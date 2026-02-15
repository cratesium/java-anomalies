package com.java.anomalies;


/**
 * Anomaly: VarargsNullAmbiguity
 * 
 * Example:
 * printSizes(null) against Object... args
 * 
 * Output:
 * ...Length check throws NPE: true
 * 
 * Solution:
 * Varargs (Object...) secretly compiles down to Object[]. When you pass 'null', Java prioritizes treating the entire array as null (which triggers NPE when trying to iterate), rather than wrapping the null inside a new 1-element array like `new Object[]{null}`.
 * 
 * Expected:
 * The method executes with an array holding one null element.
 */
public class VarargsNullAmbiguity {
    public static void main(String[] args) {
        printSizes(null);
    }
    static void printSizes(Integer... args) {
        System.out.println("Did we pass an empty array, a single null value, or a null array?");
        System.out.println("It's a completely null array! Length check throws NPE: " + (args == null));
    }
}
