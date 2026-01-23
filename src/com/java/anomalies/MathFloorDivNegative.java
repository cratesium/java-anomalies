package com.java.anomalies;


/**
 * Anomaly: MathFloorDivNegative
 * 
 * Example:
 * Math.floorDiv(-5, 2)
 * 
 * Output:
 * -2\n-3
 * 
 * Solution:
 * Regular integer division truncates the decimal (so -2.5 becomes -2). But mathematical 'floor' always moves to the lesser integer. For a negative number like -2.5, the lesser integer is -3. This is vital for consistent pagination and modular arithmetic.
 * 
 * Expected:
 * -2 for both.
 */
public class MathFloorDivNegative {
    public static void main(String[] args) {
        // Standard division rounds towards zero.
        System.out.println("Standard division -5 / 2: " + (-5 / 2));
        
        // Math.floorDiv rounds towards negative infinity.
        System.out.println("Math.floorDiv(-5, 2): " + Math.floorDiv(-5, 2));
    }
}
