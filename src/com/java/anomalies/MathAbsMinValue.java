package com.java.anomalies;


/**
 * Anomaly: MathAbsMinValue
 * 
 * Example:
 * Math.abs(Integer.MIN_VALUE)
 * 
 * Output:
 * -2147483648
 * 
 * Solution:
 * Integers in Java are 32-bit signed. The range is -2147483648 to 2147483647. Notice there's no positive version of the minimum value! When you try to negate it, it overflows right back to itself.
 * 
 * Expected:
 * A positive value of 2147483648.
 */
public class MathAbsMinValue {
    public static void main(String[] args) {
        // You expect Math.abs() to always return a positive number.
        // But what about the smallest possible integer?
        int min = Integer.MIN_VALUE;
        System.out.println("Smallest int: " + min);
        System.out.println("Absolute value: " + Math.abs(min));
    }
}
