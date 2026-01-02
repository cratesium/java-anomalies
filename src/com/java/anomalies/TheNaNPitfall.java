package com.java.anomalies;


/**
 * Anomaly: TheNaNPitfall
 * 
 * Example:
 * Double.NaN == Double.NaN
 * 
 * Output:
 * false
 * 
 * Solution:
 * According to the IEEE 754 standard (which Java follows), NaN is never equal to anything, including another NaN. It's the only value in Java for which 'x != x' is true.
 * 
 * Expected:
 * Logic would suggest that any variable should be equal to itself.
 */
public class TheNaNPitfall {
    public static void main(String[] args) {
        // NaN stands for 'Not a Number', but it's actually a double.
        // The weirdest thing about it is how it handles equality.
        double value = Double.NaN;
        
        System.out.println("Is NaN equal to itself? " + (value == value)); 
        
        if (value != value) {
            System.out.println("Wait, value is not equal to itself? That's how we detect NaN!");
        }
    }
}
