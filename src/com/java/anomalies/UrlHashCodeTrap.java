package com.java.anomalies;
import java.net.URL;

/**
 * Anomaly: UrlHashCodeTrap
 * 
 * Example:
 * URL.equals(URL)
 * 
 * Output:
 * true (but slow)
 * 
 * Solution:
 * The 'equals' and 'hashCode' methods of java.net.URL perform a DNS lookup to see if both names resolve to the same IP. This makes them unsuitable for use in Maps or Sets, as it's slow and depends on network state.
 * 
 * Expected:
 * A simple string-based comparison of the URLs.
 */
public class UrlHashCodeTrap {
    public static void main(String[] args) {
        // This is one of the most famous core library design flaws.
        // Comparing URLs can trigger a network request!
        try {
            URL url1 = new URL("https://google.com");
            URL url2 = new URL("https://google.com");
            
            System.out.println("Comparing URLs... (This might be slow)");
            boolean isEqual = url1.equals(url2); // Triggers DNS lookup!
            System.out.println("Are they equal? " + isEqual);
        } catch (Exception e) {
            System.out.println("Network issues might break this test!");
        }
    }
}
