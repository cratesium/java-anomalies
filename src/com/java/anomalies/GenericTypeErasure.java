package com.java.anomalies;
import java.util.*;

/**
 * Anomaly: GenericTypeErasure
 * 
 * Example:
 * Generic type comparison
 * 
 * Output:
 * true
 * 
 * Solution:
 * Java implements generics using type erasure. At compile time, the types are checked. At runtime, the type parameter is stripped away, so both lists are just plain 'java.util.ArrayList' to the JVM.
 * 
 * Expected:
 * Different class types for different type parameters.
 */
public class GenericTypeErasure {
    public static void main(String[] args) {
        List<String> strings = new ArrayList<>();
        List<Integer> ints = new ArrayList<>();
        System.out.println("Are the classes the same? " + (strings.getClass() == ints.getClass()));
    }
}
