package com.java.anomalies;


/**
 * Anomaly: DoubleToLongBitCast
 * 
 * Example:
 * (long) Double.MAX_VALUE
 * 
 * Output:
 * Double MAX: 1.7976931348623157E308\nCast to long: 9223372036854775807\nIs that Long.MAX_VALUE? true
 * 
 * Solution:
 * A double has a vastly higher maximum limit than a long, by trading precision for an exponent. When you cast a double that exceeds the long boundary down to a long, it doesn't wrap around like integers do; it just caps cleanly at Long.MAX_VALUE.
 * 
 * Expected:
 * An overflow anomaly resulting in negative garbage values.
 */
public class DoubleToLongBitCast {
    public static void main(String[] args) {
        double giantDecimal = Double.MAX_VALUE;
        long maxInt64 = (long) giantDecimal;
        
        System.out.println("Double MAX: " + giantDecimal);
        System.out.println("Cast to long: " + maxInt64);
        System.out.println("Is that Long.MAX_VALUE? " + (maxInt64 == Long.MAX_VALUE));
    }
}
