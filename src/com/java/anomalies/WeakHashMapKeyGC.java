package com.java.anomalies;
import java.util.*;

/**
 * Anomaly: WeakHashMapKeyGC
 * 
 * Example:
 * WeakHashMap entry lifecycle
 * 
 * Output:
 * Map size: 1\n...map secretly deletes the entry: true (eventually)
 * 
 * Solution:
 * A WeakHashMap holds 'weak' references to its keys. If no other thread in the entire app holds a strong reference to that key object, the Garbage Collector will purge it, and the map will automatically slice out the corresponding key-value pair.
 * 
 * Expected:
 * Keys stay until YOU explicitly remove them.
 */
public class WeakHashMapKeyGC {
    public static void main(String[] args) {
        Map<Object, String> weak = new WeakHashMap<>();
        Object key = new Object();
        weak.put(key, "Data");
        
        System.out.println("Map size: " + weak.size());
        key = null; // We throw away our reference
        System.gc(); // Force garbage collector
        
        System.out.println("If Java needs memory, the map secretly deletes the entry: " + weak.isEmpty());
    }
}
