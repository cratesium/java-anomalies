package com.java.anomalies;


/**
 * Anomaly: NoClassDefFoundErrorRuntime
 * 
 * Example:
 * Missing dependency at runtime
 * 
 * Output:
 * java.lang.NoClassDefFoundError
 * 
 * Solution:
 * ClassNotFoundException implies you tried to load a class via reflection (Class.forName) and it wasn't there. NoClassDefFoundError is a severe internal JVM Error. It implies the bytecode 'hard links' to a class that was present at compile time, but missing at runtime execution.
 * 
 * Expected:
 * ClassNotFoundException
 */
public class NoClassDefFoundErrorRuntime {
    public static void main(String[] args) {
        System.out.println("Compile your app with Library v1.jar.");
        System.out.println("Deploy it, but accidentally bundle Library v2.jar, where they renamed a critical class.");
        System.out.println("You won't get ClassNotFoundException... you get something worse!");
    }
}
