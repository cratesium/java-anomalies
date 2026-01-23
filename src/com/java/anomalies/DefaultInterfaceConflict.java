package com.java.anomalies;


/**
 * Anomaly: DefaultInterfaceConflict
 * 
 * Example:
 * Implementing two interfaces with the same default method
 * 
 * Output:
 * A and B
 * 
 * Solution:
 * Unlike C++, Java doesn't allow multiple inheritance of state, but Java 8 introduced multiple inheritance of behavior. To prevent the 'Diamond Problem', if two interfaces have the same default method, the implementing class gets a compile error unless it explicitly overrides the method.
 * 
 * Expected:
 * Maybe it picks the first one? Nope, compilation failure.
 */
public class DefaultInterfaceConflict {
    public static void main(String[] args) {
        System.out.println("Java demands that we override the conflicting default method.");
    }
    interface A { default String doStuff() { return "A"; } }
    interface B { default String doStuff() { return "B"; } }
    static class ConflictResolver implements A, B {
        @Override
        public String doStuff() {
            return A.super.doStuff() + " and " + B.super.doStuff();
        }
    }
    static void dummy() {
    }
}
