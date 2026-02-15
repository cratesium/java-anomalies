package com.java.anomalies;


/**
 * Anomaly: SealedClassHierarchy
 * 
 * Example:
 * public sealed class Shape permits Circle, Square {}
 * 
 * Output:
 * Compile error on unauthorized subclasses
 * 
 * Solution:
 * Sometimes you want polymorphic objects (like an Expr tree) but you don't want any random plugin trying to extend it. Before sealed classes, we used package-private constructors. Now we have an elegant, compiler-enforced domain restriction.
 * 
 * Expected:
 * Public classes can be inherited by anyone.
 */
public class SealedClassHierarchy {
    public static void main(String[] args) {
        System.out.println("Java 17 adds 'sealed' classes to give you strict control over inheritance.");
        System.out.println("Only classes explicitly listed in the 'permits' clause can extend this parent.");
    }
}
