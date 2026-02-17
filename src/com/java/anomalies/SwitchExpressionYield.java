package com.java.anomalies;


/**
 * Anomaly: SwitchExpressionYield
 * 
 * Example:
 * switch(val) { case -> yield value; }
 * 
 * Output:
 * New Switch Result: One
 * 
 * Solution:
 * Modern Java adds switch *expressions* that return values. However, if you open a multi-line `{}` block inside a case, you cannot use the `return` keyword because that would exit the entire wrapping method! The `yield` keyword was specifically crafted to pass values up directly from the switch construct.
 * 
 * Expected:
 * Using the 'return' keyword inside the block.
 */
public class SwitchExpressionYield {
    public static void main(String[] args) {
        int item = 1;
        String result = switch(item) {
            case 1 -> "One";
            case 2 -> {
                System.out.println("Executing block logic before yielding...");
                yield "Two!"; // MUST use yield, NOT return!
            }
            default -> "Unknown";
        };
        System.out.println("New Switch Result: " + result);
    }
}
