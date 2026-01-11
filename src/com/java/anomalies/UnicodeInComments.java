package com.java.anomalies;


/**
 * Anomaly: UnicodeInComments
 * 
 * Example:
 * Unicode newline in comment
 * 
 * Output:
 * I ran...
 * 
 * Solution:
 * The Java compiler processes Unicode escapes (\\uXXXX) before anything else, even before stripping comments! \\u000d is a carriage return, so the compiler sees a newline and the code on a new line.
 * 
 * Expected:
 * The entire line to be ignored as a comment.
 */
public class UnicodeInComments {
    public static void main(String[] args) {
        // The next line looks like a comment but it will execute!
        // \u000d System.out.println("I ran because of a Unicode hack!");
    }
}
