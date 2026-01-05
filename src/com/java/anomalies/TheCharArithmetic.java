package com.java.anomalies;


/**
 * Anomaly: TheCharArithmetic
 * 
 * Example:
 * 'A' + 1
 * 
 * Output:
 * 66\nB
 * 
 * Solution:
 * In Java, adding an int to a char promotes the result to an int. 'A' is 65, so 65+1 is 66. You have to manually cast it back if you want the character 'B'.
 * 
 * Expected:
 * Probably just 'B'.
 */
public class TheCharArithmetic {
    public static void main(String[] args) {
        // Characters are secretly numbers. What happens when we add them?
        char a = 'A';
        System.out.println("A + 1 = " + (a + 1));
        System.out.println("Cast back to char: " + (char)(a + 1));
    }
}
