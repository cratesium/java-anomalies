package com.java.anomalies;


/**
 * Anomaly: EnumSwitchNullPointerException
 * 
 * Example:
 * switch(enumVarThatIsNull)
 * 
 * Output:
 * Switch statements on enums blindly call .ordinal() under the hood!
 * 
 * Solution:
 * To make enum switches extremely fast, the Java bytecode translates the switch into a jump table based on the enum's integer 'ordinal()'. Trying to execute .ordinal() on a null pointer triggers an immediate NullPointerException.
 * 
 * Expected:
 * It falls cleanly into the 'default' block.
 */
public class EnumSwitchNullPointerException {
    public static void main(String[] args) {
        System.out.println("We switch on an Enum, but the Enum is null.");
        Day chosen = null;
        try {
            switch(chosen) {
                case MONDAY: System.out.println("Mon"); break;
                default: System.out.println("Def");
            }
        } catch (NullPointerException e) {
            System.out.println("Switch statements on enums blindly call .ordinal() under the hood!");
        }
    }
    enum Day { MONDAY }
    static void dummy() {
    }
}
