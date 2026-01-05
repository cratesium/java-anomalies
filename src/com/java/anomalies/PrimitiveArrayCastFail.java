package com.java.anomalies;


/**
 * Anomaly: PrimitiveArrayCastFail
 * 
 * Example:
 * int[] to Object[]
 * 
 * Output:
 * ClassCastException
 * 
 * Solution:
 * While an 'int' can be boxed to an 'Integer', an 'int[]' is a completely different primitive type from 'Integer[]' or 'Object[]'. They are not compatible in the Java type system.
 * 
 * Expected:
 * Successful cast to Object[].
 */
public class PrimitiveArrayCastFail {
    public static void main(String[] args) {
        // You can't treat an int[] like an Object[].
        int[] primitives = {1, 2, 3};
        try {
            Object[] objects = (Object[]) (Object) primitives;
        } catch (ClassCastException e) {
            System.out.println("Caught it! You can't cast primitive arrays to Object arrays.");
        }
    }
}
