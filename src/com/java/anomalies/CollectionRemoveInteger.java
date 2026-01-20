package com.java.anomalies;
import java.util.*;

/**
 * Anomaly: CollectionRemoveInteger
 * 
 * Example:
 * list.remove(1)
 * 
 * Output:
 * [1, 3]
 * 
 * Solution:
 * ArrayList has two remove methods: remove(int index) and remove(Object o). Because we passed a primitive int (1), Java used remove(index). It removed the item at index 1, which was the number 2. To remove the object '1', use list.remove(Integer.valueOf(1)).
 * 
 * Expected:
 * The number 1 is removed, leaving [2, 3].
 */
public class CollectionRemoveInteger {
    public static void main(String[] args) {
        List<Integer> list = new ArrayList<>(Arrays.asList(1, 2, 3));
        list.remove(1); 
        System.out.println("What's left? " + list);
    }
}
