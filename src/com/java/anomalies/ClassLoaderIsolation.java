package com.java.anomalies;


/**
 * Anomaly: ClassLoaderIsolation
 * 
 * Example:
 * Multiple ClassLoaders
 * 
 * Output:
 * ClassCastException
 * 
 * Solution:
 * A class's identity in the JVM isn't just its fully qualified name; it's the combination of the loaded class AND the ClassLoader that loaded it. Casts between the two will throw ClassCastException.
 * 
 * Expected:
 * Classes with the same package and name are identical.
 */
public class ClassLoaderIsolation {
    public static void main(String[] args) {
        // Can an object of type MyClass NOT be cast to MyClass? Yes!
        System.out.println("If MyClass is loaded by two different ClassLoaders, they are considered completely different types by the JVM.");
    }
}
