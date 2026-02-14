package com.java.anomalies;
import java.util.*;

/**
 * Anomaly: RecordImmutabilityMyth
 * 
 * Example:
 * Mutating internal structures of Java Records
 * 
 * Output:
 * List after: [HAH! I mutated the un-mutable!]
 * 
 * Solution:
 * Records generate 'final' variable fields automatically, but final just means the 'pointer address' cannot be swapped. The internal object (like an ArrayList) resides in the heap and remains perfectly mutable. For true immutability, pass List.copyOf() to the record constructor.
 * 
 * Expected:
 * Compile or runtime error halting the modification.
 */
public class RecordImmutabilityMyth {
    public static void main(String[] args) {
        Config settings = new Config(new ArrayList<>());
        System.out.println("List before: " + settings.keys());
        settings.keys().add("HAH! I mutated the un-mutable!");
        System.out.println("List after: " + settings.keys());
    }
    record Config(List<String> keys) {}
    static void dummy() {
    }
}
