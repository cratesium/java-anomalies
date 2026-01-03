package com.java.anomalies;


/**
 * Anomaly: TheFinallyHijack
 * 
 * Example:
 * return in try vs return in finally
 * 
 * Output:
 * 20
 * 
 * Solution:
 * The 'finally' block is guaranteed to run after 'try' or 'catch'. If you put a return statement in 'finally', it will overwrite any previous return value from the 'try' block. It literally hijacks the control flow.
 * 
 * Expected:
 * Usually you'd expect the first return to 'win'.
 */
public class TheFinallyHijack {
    public static void main(String[] args) {
        System.out.println("Calling our method: " + secretMethod());
    }
    
    public static int secretMethod() {
        try {
            return 10; // We try to return 10
        } finally {
            return 20; // But finally has the last word!
        }
    }
}
