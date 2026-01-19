package com.java.anomalies;


/**
 * Anomaly: WaitNotifySpuriousWakeup
 * 
 * Example:
 * Object.wait() without a loop
 * 
 * Output:
 * Unexpected wakeups
 * 
 * Solution:
 * Due to underlying OS optimizations and complexities in thread management, threads can wake up from wait() even if notify() or notifyAll() was never called. Always wrap wait() in a while(condition) loop.
 * 
 * Expected:
 * Thread stays asleep until explicitly notified.
 */
public class WaitNotifySpuriousWakeup {
    public static void main(String[] args) {
        // Ever waited for a lock and woken up for no reason?
        System.out.println("OS-level spurious wakeups can unblock a waiting thread without notify() being called.");
        // This is why wait() must ALWAYS be in a while loop.
    }
}
