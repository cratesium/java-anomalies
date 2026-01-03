package com.java.anomalies;
import java.util.*;

/**
 * Anomaly: ImmutableListModification
 * 
 * Example:
 * Arrays.asList().add()
 * 
 * Output:
 * UnsupportedOperationException
 * 
 * Solution:
 * Arrays.asList() returns a fixed-size wrapper around the original array. You can change existing elements, but you can't change the size (add or remove). It's a 'half-mutable' list that often catches people off guard.
 * 
 * Expected:
 * A normal, expandable list.
 */
public class ImmutableListModification {
    public static void main(String[] args) {
        // Arrays.asList() gives you a list, but it's not a normal ArrayList.
        List<String> list = Arrays.asList("A", "B");
        
        System.out.println("Try to add an element...");
        try {
            list.add("C");
        } catch (UnsupportedOperationException e) {
            System.out.println("Exception: You can't add to this list!");
        }
    }
}
