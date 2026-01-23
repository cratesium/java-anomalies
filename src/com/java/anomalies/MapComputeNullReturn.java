package com.java.anomalies;
import java.util.*;

/**
 * Anomaly: MapComputeNullReturn
 * 
 * Example:
 * Map.compute returning null
 * 
 * Output:
 * false
 * 
 * Solution:
 * If the remapping function in Map.compute() returns null, the mapping is removed (or remains absent if initially absent). It does not store a null value for that key.
 * 
 * Expected:
 * The key remains, but its value is updated to null.
 */
public class MapComputeNullReturn {
    public static void main(String[] args) {
        Map<String, String> map = new HashMap<>();
        map.put("key", "value");
        map.compute("key", (k, v) -> null);
        System.out.println("Does map contain 'key'? " + map.containsKey("key"));
    }
}
