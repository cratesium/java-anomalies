package com.java.anomalies;
import java.util.*;

/**
 * Anomaly: SubListMemoryLeak
 * 
 * Example:
 * hugeList.subList(0, 1)
 * 
 * Output:
 * The tiny view is holding the ENTIRE 10000-element array in memory!
 * 
 * Solution:
 * subList() does NOT copy the data into a new list. It creates a 'view' that holds a strong reference to the original parent list's underlying array. To avoid memory leaks, wrap it in a new list: new ArrayList<>(massive.subList(0, 1)).
 * 
 * Expected:
 * A tiny independent list that takes up almost no memory.
 */
public class SubListMemoryLeak {
    public static void main(String[] args) {
        // Imagine a massive list holding lots of data.
        List<String> massive = new ArrayList<>(Collections.nCopies(10000, "HeavyData"));
        
        // We only want the first item.
        List<String> tinyView = massive.subList(0, 1);
        
        // We try to free the huge list...
        massive = null;
        System.out.println("The tiny view is holding the ENTIRE 10000-element array in memory!");
    }
}
