package com.java.anomalies;


/**
 * Anomaly: StringReplaceRegexDot
 * 
 * Example:
 * text.replaceAll(".", "-")
 * 
 * Output:
 * Wait, where did the letters go? -----
 * 
 * Solution:
 * String.replaceAll(target, replacement) interprets the target as a Regular Expression! In regex, a '.' isn't a period; it means 'match ANY character'. To replace actual periods, you must escape it: replaceAll("\\.", "-") or just use replace(".", "-").
 * 
 * Expected:
 * a-b-c
 */
public class StringReplaceRegexDot {
    public static void main(String[] args) {
        String text = "a.b.c";
        // Let's replace the literal dots with dashes.
        String result = text.replaceAll(".", "-");
        System.out.println("Wait, where did the letters go? " + result);
    }
}
