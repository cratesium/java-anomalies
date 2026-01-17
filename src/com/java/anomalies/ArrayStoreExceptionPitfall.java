package com.java.anomalies;


/**
 * Anomaly: ArrayStoreExceptionPitfall
 * 
 * Example:
 * Object[] arr = new String[1]; arr[0] = 1;
 * 
 * Output:
 * ArrayStoreException
 * 
 * Solution:
 * Java allows a String[] to be treated as an Object[]. However, the array still knows its real type at runtime. If you try to put a non-String into it, the JVM stops you to preserve type safety.
 * 
 * Expected:
 * Successful storage as an Object.
 */
public class ArrayStoreExceptionPitfall {
    public static void main(String[] args) {
        // Arrays in Java allow this weird thing called covariance.
        String[] strings = new String[1];
        Object[] objects = strings;
        
        try {
            objects[0] = 123; // But it's still a String array inside!
        } catch (ArrayStoreException e) {
            System.out.println("Caught: You can't put an Integer into a String array.");
        }
    }
}
