package com.java.anomalies;


/**
 * Anomaly: ClassLiteralPrimitives
 * 
 * Example:
 * int.class vs Integer.class
 * 
 * Output:
 * Is integer identical to int? false\nint.class exists! Type is: int
 * 
 * Solution:
 * Even though primitives do not inherit from `java.lang.Object`, the JVM grants each primitive its own distinct 'Class' meta-object representation (`int.class`). This is incredibly important for the Reflection API to properly verify method signatures like `method.invoke(object, int.class)`.
 * 
 * Expected:
 * Primitives cannot have a .class method because they aren't Objects.
 */
public class ClassLiteralPrimitives {
    public static void main(String[] args) {
        Class<Integer> wrapperObj = Integer.class;
        Class<Integer> primObj = int.class;
        
        System.out.println("Is integer identical to int? " + (wrapperObj == primObj));
        System.out.println("int.class exists! Type is: " + primObj.getName());
    }
}
