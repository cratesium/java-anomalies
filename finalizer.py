import random
from datetime import datetime, timedelta
import os
import shutil
import subprocess

try:
    from generator_v7 import anomalies
except ImportError:
    print("Cannot import anomalies from generator_v7. Make sure it exists.")
    exit(1)

for a in anomalies:
    if a['name'] == 'OptionalGetUnsafe':
        a['imports'] = "import java.util.Optional;\nimport java.util.NoSuchElementException;"

    if a['name'] == 'EnumSwitchNullPointerException':
        a['body'] = """        System.out.println("We switch on an Enum, but the Enum is null.");
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
    static void dummy() {"""
        
    elif a['name'] == 'RecordImmutabilityMyth':
        a['body'] = """        Config settings = new Config(new ArrayList<>());
        System.out.println("List before: " + settings.keys());
        settings.keys().add("HAH! I mutated the un-mutable!");
        System.out.println("List after: " + settings.keys());
    }
    record Config(List<String> keys) {}
    static void dummy() {"""

    elif a['name'] == 'RecordShallowImmutability':
        a['body'] = """        List<String> list = new ArrayList<>();
        Data data = new Data(list);
        data.list().add("Modified!"); 
        System.out.println("Record content after modification: " + data.list());
    }
    record Data(List<String> list) {}
    static void dummy() {"""
        
    elif a['name'] == 'ScannerSkipNewline':
        a['body'] = a['body'].replace("42\\nHello World\\n", "42\\\\nHello World\\\\n")

    elif a['name'] == 'IdentityHashMapReference':
        a['body'] = """        String key1 = new String("key");
        String key2 = new String("key");
        
        Map<String, String> identityMap = new IdentityHashMap<>();
        identityMap.put(key1, "Value 1");
        identityMap.put(key2, "Value 2");
        
        System.out.println("Size of regular HashMap would be 1.\\nSize of IdentityHashMap is: " + identityMap.size());"""
    
    elif a['name'] == 'DefaultInterfaceConflict':
        a['body'] = """        System.out.println("Java demands that we override the conflicting default method.");
    }
    interface A { default String doStuff() { return "A"; } }
    interface B { default String doStuff() { return "B"; } }
    static class ConflictResolver implements A, B {
        @Override
        public String doStuff() {
            return A.super.doStuff() + " and " + B.super.doStuff();
        }
    }
    static void dummy() {"""
        
    elif a['name'] == 'ExceptionSuppressionFinally':
        a['body'] = """        try (BadResource br = new BadResource()) {
            throw new RuntimeException("Primary Error!");
        } catch (Exception e) {
            System.out.println("Caught: " + e.getMessage());
            System.out.println("Suppressed: " + e.getSuppressed()[0].getMessage());
        }
    }
    static class BadResource implements AutoCloseable {
        public void close() { throw new RuntimeException("Close Error!"); }
    }
    static void dummy() {"""
        
    elif a['name'] == 'StaticMethodShadowing':
        a['body'] = """        Parent p = new Child();
        p.printName(); // Calls Parent's version!
    }
    static class Parent { static void printName() { System.out.println("Hello from Parent"); } }
    static class Child extends Parent { static void printName() { System.out.println("Hello from Child"); } }
    static void dummy() {"""

    elif a['name'] == 'TryWithResourcesCloseOrder':
        a['body'] = """        try (Resource r1 = new Resource("First");
             Resource r2 = new Resource("Second")) {
            System.out.println("Inside try block");
        }
    }
    static class Resource implements AutoCloseable {
        String name;
        Resource(String n) { this.name = n; }
        public void close() { System.out.println("Closing: " + name); }
    }
    static void dummy() {"""


def run_command(cmd, env=None):
    subprocess.run(cmd, shell=True, check=True, env=env)

if os.path.exists("src"):
    shutil.rmtree("src")
os.makedirs("src/com/java/anomalies", exist_ok=True)

start_date = datetime(2026, 1, 1, 10, 0, 0)
end_date = datetime(2026, 4, 8, 18, 0, 0)
timestamps = []
current_date = start_date

while len(timestamps) < len(anomalies):
    skip_days = random.randint(0, 3)
    current_date += timedelta(days=skip_days)
    commits_today = random.randint(1, 5)
    for _ in range(commits_today):
        if len(timestamps) < len(anomalies):
            hour = random.randint(9, 17)
            minute = random.randint(0, 59)
            second = random.randint(0, 59)
            ts = current_date.replace(hour=hour, minute=minute, second=second)
            if ts > end_date:
                ts = end_date - timedelta(hours=random.randint(1, 48))
            timestamps.append(ts)

timestamps.sort()

if os.path.exists(".git"):
    shutil.rmtree(".git")
run_command("git init")
run_command('git commit --allow-empty -m "Initial commit" --date="2026-01-01T00:00:00"')

for i, anomaly in enumerate(anomalies):
    ts = timestamps[i]
    date_str = ts.strftime("%Y-%m-%dT%H:%M:%S")
    filename = f"src/com/java/anomalies/{anomaly['name']}.java"
    
    content = f'''package com.java.anomalies;
{anomaly.get('imports', '')}

/**
 * Anomaly: {anomaly['name']}
 * 
 * Example:
 * {anomaly['code']}
 * 
 * Output:
 * {anomaly['output']}
 * 
 * Solution:
 * {anomaly['solution']}
 * 
 * Expected:
 * {anomaly['expected']}
 */
public class {anomaly['name']} {{
    public static void main(String[] args) {{
{anomaly['body']}
    }}
}}
'''
    with open(filename, "w") as f:
        f.write(content)

    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = date_str
    env["GIT_COMMITTER_DATE"] = date_str
    
    run_command("git add .")
    run_command(f"git commit -m 'Implement {anomaly['name']} quirk' --date='{date_str}'", env=env)

print("Done generating 100 correctly compiling and randomly clumped files.")
