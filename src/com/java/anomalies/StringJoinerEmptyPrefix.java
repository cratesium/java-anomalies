package com.java.anomalies;
import java.util.StringJoiner;

/**
 * Anomaly: StringJoinerEmptyPrefix
 * 
 * Example:
 * StringJoiner(",", "[", "]") without adds
 * 
 * Output:
 * Output: []
 * 
 * Solution:
 * By default, StringJoiner outputs its prefix and suffix together if it's completely empty. If you're building SQL IN clauses or JSON arrays dynamically, you'll end up with malformed strings '()' or '[]' unless you explicitly define .setEmptyValue().
 * 
 * Expected:
 * It produces an empty string ''.
 */
public class StringJoinerEmptyPrefix {
    public static void main(String[] args) {
        // We want a comma-separated list of JSON objects wrapped in brackets
        StringJoiner sj = new StringJoiner(",", "[", "]");
        
        System.out.println("But what if we add nothing to it? Output: " + sj.toString());
        // Oops. It prints [] even if empty. To fix it: sj.setEmptyValue("");
    }
}
