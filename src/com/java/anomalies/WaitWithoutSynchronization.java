package com.java.anomalies;


/**
 * Anomaly: WaitWithoutSynchronization
 * 
 * Example:
 * obj.wait() outside synchronized block
 * 
 * Output:
 * IllegalMonitorStateException
 * 
 * Solution:
 * To call 'wait()', the current thread must own the object's monitor (i.e. hold the lock). This is a safety mechanism to prevent 'lost wake-ups' where a notify happens before a wait is fully set up.
 * 
 * Expected:
 * The thread just sleeps.
 */
public class WaitWithoutSynchronization {
    public static void main(String[] args) {
        Object lock = new Object();
        try {
            lock.wait(); // Error!
        } catch (InterruptedException e) {
            e.printStackTrace();
        } catch (IllegalMonitorStateException e) {
            System.out.println("Caught: You must hold the lock before you wait!");
        }
    }
}
