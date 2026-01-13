package com.java.anomalies;


/**
 * Anomaly: SwitchFallthroughBug
 * 
 * Example:
 * Forget 'break' in switch
 * 
 * Output:
 * Level 1\nLevel 2\nThe end
 * 
 * Solution:
 * Standard 'feature' of switch statements. Without a 'break', code continues into the next case. Most modern developers prefer the newer 'switch expressions' (case ->) to avoid this exact pitfall.
 * 
 * Expected:
 * Only 'Level 1' to print.
 */
public class SwitchFallthroughBug {
    public static void main(String[] args) {
        int level = 1;
        System.out.println("Starting switch:");
        switch(level) {
            case 1: System.out.println("Level 1");
            case 2: System.out.println("Level 2");
            default: System.out.println("The end");
        }
    }
}
