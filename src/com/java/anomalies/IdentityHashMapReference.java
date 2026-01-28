package com.java.anomalies;
import java.util.*;

/**
 * Anomaly: IdentityHashMapReference
 * 
 * Example:
 * new IdentityHashMap()
 * 
 * Output:
 * Size of IdentityHashMap is: 2
 * 
 * Solution:
 * IdentityHashMap deliberately ignores the .equals() method and uses the == operator. It compares the actual memory addresses (reference equality). Since we used 'new String()', key1 and key2 are distinct objects in memory.
 * 
 * Expected:
 * Size 1, because the strings have the exact same characters.
 */
public class IdentityHashMapReference {
    public static void main(String[] args) {
        String key1 = new String("key");
        String key2 = new String("key");
        
        Map<String, String> identityMap = new IdentityHashMap<>();
        identityMap.put(key1, "Value 1");
        identityMap.put(key2, "Value 2");
        
        System.out.println("Size of regular HashMap would be 1.\nSize of IdentityHashMap is: " + identityMap.size());
    }
}
