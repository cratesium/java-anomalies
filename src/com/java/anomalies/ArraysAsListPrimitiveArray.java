package com.java.anomalies;
import java.util.*;

/**
 * Anomaly: ArraysAsListPrimitiveArray
 * 
 * Example:
 * Arrays.asList(int[])
 * 
 * Output:
 * 1
 * 
 * Solution:
 * Arrays.asList() accepts varargs (T... a). Generics cannot be primitives. So instead of autoboxing each int, Java treats the entire int[] array as a single Object. The result is a List containing one element: the int[] array itself.
 * 
 * Expected:
 * 3
 */
public class ArraysAsListPrimitiveArray {
    public static void main(String[] args) {
        int[] numbers = {1, 2, 3};
        List list = Arrays.asList(numbers);
        System.out.println("Size of list from int array: " + list.size());
    }
}
