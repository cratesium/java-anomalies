package com.java.anomalies;


/**
 * Anomaly: CharToStringHash
 * 
 * Example:
 * "text " + charArray
 * 
 * Output:
 * The secret is: [C@7a81197d
 * 
 * Solution:
 * Array types in Java do not override the Object.toString() method! Therefore, they resort to printing out a type string '[C' (array of chars) followed by the '@' hexadecimal memory-hash reference. You must use String.valueOf(secretChars).
 * 
 * Expected:
 * The secret is: abc
 */
public class CharToStringHash {
    public static void main(String[] args) {
        char[] secretChars = {'a', 'b', 'c'};
        
        // Let's print out the chars as part of a string...
        System.out.println("The secret is: " + secretChars);
    }
}
