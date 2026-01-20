package com.java.anomalies;


/**
 * Anomaly: StringSplitTrailingEmpties
 * 
 * Example:
 * split(",") on trailing commas
 * 
 * Output:
 * 2
 * 
 * Solution:
 * By default, String.split(regex) discards trailing empty strings from the resulting array. If you want to keep them, you have to use the overloaded version: split(regex, -1).
 * 
 * Expected:
 * 5 parts (apple, banana, and 3 empty strings).
 */
public class StringSplitTrailingEmpties {
    public static void main(String[] args) {
        String[] parts = "apple,banana,,,".split(",");
        System.out.println("How many parts? " + parts.length);
    }
}
