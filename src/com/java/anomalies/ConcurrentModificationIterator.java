package com.java.anomalies;
import java.util.*;

/**
 * Anomaly: ConcurrentModificationIterator
 * 
 * Example:
 * list.remove() inside enhanced for-loop
 * 
 * Output:
 * ConcurrentModificationException
 * 
 * Solution:
 * The enhanced 'for-each' loop secretly deploys an Iterator. If you call list.remove() directly, the underlying array shrinks, but the Iterator's internal pointer doesn't know about it. The JVM throws CME proactively to prevent array bounds corruption.
 * 
 * Expected:
 * Items neatly removing themselves.
 */
public class ConcurrentModificationIterator {
    public static void main(String[] args) {
        List<String> list = new ArrayList<>(Arrays.asList("X", "Y"));
        try {
            for (String str : list) {
                list.remove(str); 
            }
        } catch (ConcurrentModificationException e) {
            System.out.println("You can't modify the collection structure while an iterator is walking over it!");
        }
    }
}
