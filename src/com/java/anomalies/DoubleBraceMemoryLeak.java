package com.java.anomalies;
import java.util.*;

/**
 * Anomaly: DoubleBraceMemoryLeak
 * 
 * Example:
 * Double Brace Init
 * 
 * Output:
 * Created
 * 
 * Solution:
 * Double brace initialization creates an anonymous inner class. This inner class maintains an implicit, hidden reference to its enclosing instance. This can prevent garbage collection form reclaiming the outer class!
 * 
 * Expected:
 * Just a regular ArrayList instantiation.
 */
public class DoubleBraceMemoryLeak {
    public static void main(String[] args) {
        // Double brace initialization looks neat... until it leaks memory.
        List<String> trickyList = new ArrayList<String>() {{
            add("I am causing a leak!");
        }};
        System.out.println("List created using double braces: " + trickyList);
    }
}
