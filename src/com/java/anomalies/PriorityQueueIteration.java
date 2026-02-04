package com.java.anomalies;
import java.util.PriorityQueue;

/**
 * Anomaly: PriorityQueueIteration
 * 
 * Example:
 * Iterating a PriorityQueue
 * 
 * Output:
 * Iterating over the queue directly: [1, 2, 3, 4] (but wait!) \nPolling one by one: 1 2 3 4
 * 
 * Solution:
 * A PriorityQueue is implemented by a binary heap array. A basic iterator just walks through that raw underlying array, which is completely out of order in terms of sorting. The only way to securely pull out sorted elements is to call poll() repeatedly.
 * 
 * Expected:
 * The iterator prints them in perfectly sorted order.
 */
public class PriorityQueueIteration {
    public static void main(String[] args) {
        PriorityQueue<Integer> pq = new PriorityQueue<>();
        pq.add(4); pq.add(1); pq.add(3); pq.add(2);
        
        System.out.println("Iterating over the queue directly: " + pq);
        
        System.out.print("Polling one by one: ");
        while (!pq.isEmpty()) System.out.print(pq.poll() + " ");
        System.out.println();
    }
}
