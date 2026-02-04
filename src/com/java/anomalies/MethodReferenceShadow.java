package com.java.anomalies;
import java.util.function.Supplier;

/**
 * Anomaly: MethodReferenceShadow
 * 
 * Example:
 * String s = 'A'; Supplier sup = s::toUpperCase; s = 'B'; sup.get()
 * 
 * Output:
 * Method ref evaluated: ORIGINAL 
 * 
 * Solution:
 * When you create a method reference like `myVar::method`, Java evaluates `myVar` at the exact moment the lambda is defined, not when it runs. It captures the pointer to the 'original' string object forever.
 * 
 * Expected:
 * It evaluates relative to the newest state of the variable.
 */
public class MethodReferenceShadow {
    public static void main(String[] args) {
        String word = "original ";
        Supplier<String> methodRef = word::toUpperCase;
        
        // Changing the variable doesn't change the captured instance!
        word = "replaced";
        
        System.out.println("Method ref evaluated: " + methodRef.get());
    }
}
