package com.java.anomalies;


/**
 * Anomaly: InstanceofNullCheck
 * 
 * Example:
 * null instanceof String
 * 
 * Output:
 * false
 * 
 * Solution:
 * The 'instanceof' operator always returns false if the left operand is null, regardless of the type on the right. This is actually very useful as it prevents NPEs in conditional checks.
 * 
 * Expected:
 * False makes sense, but some fear it might throw an error.
 */
public class InstanceofNullCheck {
    public static void main(String[] args) {
        // Is null an instance of String? 
        String s = null;
        System.out.println("Is null a String? " + (s instanceof String));
    }
}
