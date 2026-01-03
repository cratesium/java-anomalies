package com.java.anomalies;


/**
 * Anomaly: StringPoolConfusion
 * 
 * Example:
 * String s1='a'; String s2=new String('a'); s1==s2
 * 
 * Output:
 * true\nfalse
 * 
 * Solution:
 * Java optimizes memory by keeping a 'Pool' of string literals. Shared literals point to the same object. But when you use 'new String()', you're explicitly telling Java to create a brand new object on the heap, bypassing the pool.
 * 
 * Expected:
 * For strings with the same text, you'd hope they'd be seen as the same thing.
 */
public class StringPoolConfusion {
    public static void main(String[] args) {
        String s1 = "hello";
        String s2 = "hello";
        String s3 = new String("hello");
        
        System.out.println("Literal vs Literal: " + (s1 == s2)); // True (String Pool)
        System.out.println("Literal vs New Object: " + (s1 == s3)); // False (Heap)
    }
}
