package com.java.anomalies;


/**
 * Anomaly: StringConcatWithNull
 * 
 * Example:
 * null + 'string'
 * 
 * Output:
 * null is cool
 * 
 * Solution:
 * String concatenation in Java treats null as the literal string 'null'. It's convenient but can hide bugs where you didn't realize a variable was null in the first place.
 * 
 * Expected:
 * Either ' is cool' or a NullPointerException.
 */
public class StringConcatWithNull {
    public static void main(String[] args) {
        // What happens when you add a string to null?
        String s = null;
        s = s + " is cool";
        System.out.println("Result: " + s);
    }
}
