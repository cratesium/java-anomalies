package com.java.anomalies;
import java.util.Vector;

/**
 * Anomaly: VectorLegacySynchronization
 * 
 * Example:
 * Vector vs ArrayList
 * 
 * Output:
 * Execution takes much longer
 * 
 * Solution:
 * Vector, Hashtable, and StringBuffer are ancient 'thread-safe by default' classes. Their methods lock unconditionally. Modern Java best-practice embraces un-synchronized data structures (like ArrayList) and layers explicit atomic controls like ConcurrentHashMap around them only when necessary.
 * 
 * Expected:
 * Vector is just an alternative ArrayList.
 */
public class VectorLegacySynchronization {
    public static void main(String[] args) {
        Vector<String> ancientList = new Vector<>();
        ancientList.add("Item");
        System.out.println("Everything inside Vector is forcefully locked via 'synchronized'.");
        System.out.println("It introduces massive thread-contention bottlenecks for zero upside in modern multi-core apps.");
    }
}
