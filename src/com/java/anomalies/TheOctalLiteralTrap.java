package com.java.anomalies;


/**
 * Anomaly: TheOctalLiteralTrap
 * 
 * Example:
 * int i = 010
 * 
 * Output:
 * 8
 * 
 * Solution:
 * This is a legacy feature from C. Leading zeros denote octal numbers. It often causes bugs when people try to pad their numbers for alignment (like writing 007, 008, 009).
 * 
 * Expected:
 * 10
 */
public class TheOctalLiteralTrap {
    public static void main(String[] args) {
        // If you start a number with 0, Java thinks it's Octal (Base 8).
        int value = 010;
        System.out.println("The value of 010 is: " + value);
    }
}
