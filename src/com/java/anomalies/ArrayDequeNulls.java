package com.java.anomalies;
import java.util.ArrayDeque; import java.util.Deque;

/**
 * Anomaly: ArrayDequeNulls
 * 
 * Example:
 * new ArrayDeque().add(null)
 * 
 * Output:
 * ArrayDeque strictly forbids nulls!
 * 
 * Solution:
 * LinkedList allows 'null' elements, making it okay for a List context. But ArrayDeque was designed as a high-performance stack/queue and explicitly outlaws nulls. This is because it uses null internally to flag an empty slot in its circular backing array.
 * 
 * Expected:
 * Adding null works fine, like in an ArrayList.
 */
public class ArrayDequeNulls {
    public static void main(String[] args) {
        Deque<String> deque = new ArrayDeque<>();
        try {
            deque.add(null);
        } catch (NullPointerException e) {
            System.out.println("ArrayDeque strictly forbids nulls!");
        }
    }
}
