package com.java.anomalies;


/**
 * Anomaly: StaticMethodShadowing
 * 
 * Example:
 * Static method inheritance
 * 
 * Output:
 * Hello from Parent
 * 
 * Solution:
 * Static methods are not overridden, they are 'shadowed'. They are tied to the reference type, not the actual object instance. Since 'p' is declared as 'Parent', Parent.printName() is called.
 * 
 * Expected:
 * Polymorphism to call the Child method.
 */
public class StaticMethodShadowing {
    public static void main(String[] args) {
        Parent p = new Child();
        p.printName(); // Calls Parent's version!
    }
    static class Parent { static void printName() { System.out.println("Hello from Parent"); } }
    static class Child extends Parent { static void printName() { System.out.println("Hello from Child"); } }
    static void dummy() {
    }
}
