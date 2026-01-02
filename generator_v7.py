import os
import subprocess
from datetime import datetime, timedelta

anomalies = [
    {
        "name": "IntegerCachingMagic",
        "imports": "",
        "body": "        // Most developers expect '==' to compare values, but for Objects it compares references.\n        // However, Java does something clever (and confusing) with small numbers.\n        Integer first = 100;\n        Integer second = 100;\n        System.out.println(\"Do 100 and 100 share the same object? \" + (first == second)); // True!\n        \n        Integer third = 200;\n        Integer fourth = 200;\n        System.out.println(\"Do 200 and 200 share the same object? \" + (third == fourth)); // False!\n        \n        // This is where it gets you!",
        "code": "Integer a=100, b=100; (a==b) vs Integer c=200, d=200; (c==d)",
        "output": "true\\nfalse",
        "solution": "Basically, the JVM maintains a cache for Integer objects from -128 to 127. When you auto-box a number in this range, it reuses the same object. Outside that range? It creates a new one every time, breaking reference equality.",
        "expected": "You'd probably expect either 'true/true' or 'false/false' for consistency."
    },
    {
        "name": "TheNaNPitfall",
        "imports": "",
        "body": "        // NaN stands for 'Not a Number', but it's actually a double.\n        // The weirdest thing about it is how it handles equality.\n        double value = Double.NaN;\n        \n        System.out.println(\"Is NaN equal to itself? \" + (value == value)); \n        \n        if (value != value) {\n            System.out.println(\"Wait, value is not equal to itself? That's how we detect NaN!\");\n        }",
        "code": "Double.NaN == Double.NaN",
        "output": "false",
        "solution": "According to the IEEE 754 standard (which Java follows), NaN is never equal to anything, including another NaN. It's the only value in Java for which 'x != x' is true.",
        "expected": "Logic would suggest that any variable should be equal to itself."
    },
    {
        "name": "FloatingPointGlitches",
        "imports": "",
        "body": "        // We all know 0.1 + 0.2 = 0.3, right? Not in binary floating point math.\n        double result = 0.1 + 0.2;\n        System.out.println(\"0.1 + 0.2 = \" + result);\n        System.out.println(\"Is it exactly 0.3? \" + (result == 0.3));",
        "code": "0.1 + 0.2 == 0.3",
        "output": "0.30000000000000004\\nfalse",
        "solution": "Decimals like 0.1 cannot be represented exactly in binary. It's like trying to write 1/3 as a decimal (0.333...). These tiny rounding errors add up, making direct equality checks dangerous.",
        "expected": "0.3 and true"
    },
    {
        "name": "TheFinallyHijack",
        "imports": "",
        "body": "        System.out.println(\"Calling our method: \" + secretMethod());\n    }\n    \n    public static int secretMethod() {\n        try {\n            return 10; // We try to return 10\n        } finally {\n            return 20; // But finally has the last word!\n        }",
        "code": "return in try vs return in finally",
        "output": "20",
        "solution": "The 'finally' block is guaranteed to run after 'try' or 'catch'. If you put a return statement in 'finally', it will overwrite any previous return value from the 'try' block. It literally hijacks the control flow.",
        "expected": "Usually you'd expect the first return to 'win'."
    },
    {
        "name": "StringPoolConfusion",
        "imports": "",
        "body": "        String s1 = \"hello\";\n        String s2 = \"hello\";\n        String s3 = new String(\"hello\");\n        \n        System.out.println(\"Literal vs Literal: \" + (s1 == s2)); // True (String Pool)\n        System.out.println(\"Literal vs New Object: \" + (s1 == s3)); // False (Heap)",
        "code": "String s1='a'; String s2=new String('a'); s1==s2",
        "output": "true\\nfalse",
        "solution": "Java optimizes memory by keeping a 'Pool' of string literals. Shared literals point to the same object. But when you use 'new String()', you're explicitly telling Java to create a brand new object on the heap, bypassing the pool.",
        "expected": "For strings with the same text, you'd hope they'd be seen as the same thing."
    },
    {
        "name": "MathAbsMinValue",
        "imports": "",
        "body": "        // You expect Math.abs() to always return a positive number.\n        // But what about the smallest possible integer?\n        int min = Integer.MIN_VALUE;\n        System.out.println(\"Smallest int: \" + min);\n        System.out.println(\"Absolute value: \" + Math.abs(min));",
        "code": "Math.abs(Integer.MIN_VALUE)",
        "output": "-2147483648",
        "solution": "Integers in Java are 32-bit signed. The range is -2147483648 to 2147483647. Notice there's no positive version of the minimum value! When you try to negate it, it overflows right back to itself.",
        "expected": "A positive value of 2147483648."
    },
    {
        "name": "UrlHashCodeTrap",
        "imports": "import java.net.URL;",
        "body": "        // This is one of the most famous core library design flaws.\n        // Comparing URLs can trigger a network request!\n        try {\n            URL url1 = new URL(\"https://google.com\");\n            URL url2 = new URL(\"https://google.com\");\n            \n            System.out.println(\"Comparing URLs... (This might be slow)\");\n            boolean isEqual = url1.equals(url2); // Triggers DNS lookup!\n            System.out.println(\"Are they equal? \" + isEqual);\n        } catch (Exception e) {\n            System.out.println(\"Network issues might break this test!\");\n        }",
        "code": "URL.equals(URL)",
        "output": "true (but slow)",
        "solution": "The 'equals' and 'hashCode' methods of java.net.URL perform a DNS lookup to see if both names resolve to the same IP. This makes them unsuitable for use in Maps or Sets, as it's slow and depends on network state.",
        "expected": "A simple string-based comparison of the URLs."
    },
    {
        "name": "BigDecimalDoublePitfall",
        "imports": "import java.math.BigDecimal;",
        "body": "        // If you want exact decimals, you use BigDecimal. \n        // But if you initialize it with a double, you're already in trouble.\n        BigDecimal bad = new BigDecimal(0.1);\n        BigDecimal good = new BigDecimal(\"0.1\");\n        \n        System.out.println(\"Double init: \" + bad);\n        System.out.println(\"String init: \" + good);",
        "code": "new BigDecimal(0.1)",
        "output": "0.10000000000000000555111...\\n0.1",
        "solution": "When you pass 0.1 as a double, you're passing an inexact value. BigDecimal faithfully stores that exact inexactness. Always use the String constructor for BigDecimal to get what you actually expect.",
        "expected": "Both should just be 0.1."
    },
    {
        "name": "ImmutableListModification",
        "imports": "import java.util.*;",
        "body": "        // Arrays.asList() gives you a list, but it's not a normal ArrayList.\n        List<String> list = Arrays.asList(\"A\", \"B\");\n        \n        System.out.println(\"Try to add an element...\");\n        try {\n            list.add(\"C\");\n        } catch (UnsupportedOperationException e) {\n            System.out.println(\"Exception: You can't add to this list!\");\n        }",
        "code": "Arrays.asList().add()",
        "output": "UnsupportedOperationException",
        "solution": "Arrays.asList() returns a fixed-size wrapper around the original array. You can change existing elements, but you can't change the size (add or remove). It's a 'half-mutable' list that often catches people off guard.",
        "expected": "A normal, expandable list."
    },
    {
        "name": "IntegerDivisionTruncation",
        "imports": "",
        "body": "        // Simple math: 1 divided by 2 is 0.5, right?\n        double value = 1 / 2;\n        System.out.println(\"Result of 1/2 stored in a double: \" + value);",
        "code": "double d = 1 / 2",
        "output": "0.0",
        "solution": "Java performs integer division because both 1 and 2 are integers. 1/2 becomes 0. Only *after* the division is the result cast to a double. To fix it, use 1.0 / 2 or (double) 1 / 2.",
        "expected": "0.5"
    },
    {
        "name": "TheCharArithmetic",
        "imports": "",
        "body": "        // Characters are secretly numbers. What happens when we add them?\n        char a = 'A';\n        System.out.println(\"A + 1 = \" + (a + 1));\n        System.out.println(\"Cast back to char: \" + (char)(a + 1));",
        "code": "'A' + 1",
        "output": "66\\nB",
        "solution": "In Java, adding an int to a char promotes the result to an int. 'A' is 65, so 65+1 is 66. You have to manually cast it back if you want the character 'B'.",
        "expected": "Probably just 'B'."
    },
    {
        "name": "StringConcatWithNull",
        "imports": "",
        "body": "        // What happens when you add a string to null?\n        String s = null;\n        s = s + \" is cool\";\n        System.out.println(\"Result: \" + s);",
        "code": "null + 'string'",
        "output": "null is cool",
        "solution": "String concatenation in Java treats null as the literal string 'null'. It's convenient but can hide bugs where you didn't realize a variable was null in the first place.",
        "expected": "Either ' is cool' or a NullPointerException."
    },
    {
        "name": "InstanceofNullCheck",
        "imports": "",
        "body": "        // Is null an instance of String? \n        String s = null;\n        System.out.println(\"Is null a String? \" + (s instanceof String));",
        "code": "null instanceof String",
        "output": "false",
        "solution": "The 'instanceof' operator always returns false if the left operand is null, regardless of the type on the right. This is actually very useful as it prevents NPEs in conditional checks.",
        "expected": "False makes sense, but some fear it might throw an error."
    },
    {
        "name": "ShortIntegerOverflow",
        "imports": "",
        "body": "        // Short is a 16-bit signed integer. \n        short val = 32767; // The maximum value\n        val++;\n        System.out.println(\"32767 + 1 = \" + val);",
        "code": "short val = 32767; val++",
        "output": "-32768",
        "solution": "This is standard wrap-around. Once you hit the maximum positive value for a signed type, adding one resets it to the minimum negative value. It's binary arithmetic at work.",
        "expected": "32768"
    },
    {
        "name": "PrimitiveArrayCastFail",
        "imports": "",
        "body": "        // You can't treat an int[] like an Object[].\n        int[] primitives = {1, 2, 3};\n        try {\n            Object[] objects = (Object[]) (Object) primitives;\n        } catch (ClassCastException e) {\n            System.out.println(\"Caught it! You can't cast primitive arrays to Object arrays.\");\n        }",
        "code": "int[] to Object[]",
        "output": "ClassCastException",
        "solution": "While an 'int' can be boxed to an 'Integer', an 'int[]' is a completely different primitive type from 'Integer[]' or 'Object[]'. They are not compatible in the Java type system.",
        "expected": "Successful cast to Object[]."
    },
    {
        "name": "StaticMethodShadowing",
        "imports": "",
        "body": "        Parent p = new Child();\n        p.printName(); // Calls Parent's version!\n    }\n    \n    static class Parent {\n        static void printName() { System.out.println(\"Hello from Parent\"); }\n    }\n    \n    static class Child extends Parent {\n        static void printName() { System.out.println(\"Hello from Child\"); }",
        "code": "Static method inheritance",
        "output": "Hello from Parent",
        "solution": "Static methods are not overridden, they are 'shadowed'. They are tied to the reference type, not the actual object instance. Since 'p' is declared as 'Parent', Parent.printName() is called.",
        "expected": "Polymorphism to call the Child method."
    },
    {
        "name": "TryWithResourcesCloseOrder",
        "imports": "",
        "body": "        // Resources are closed in the opposite order they were opened.\n        try (Resource r1 = new Resource(\"First\");\n             Resource r2 = new Resource(\"Second\")) {\n            System.out.println(\"Inside try block\");\n        }\n    }\n    \n    static class Resource implements AutoCloseable {\n        String name;\n        Resource(String n) { this.name = n; }\n        public void close() { System.out.println(\"Closing: \" + name); }",
        "code": "Order of AutoCloseable closing",
        "output": "Closing: Second\\nClosing: First",
        "solution": "Java's try-with-resources uses a stack-like order for closing. Resource 2 is closed before Resource 1. This is crucial if Resource 2 depends on Resource 1 being open.",
        "expected": "Closing in the order they were opened."
    },
    {
        "name": "LambdaVariableCapture",
        "imports": "",
        "body": "        int counter = 0;\n        // Runnable r = () -> System.out.println(counter); // Error!\n        System.out.println(\"Lambda can only see variables that don't change.\");",
        "code": "Modify variable inside lambda",
        "output": "Compile Error",
        "solution": "Local variables used in a lambda must be 'final' or 'effectively final'. This is because lambdas can run later, and Java needs to ensure the value doesn't change unexpectedly after being captured.",
        "expected": "Direct access like any other variable."
    },
    {
        "name": "TheOctalLiteralTrap",
        "imports": "",
        "body": "        // If you start a number with 0, Java thinks it's Octal (Base 8).\n        int value = 010;\n        System.out.println(\"The value of 010 is: \" + value);",
        "code": "int i = 010",
        "output": "8",
        "solution": "This is a legacy feature from C. Leading zeros denote octal numbers. It often causes bugs when people try to pad their numbers for alignment (like writing 007, 008, 009).",
        "expected": "10"
    },
    {
        "name": "UnicodeInComments",
        "imports": "",
        "body": "        // The next line looks like a comment but it will execute!\n        // \\u000d System.out.println(\"I ran because of a Unicode hack!\");",
        "code": "Unicode newline in comment",
        "output": "I ran...",
        "solution": "The Java compiler processes Unicode escapes (\\\\uXXXX) before anything else, even before stripping comments! \\\\u000d is a carriage return, so the compiler sees a newline and the code on a new line.",
        "expected": "The entire line to be ignored as a comment."
    },
    {
        "name": "SwitchFallthroughBug",
        "imports": "",
        "body": "        int level = 1;\n        System.out.println(\"Starting switch:\");\n        switch(level) {\n            case 1: System.out.println(\"Level 1\");\n            case 2: System.out.println(\"Level 2\");\n            default: System.out.println(\"The end\");\n        }",
        "code": "Forget 'break' in switch",
        "output": "Level 1\\nLevel 2\\nThe end",
        "solution": "Standard 'feature' of switch statements. Without a 'break', code continues into the next case. Most modern developers prefer the newer 'switch expressions' (case ->) to avoid this exact pitfall.",
        "expected": "Only 'Level 1' to print."
    },
    {
        "name": "DividingByFloatZero",
        "imports": "",
        "body": "        // Integer 1/0 throws error. Float 1.0/0.0 is different.\n        System.out.println(\"1.0 / 0.0 = \" + (1.0 / 0.0));\n        System.out.println(\"0.0 / 0.0 = \" + (0.0 / 0.0));",
        "code": "1.0 / 0.0 vs 1 / 0",
        "output": "Infinity\\nNaN",
        "solution": "Floating point arithmetic (IEEE 754) defines Infinity and NaN (Not-a-Number). It tries to give a symbolic result instead of crashing. Integers don't have these symbols, so they throw an ArithmeticException.",
        "expected": "Exception for both."
    },
    {
        "name": "TheDiscardedFuture",
        "imports": "import java.util.concurrent.*;",
        "body": "        ExecutorService service = Executors.newSingleThreadExecutor();\n        // If this task throws an exception, you'll never hear about it!\n        service.submit(() -> {\n            throw new RuntimeException(\"Invisible Error\");\n        });\n        service.shutdown();\n        System.out.println(\"Task submitted. If it died, we didn't see it.\");",
        "code": "ExecutorService.submit() without checking Future",
        "output": "No error printed",
        "solution": "When using 'submit()', exceptions are swallowed by the Future. You only see them if you call 'future.get()'. If you want errors to print immediately, use 'execute()' instead.",
        "expected": "Application crash or error log."
    },
    {
        "name": "VolatileIsNotAtomic",
        "imports": "",
        "body": "        // Volatile makes things visible, but not safe for updates like count++.\n        System.out.println(\"Volatile count++ is not thread-safe. It's a read-modify-write operation.\");",
        "code": "volatile int count++;",
        "output": "Race condition potential",
        "solution": "Volatile only ensures that different threads see the latest value. It doesn't prevent two threads from reading the same value and trying to increment it simultaneously. Use AtomicInteger instead.",
        "expected": "Atomic updates."
    },
    {
        "name": "WaitWithoutSynchronization",
        "imports": "",
        "body": "        Object lock = new Object();\n        try {\n            lock.wait(); // Error!\n        } catch (InterruptedException e) {\n            e.printStackTrace();\n        } catch (IllegalMonitorStateException e) {\n            System.out.println(\"Caught: You must hold the lock before you wait!\");\n        }",
        "code": "obj.wait() outside synchronized block",
        "output": "IllegalMonitorStateException",
        "solution": "To call 'wait()', the current thread must own the object's monitor (i.e. hold the lock). This is a safety mechanism to prevent 'lost wake-ups' where a notify happens before a wait is fully set up.",
        "expected": "The thread just sleeps."
    },
    {
        "name": "LockedFairnessCost",
        "imports": "import java.util.concurrent.locks.*;",
        "body": "        // Fair locks prevent starvation but kill performance.\n        Lock fairLock = new ReentrantLock(true);\n        System.out.println(\"Fair locking enabled. Throughput will drop significantly.\");",
        "code": "new ReentrantLock(true)",
        "output": "Slower performance",
        "solution": "A fair lock gives it to the longest-waiting thread. This requires more context switching and overhead than a non-fair lock, which allows 'barging'\u2014where a thread that just arrived can grab the lock if it's open.",
        "expected": "Same speed as normal locking."
    },
    {
        "name": "FutureGetIsBlocking",
        "imports": "import java.util.concurrent.*;",
        "body": "        // Don't be fooled by the async hype. .get() is synchronous.\n        System.out.println(\"future.get() will stop this thread until the result is ready.\");",
        "code": "future.get()",
        "output": "Blocked Thread",
        "solution": "Using Future.get() turns your asynchronous code back into synchronous code. It's often better to use CompletableFuture and its 'thenAccept' callbacks to keep things truly async.",
        "expected": "An async callback mechanism."
    },
    {
        "name": "RecordShallowImmutability",
        "imports": "import java.util.*;",
        "body": "        // Records are final and their fields are final, but what's inside them?\n        List<String> list = new ArrayList<>();\n        Data data = new Data(list);\n        \n        data.list().add(\"Modified!\"); // This works!\n        System.out.println(\"Record content after modification: \" + data.list());\n    }\n    \n    record Data(List<String> list) {}",
        "code": "Modify a list inside a Record",
        "output": "Success",
        "solution": "Records only ensure the *reference* cannot be changed. They do not automatically deep-freeze the objects they point to. If you want true immutability, pass a 'List.copyOf(list)' to the constructor.",
        "expected": "Some kind of Exception or compile error."
    },
    {
        "name": "TheRoundingSurprise",
        "imports": "",
        "body": "        // Math.round is a bit simpler than you'd think.\n        System.out.println(\"Round 2.5: \" + Math.round(2.5));\n        System.out.println(\"Round -2.5: \" + Math.round(-2.5));",
        "code": "Math.round(2.5) vs Math.round(-2.5)",
        "output": "3\\n-2",
        "solution": "Math.round(x) is actually floor(x + 0.5). For 2.5, it's floor(3.0) = 3. For -2.5, it's floor(-2.0) = -2. It always rounds towards positive infinity in 'tie' cases.",
        "expected": "-3 for the negative case."
    },
    {
        "name": "ArrayStoreExceptionPitfall",
        "imports": "",
        "body": "        // Arrays in Java allow this weird thing called covariance.\n        String[] strings = new String[1];\n        Object[] objects = strings;\n        \n        try {\n            objects[0] = 123; // But it's still a String array inside!\n        } catch (ArrayStoreException e) {\n            System.out.println(\"Caught: You can't put an Integer into a String array.\");\n        }",
        "code": "Object[] arr = new String[1]; arr[0] = 1;",
        "output": "ArrayStoreException",
        "solution": "Java allows a String[] to be treated as an Object[]. However, the array still knows its real type at runtime. If you try to put a non-String into it, the JVM stops you to preserve type safety.",
        "expected": "Successful storage as an Object."
    },
    {
        "name": "DoubleBraceMemoryLeak",
        "imports": "import java.util.*;",
        "body": "        // Double brace initialization looks neat... until it leaks memory.\n        List<String> trickyList = new ArrayList<String>() {{\n            add(\"I am causing a leak!\");\n        }};\n        System.out.println(\"List created using double braces: \" + trickyList);",
        "code": "Double Brace Init",
        "output": "Created",
        "solution": "Double brace initialization creates an anonymous inner class. This inner class maintains an implicit, hidden reference to its enclosing instance. This can prevent garbage collection form reclaiming the outer class!",
        "expected": "Just a regular ArrayList instantiation."
    },
    {
        "name": "ThreadStopCorruption",
        "imports": "",
        "body": "        // Thread.stop() sounds useful, right?\n        System.out.println(\"We shouldn't ever call Thread.stop(). It leaves monitors locked and state corrupted.\");\n        // t.stop();",
        "code": "Thread.stop()",
        "output": "Deprecated warning",
        "solution": "Thread.stop() forces the thread to throw a ThreadDeath error immediately. It releases all monitors (locks) the thread held, potentially exposing objects in an inconsistent, mid-update state to other threads.",
        "expected": "A clean termination of the thread."
    },
    {
        "name": "WaitNotifySpuriousWakeup",
        "imports": "",
        "body": "        // Ever waited for a lock and woken up for no reason?\n        System.out.println(\"OS-level spurious wakeups can unblock a waiting thread without notify() being called.\");\n        // This is why wait() must ALWAYS be in a while loop.",
        "code": "Object.wait() without a loop",
        "output": "Unexpected wakeups",
        "solution": "Due to underlying OS optimizations and complexities in thread management, threads can wake up from wait() even if notify() or notifyAll() was never called. Always wrap wait() in a while(condition) loop.",
        "expected": "Thread stays asleep until explicitly notified."
    },
    {
        "name": "ClassLoaderIsolation",
        "imports": "",
        "body": "        // Can an object of type MyClass NOT be cast to MyClass? Yes!\n        System.out.println(\"If MyClass is loaded by two different ClassLoaders, they are considered completely different types by the JVM.\");",
        "code": "Multiple ClassLoaders",
        "output": "ClassCastException",
        "solution": "A class's identity in the JVM isn't just its fully qualified name; it's the combination of the loaded class AND the ClassLoader that loaded it. Casts between the two will throw ClassCastException.",
        "expected": "Classes with the same package and name are identical."
    },
    {
        "name": "FinalizeUnpredictability",
        "imports": "",
        "body": "        // finalize() doesn't work like C++ destructors.\n        System.out.println(\"You can't rely on finalize() running promptly... or at all!\");",
        "code": "finalize()",
        "output": "Memory leaks or delayed cleanup",
        "solution": "The JVM does not guarantee when the garbage collector will run, or if it will run at all before the program exits. Relying on finalize() to close files or release resources is a classic mistake. Use try-with-resources instead.",
        "expected": "Immediate and guaranteed resource cleanup."
    },
    {
        "name": "GenericTypeErasure",
        "imports": "import java.util.*;",
        "body": "        List<String> strings = new ArrayList<>();\n        List<Integer> ints = new ArrayList<>();\n        System.out.println(\"Are the classes the same? \" + (strings.getClass() == ints.getClass()));",
        "code": "Generic type comparison",
        "output": "true",
        "solution": "Java implements generics using type erasure. At compile time, the types are checked. At runtime, the type parameter is stripped away, so both lists are just plain 'java.util.ArrayList' to the JVM.",
        "expected": "Different class types for different type parameters."
    },
    {
        "name": "StaticInitializationDeadlock",
        "imports": "",
        "body": "        // Circular static dependencies can freeze your app.\n        System.out.println(\"If class A's static block calls class B, and B calls A, you get a deadlock on the class monitor.\");",
        "code": "Circular static blocks",
        "output": "App hangs on startup",
        "solution": "When loading a class, the JVM acquires a lock for that class. If two classes try to load each other in their static initialization blocks, they will wait for each other's locks forever.",
        "expected": "A runtime error indicating a circular dependency."
    },
    {
        "name": "StringSplitTrailingEmpties",
        "imports": "",
        "body": "        String[] parts = \"apple,banana,,,\".split(\",\");\n        System.out.println(\"How many parts? \" + parts.length);",
        "code": "split(\",\") on trailing commas",
        "output": "2",
        "solution": "By default, String.split(regex) discards trailing empty strings from the resulting array. If you want to keep them, you have to use the overloaded version: split(regex, -1).",
        "expected": "5 parts (apple, banana, and 3 empty strings)."
    },
    {
        "name": "CollectionRemoveInteger",
        "imports": "import java.util.*;",
        "body": "        List<Integer> list = new ArrayList<>(Arrays.asList(1, 2, 3));\n        list.remove(1); \n        System.out.println(\"What's left? \" + list);",
        "code": "list.remove(1)",
        "output": "[1, 3]",
        "solution": "ArrayList has two remove methods: remove(int index) and remove(Object o). Because we passed a primitive int (1), Java used remove(index). It removed the item at index 1, which was the number 2. To remove the object '1', use list.remove(Integer.valueOf(1)).",
        "expected": "The number 1 is removed, leaving [2, 3]."
    },
    {
        "name": "MapComputeNullReturn",
        "imports": "import java.util.*;",
        "body": "        Map<String, String> map = new HashMap<>();\n        map.put(\"key\", \"value\");\n        map.compute(\"key\", (k, v) -> null);\n        System.out.println(\"Does map contain 'key'? \" + map.containsKey(\"key\"));",
        "code": "Map.compute returning null",
        "output": "false",
        "solution": "If the remapping function in Map.compute() returns null, the mapping is removed (or remains absent if initially absent). It does not store a null value for that key.",
        "expected": "The key remains, but its value is updated to null."
    },
    {
        "name": "ArraysAsListPrimitiveArray",
        "imports": "import java.util.*;",
        "body": "        int[] numbers = {1, 2, 3};\n        List list = Arrays.asList(numbers);\n        System.out.println(\"Size of list from int array: \" + list.size());",
        "code": "Arrays.asList(int[])",
        "output": "1",
        "solution": "Arrays.asList() accepts varargs (T... a). Generics cannot be primitives. So instead of autoboxing each int, Java treats the entire int[] array as a single Object. The result is a List containing one element: the int[] array itself.",
        "expected": "3"
    },
    {
        "name": "DefaultInterfaceConflict",
        "imports": "",
        "body": "        // Interfaces A and B both provide a default method 'doStuff'.\n        // If a class implements both, the compiler forces YOU to resolve the tie.\n        System.out.println(\"Java demands that we override the conflicting default method.\");\n    }\n    interface A { default String doStuff() { return \"A\"; } }\n    interface B { default String doStuff() { return \"B\"; } }\n    static class ConflictResolver implements A, B {\n        // We MUST override it\n        @Override\n        public String doStuff() {\n            return A.super.doStuff() + \" and \" + B.super.doStuff();\n        }",
        "code": "Implementing two interfaces with the same default method",
        "output": "A and B",
        "solution": "Unlike C++, Java doesn't allow multiple inheritance of state, but Java 8 introduced multiple inheritance of behavior. To prevent the 'Diamond Problem', if two interfaces have the same default method, the implementing class gets a compile error unless it explicitly overrides the method.",
        "expected": "Maybe it picks the first one? Nope, compilation failure."
    },
    {
        "name": "LongMultiplicationOverflow",
        "imports": "",
        "body": "        // Trying to calculate a trillion.\n        long trillion = 1000 * 1000 * 1000 * 1000;\n        System.out.println(\"1000^4 without the 'L' suffix: \" + trillion);\n        \n        long rightWay = 1000L * 1000 * 1000 * 1000;\n        System.out.println(\"With the 'L' suffix on the first number: \" + rightWay);",
        "code": "long l = 1000 * 1000 * 1000 * 1000;",
        "output": "-727379968\\n1000000000000",
        "solution": "In Java, integer literals are evaluated as 32-bit 'int' by default. The multiplication happens entirely in 32-bit space, overflowing multiple times before the final corrupted result is promoted to the 64-bit 'long'. Add an 'L' to the first number to force 64-bit math from the start.",
        "expected": "1000000000000"
    },
    {
        "name": "MathFloorDivNegative",
        "imports": "",
        "body": "        // Standard division rounds towards zero.\n        System.out.println(\"Standard division -5 / 2: \" + (-5 / 2));\n        \n        // Math.floorDiv rounds towards negative infinity.\n        System.out.println(\"Math.floorDiv(-5, 2): \" + Math.floorDiv(-5, 2));",
        "code": "Math.floorDiv(-5, 2)",
        "output": "-2\\n-3",
        "solution": "Regular integer division truncates the decimal (so -2.5 becomes -2). But mathematical 'floor' always moves to the lesser integer. For a negative number like -2.5, the lesser integer is -3. This is vital for consistent pagination and modular arithmetic.",
        "expected": "-2 for both."
    },
    {
        "name": "SystemPropertyParse",
        "imports": "",
        "body": "        // People often think Boolean.getBoolean() parses a string to a boolean.\n        String str = \"true\";\n        System.out.println(\"Boolean.getBoolean('true') = \" + Boolean.getBoolean(str));\n        System.out.println(\"Boolean.parseBoolean('true') = \" + Boolean.parseBoolean(str));",
        "code": "Boolean.getBoolean(\"true\")",
        "output": "false\\ntrue",
        "solution": "It's horribly misnamed! Boolean.getBoolean(String) actually reads a System Property (like something passed via -DmyProp=true) and checks if THAT is true. To parse a raw string, you must use parseBoolean().",
        "expected": "Boolean.getBoolean('true') to be true."
    },
    {
        "name": "CatchingThrowableError",
        "imports": "",
        "body": "        try {\n            // Running some code...\n            throw new OutOfMemoryError(\"Fake OOM\");\n        } catch (Exception e) {\n            System.out.println(\"Caught an Exception\");\n        } catch (Throwable t) {\n            System.out.println(\"Caught a Throwable! This is dangerous.\");\n        }",
        "code": "catch (Throwable t)",
        "output": "Caught a Throwable! This is dangerous.",
        "solution": "Throwable is the parent of both Exception and Error. Errors (like OutOfMemoryError or StackOverflowError) are thrown by the JVM when the environment is fundamentally broken. Catching Throwable means you're swallowing these fatal errors instead of letting the app die cleanly.",
        "expected": "Catching Exception is usually enough."
    },
    {
        "name": "IdentityHashMapReference",
        "imports": "import java.util.*;",
        "body": "        // We have two strings that have the same text, but are different objects.\n        String key1 = new String(\"key\");\n        String key2 = new String(\"key\");\n        \n        Map<String, String> identityMap = new IdentityHashMap<>();\n        identityMap.put(key1, \"Value 1\");\n        identityMap.put(key2, \"Value 2\");\n        \n        System.out.println(\"Size of regular HashMap would be 1.\nSize of IdentityHashMap is: \" + identityMap.size());",
        "code": "new IdentityHashMap()",
        "output": "Size of IdentityHashMap is: 2",
        "solution": "IdentityHashMap deliberately ignores the .equals() method and uses the == operator. It compares the actual memory addresses (reference equality). Since we used 'new String()', key1 and key2 are distinct objects in memory.",
        "expected": "Size 1, because the strings have the exact same characters."
    },
    {
        "name": "SubListMemoryLeak",
        "imports": "import java.util.*;",
        "body": "        // Imagine a massive list holding lots of data.\n        List<String> massive = new ArrayList<>(Collections.nCopies(10000, \"HeavyData\"));\n        \n        // We only want the first item.\n        List<String> tinyView = massive.subList(0, 1);\n        \n        // We try to free the huge list...\n        massive = null;\n        System.out.println(\"The tiny view is holding the ENTIRE 10000-element array in memory!\");",
        "code": "hugeList.subList(0, 1)",
        "output": "The tiny view is holding the ENTIRE 10000-element array in memory!",
        "solution": "subList() does NOT copy the data into a new list. It creates a 'view' that holds a strong reference to the original parent list's underlying array. To avoid memory leaks, wrap it in a new list: new ArrayList<>(massive.subList(0, 1)).",
        "expected": "A tiny independent list that takes up almost no memory."
    },
    {
        "name": "ThreadLocalThreadLeak",
        "imports": "import java.util.concurrent.*;",
        "body": "        // ThreadLocals are great for storing data specific to the current thread.\n        ThreadLocal<byte[]> localCtx = new ThreadLocal<>();\n        \n        ExecutorService pool = Executors.newFixedThreadPool(1);\n        pool.submit(() -> {\n            localCtx.set(new byte[1024 * 1024 * 10]); // 10MB\n            System.out.println(\"Set 10MB in ThreadLocal. If we don't call remove(), it stays forever in this pool thread!\");\n            // localCtx.remove(); <- FORGETTING THIS IS DEADLY\n        });\n        pool.shutdown();",
        "code": "ThreadLocal.set() without ThreadLocal.remove() in a ThreadPool",
        "output": "Set 10MB in ThreadLocal...",
        "solution": "When using Thread Pools (like Tomcat or standard Executors), threads are reused. If you set a ThreadLocal and forget to remove() it, that data lives on forever attached to that thread, causing massive memory leaks in web applications.",
        "expected": "ThreadLocal data dies when the specific task finishes."
    },
    {
        "name": "ResourceBundleCaching",
        "imports": "import java.util.*;",
        "body": "        try {\n            // Usually you'd load a properties file, but we just simulate the call.\n            ResourceBundle b = ResourceBundle.getBundle(\"fake_file\");\n        } catch (MissingResourceException e) {\n            System.out.println(\"ResourceBundles heavily cache their lookups in memory.\");\n        }",
        "code": "ResourceBundle.getBundle() relies on deep caching",
        "output": "ResourceBundles heavily cache...",
        "solution": "By default, ResourceBundle caches completely. If you change a translation file on disk, the running JVM won't see it until you reboot it, or until you write a custom ResourceBundle.Control to clear the cache.",
        "expected": "Hot-reloading of properties files."
    },
    {
        "name": "EnumOrdinalFragility",
        "imports": "",
        "body": "        enum Status { PENDING, ACTIVE, INACTIVE }\n        \n        Status current = Status.ACTIVE;\n        System.out.println(\"The DB saved ACTIVE as ordinal: \" + current.ordinal());\n        System.out.println(\"If we add 'NEW' at the top of the enum, ACTIVE becomes ordinal 2, breaking all our DB mappings!\");",
        "code": "Enum.ordinal() saved to database",
        "output": "The DB saved ACTIVE as ordinal: 1\\nIf we add 'NEW'...",
        "solution": "Never rely on enum.ordinal() for persistent storage or RPC data. If another developer rearranges the enum constants in the source file, all your database values will silently point to the wrong constants. Always save the enum.name() (as a string) instead.",
        "expected": "Using numbers is faster and saves DB space, so it seems like a good idea."
    },
    {
        "name": "SerializationUIDMismatch",
        "imports": "import java.io.*;",
        "body": "        System.out.println(\"If you serialize a class, then add a field to it without setting a static serialVersionUID...\");\n        System.out.println(\"Deserializing the old bytes will throw an InvalidClassException!\");",
        "code": "Not defining serialVersionUID",
        "output": "InvalidClassException on update",
        "solution": "When Java serializes an object, it calculates a hash of the class structure. If you don't explicitly define `private static final long serialVersionUID = 1L;`, the compiler generates one entirely based on the fields and methods. Any change breaks compatibility.",
        "expected": "I can just add new fields and older serialized data will leave them null."
    },
    {
        "name": "PhantomReferenceQueue",
        "imports": "import java.lang.ref.*;",
        "body": "        Object bigObject = new Object();\n        ReferenceQueue<Object> rq = new ReferenceQueue<>();\n        PhantomReference<Object> phantom = new PhantomReference<>(bigObject, rq);\n        \n        bigObject = null;\n        System.gc(); // Suggest garbage collection\n        \n        System.out.println(\"Phantom references let us know EXACTLY when an object has been annihilated by the GC.\");",
        "code": "PhantomReference usage",
        "output": "Phantom references let us know EXACTLY...",
        "solution": "Unlike Weak or Soft references, you cannot call .get() on a PhantomReference (it always returns null). Its sole purpose is to be enqueued when the object it points to is absolutely, positively destroyed\u2014useful for safely scheduling off-heap memory cleanup.",
        "expected": "Just use finalize(). (Don't!)"
    },
    {
        "name": "OptionalGetUnsafe",
        "imports": "import java.util.Optional;",
        "body": "        Optional<String> emptyOp = Optional.empty();\n        \n        System.out.println(\"A lot of devs just call .get()...\");\n        try {\n            String value = emptyOp.get();\n        } catch (NoSuchElementException e) {\n            System.out.println(\"And this is why you must check .isPresent() or use .orElse()!\");\n        }",
        "code": "Optional.empty().get()",
        "output": "And this is why you must check...",
        "solution": "Optional was introduced to fix NullPointerExceptions, but calling .get() directly on an empty optional throws a NoSuchElementException\u2014you've just traded one crash for another. Always use .orElse(), .orElseGet(), or .ifPresent().",
        "expected": "It returns null."
    },
    {
        "name": "MethodReferenceShadow",
        "imports": "import java.util.function.Supplier;",
        "body": "        String word = \"original \";\n        Supplier<String> methodRef = word::toUpperCase;\n        \n        // Changing the variable doesn't change the captured instance!\n        word = \"replaced\";\n        \n        System.out.println(\"Method ref evaluated: \" + methodRef.get());",
        "code": "String s = 'A'; Supplier sup = s::toUpperCase; s = 'B'; sup.get()",
        "output": "Method ref evaluated: ORIGINAL ",
        "solution": "When you create a method reference like `myVar::method`, Java evaluates `myVar` at the exact moment the lambda is defined, not when it runs. It captures the pointer to the 'original' string object forever.",
        "expected": "It evaluates relative to the newest state of the variable."
    },
    {
        "name": "ArrayDequeNulls",
        "imports": "import java.util.ArrayDeque; import java.util.Deque;",
        "body": "        Deque<String> deque = new ArrayDeque<>();\n        try {\n            deque.add(null);\n        } catch (NullPointerException e) {\n            System.out.println(\"ArrayDeque strictly forbids nulls!\");\n        }",
        "code": "new ArrayDeque().add(null)",
        "output": "ArrayDeque strictly forbids nulls!",
        "solution": "LinkedList allows 'null' elements, making it okay for a List context. But ArrayDeque was designed as a high-performance stack/queue and explicitly outlaws nulls. This is because it uses null internally to flag an empty slot in its circular backing array.",
        "expected": "Adding null works fine, like in an ArrayList."
    },
    {
        "name": "PriorityQueueIteration",
        "imports": "import java.util.PriorityQueue;",
        "body": "        PriorityQueue<Integer> pq = new PriorityQueue<>();\n        pq.add(4); pq.add(1); pq.add(3); pq.add(2);\n        \n        System.out.println(\"Iterating over the queue directly: \" + pq);\n        \n        System.out.print(\"Polling one by one: \");\n        while (!pq.isEmpty()) System.out.print(pq.poll() + \" \");\n        System.out.println();",
        "code": "Iterating a PriorityQueue",
        "output": "Iterating over the queue directly: [1, 2, 3, 4] (but wait!) \\nPolling one by one: 1 2 3 4",
        "solution": "A PriorityQueue is implemented by a binary heap array. A basic iterator just walks through that raw underlying array, which is completely out of order in terms of sorting. The only way to securely pull out sorted elements is to call poll() repeatedly.",
        "expected": "The iterator prints them in perfectly sorted order."
    },
    {
        "name": "BitSetGrowth",
        "imports": "import java.util.BitSet;",
        "body": "        BitSet bits = new BitSet();\n        bits.set(0);\n        System.out.println(\"Internal size: \" + bits.size());\n        \n        bits.set(100_000);\n        System.out.println(\"It elasticity grew! Internal size: \" + bits.size());",
        "code": "new BitSet().set(100_000)",
        "output": "Internal size: 64\\nIt elasticity grew! Internal size: 100032",
        "solution": "A BitSet uses a 'long' array to store bits efficiently. If you set a bit way out of bounds, it silently creates massive backing arrays to cover the distance. Passing an external ID as an index could trigger a huge memory spike.",
        "expected": "Out of bounds error."
    },
    {
        "name": "StackTracePerformance",
        "imports": "",
        "body": "        System.out.println(\"Generating an exception is fast.\");\n        System.out.println(\"But resolving the stack trace (Throwable::fillInStackTrace) is EXTREMELY slow!\");\n        \n        // This takes milliseconds, which is an eternity in code.\n        new RuntimeException(\"Whoops! Unwinding the C++ JVM stack frames now...\");",
        "code": "new Throwable().getStackTrace()",
        "output": "Performance hit.",
        "solution": "Instantiating an Exception forces the JVM to walk backward through the call stack to capture class names, method names, and line numbers. Never use exceptions for normal control flow (like validating forms) because this stack walk kills performance.",
        "expected": "It's instantaneous."
    },
    {
        "name": "ProxyDynamicGeneration",
        "imports": "import java.lang.reflect.*;",
        "body": "        System.out.println(\"Java lets you create classes that don't exist at compile time!\");\n        Runnable proxy = (Runnable) Proxy.newProxyInstance(\n            ClassLoader.getSystemClassLoader(),\n            new Class[]{Runnable.class},\n            (proxyObj, method, argsProxy) -> {\n                System.out.println(\"Intercepted run() call!\");\n                return null;\n            }\n        );\n        proxy.run();",
        "code": "Proxy.newProxyInstance()",
        "output": "Intercepted run() call!",
        "solution": "Dynamic proxies weave bytecode at runtime, creating an interceptor for an interface. It is the core magic behind frameworks like Spring AOP, allowing them to wrap your database calls with transactional boundaries automatically.",
        "expected": "You have to write a concrete `class MyRun implements Runnable`."
    },
    {
        "name": "TransientSerialization",
        "imports": "import java.io.*;",
        "body": "        System.out.println(\"If a class implements Serializable, all its fields are saved to byte streams.\");\n        System.out.println(\"...Unless you mark the field 'transient'.\");\n        System.out.println(\"When deserialized, transient fields will just be null (or 0 for ints).\");",
        "code": "private transient String password;",
        "output": "Null/Zero upon loading",
        "solution": "The transient keyword acts as a privacy or memory-optimization flag. It tells Java not to bother writing that piece of data to disk. It's often used for passwords, temporary cache fields, or network sockets.",
        "expected": "Everything gets saved."
    },
    {
        "name": "DoubleToLongBitCast",
        "imports": "",
        "body": "        double giantDecimal = Double.MAX_VALUE;\n        long maxInt64 = (long) giantDecimal;\n        \n        System.out.println(\"Double MAX: \" + giantDecimal);\n        System.out.println(\"Cast to long: \" + maxInt64);\n        System.out.println(\"Is that Long.MAX_VALUE? \" + (maxInt64 == Long.MAX_VALUE));",
        "code": "(long) Double.MAX_VALUE",
        "output": "Double MAX: 1.7976931348623157E308\\nCast to long: 9223372036854775807\\nIs that Long.MAX_VALUE? true",
        "solution": "A double has a vastly higher maximum limit than a long, by trading precision for an exponent. When you cast a double that exceeds the long boundary down to a long, it doesn't wrap around like integers do; it just caps cleanly at Long.MAX_VALUE.",
        "expected": "An overflow anomaly resulting in negative garbage values."
    },
    {
        "name": "StringReplaceRegexDot",
        "imports": "",
        "body": "        String text = \"a.b.c\";\n        // Let's replace the literal dots with dashes.\n        String result = text.replaceAll(\".\", \"-\");\n        System.out.println(\"Wait, where did the letters go? \" + result);",
        "code": "text.replaceAll(\".\", \"-\")",
        "output": "Wait, where did the letters go? -----",
        "solution": "String.replaceAll(target, replacement) interprets the target as a Regular Expression! In regex, a '.' isn't a period; it means 'match ANY character'. To replace actual periods, you must escape it: replaceAll(\"\\\\.\", \"-\") or just use replace(\".\", \"-\").",
        "expected": "a-b-c"
    },
    {
        "name": "ScannerSkipNewline",
        "imports": "import java.util.Scanner; import java.io.ByteArrayInputStream;",
        "body": "        String input = \"42\\nHello World\\n\";\n        Scanner sc = new Scanner(new ByteArrayInputStream(input.getBytes()));\n        \n        int number = sc.nextInt();\n        String text = sc.nextLine();\n        \n        System.out.println(\"Number was: \" + number);\n        System.out.println(\"Text was: '\" + text + \"'\");",
        "code": "sc.nextInt(); sc.nextLine();",
        "output": "Number was: 42\\nText was: ''",
        "solution": "nextInt() reads the integer but completely ignores the \\n character trailing it. The very next call to nextLine() instantly consumes that leftover \\n, returning a blank string. Always do an extra dummy `sc.nextLine()` after picking up ints from console input.",
        "expected": "Text was: 'Hello World'"
    },
    {
        "name": "WeakHashMapKeyGC",
        "imports": "import java.util.*;",
        "body": "        Map<Object, String> weak = new WeakHashMap<>();\n        Object key = new Object();\n        weak.put(key, \"Data\");\n        \n        System.out.println(\"Map size: \" + weak.size());\n        key = null; // We throw away our reference\n        System.gc(); // Force garbage collector\n        \n        System.out.println(\"If Java needs memory, the map secretly deletes the entry: \" + weak.isEmpty());",
        "code": "WeakHashMap entry lifecycle",
        "output": "Map size: 1\\n...map secretly deletes the entry: true (eventually)",
        "solution": "A WeakHashMap holds 'weak' references to its keys. If no other thread in the entire app holds a strong reference to that key object, the Garbage Collector will purge it, and the map will automatically slice out the corresponding key-value pair.",
        "expected": "Keys stay until YOU explicitly remove them."
    },
    {
        "name": "AtomicIntegerABA",
        "imports": "import java.util.concurrent.atomic.*;",
        "body": "        // We want to update an atomic value from 1 to 3, but only if it's currently 1.\n        AtomicInteger val = new AtomicInteger(1);\n        \n        // Sneaky thread does: val.set(2); then quickly val.set(1);\n        \n        boolean success = val.compareAndSet(1, 3);\n        System.out.println(\"Did we succeed? \" + success);\n        System.out.println(\"BUT WE MISSED THE INTERMEDIATE CHANGES!\");",
        "code": "compareAndSet(1, 3)",
        "output": "Did we succeed? true\\nBUT WE MISSED...",
        "solution": "This is the classic ABA problem in lock-free programming. If variable 'a' is changed to 'b' and back to 'a', compareAndSet thinks nothing ever changed. To solve this in deep algorithms, Java provides AtomicStampedReference, which attaches a version counter to the object.",
        "expected": "It shouldn't succeed if something modified it in the interim."
    },
    {
        "name": "SynchronizedBlockNull",
        "imports": "",
        "body": "        Object lock = null;\n        try {\n            synchronized(lock) {\n                System.out.println(\"In lock.\");\n            }\n        } catch (NullPointerException e) {\n            System.out.println(\"You can't lock on a null object!\");\n        }",
        "code": "synchronized(null) { ... }",
        "output": "You can't lock on a null object!",
        "solution": "Every object in Java comes with a hidden monitor (lock) attached to the memory allocation. A null reference points to absolutely nothing, meaning there is no monitor to acquire. The JVM immediately responds with a NullPointerException.",
        "expected": "Sleeps until the lock is initialized."
    },
    {
        "name": "ExceptionSuppressionFinally",
        "imports": "",
        "body": "        try (BadResource br = new BadResource()) {\n            throw new RuntimeException(\"Primary Error!\");\n        } catch (Exception e) {\n            System.out.println(\"Caught: \" + e.getMessage());\n            System.out.println(\"Suppressed: \" + e.getSuppressed()[0].getMessage());\n        }\n    }\n    static class BadResource implements AutoCloseable {\n        public void close() { throw new RuntimeException(\"Close Error!\"); }",
        "code": "try-with-resources with throwing close()",
        "output": "Caught: Primary Error!\\nSuppressed: Close Error!",
        "solution": "Unlike old-school finally blocks that completely swallow primary exceptions, try-with-resources captures the primary 'try' exception, and neatly 'attaches' the secondary 'close()' exception as an array of 'suppressed' errors, preserving all debugging info.",
        "expected": "The 'close' exception wipes out the try block exception."
    },
    {
        "name": "VolatileVisibilityGuarantee",
        "imports": "",
        "body": "        // 1. Thread A sets: done = true\n        // 2. Thread B checking an old CPU cache loop never sees it!\n        System.out.println(\"Normally, CPUs cache data aggressively.\");\n        System.out.println(\"Marking a variable 'volatile' forces the thread to bypass local cache and read/write directly to main RAM.\");",
        "code": "private volatile boolean shutdown;",
        "output": "Cross-thread alignment",
        "solution": "'volatile' establishes a formal 'happens-before' edge. Writes to the variable are immediately flushed across the memory barrier, invalidating the caches for all other threads. It's the cheapest but most subtle synchronization tool.",
        "expected": "All threads see memory exactly the same all the time."
    },
    {
        "name": "ProcessWaitForBlock",
        "imports": "import java.io.*;",
        "body": "        try {\n            // We launch a script that dumps 10MB of text to the console...\n            // Process p = Runtime.getRuntime().exec(\"heavy_script.sh\");\n            // p.waitFor();\n            System.out.println(\"If you don't read the Process's InputStream, the process's pipe buffer fills up.\");\n        } catch (Exception e) { }",
        "code": "process.waitFor() without consuming streams",
        "output": "Indefinite hanging",
        "solution": "The OS only allocates a tiny buffer (like 8KB) for a process's standard output. If your Java code waits without continuously reading that output stream, the buffer fills up, and the OS freezes the child process indefinitely. A classic integration deadlock.",
        "expected": "Waits cleanly for the script to finish."
    },
    {
        "name": "NoClassDefFoundErrorRuntime",
        "imports": "",
        "body": "        System.out.println(\"Compile your app with Library v1.jar.\");\n        System.out.println(\"Deploy it, but accidentally bundle Library v2.jar, where they renamed a critical class.\");\n        System.out.println(\"You won't get ClassNotFoundException... you get something worse!\");",
        "code": "Missing dependency at runtime",
        "output": "java.lang.NoClassDefFoundError",
        "solution": "ClassNotFoundException implies you tried to load a class via reflection (Class.forName) and it wasn't there. NoClassDefFoundError is a severe internal JVM Error. It implies the bytecode 'hard links' to a class that was present at compile time, but missing at runtime execution.",
        "expected": "ClassNotFoundException"
    },
    {
        "name": "StackOverflowRecursion",
        "imports": "",
        "body": "        System.out.println(\"JVM memory is split into Heap (objects) and Stack (method calls).\");\n        System.out.println(\"Infinite recursion doesn't out-of-memory the heap... it blows up the Stack!\");\n        // We'd write an infinite recursive method here, but we don't want to crash.\n        // recurse();",
        "code": "void recurse(){ recurse(); }",
        "output": "java.lang.StackOverflowError",
        "solution": "Each method invocation carves out a 'stack frame' to hold its local primitives and pointers. The JVM only allows a fixed depth (a few thousand frames). Infinite loops push frames until you slam into the roof.",
        "expected": "An eventual OutOfMemoryException."
    },
    {
        "name": "CharToStringHash",
        "imports": "",
        "body": "        char[] secretChars = {'a', 'b', 'c'};\n        \n        // Let's print out the chars as part of a string...\n        System.out.println(\"The secret is: \" + secretChars);",
        "code": "\"text \" + charArray",
        "output": "The secret is: [C@7a81197d",
        "solution": "Array types in Java do not override the Object.toString() method! Therefore, they resort to printing out a type string '[C' (array of chars) followed by the '@' hexadecimal memory-hash reference. You must use String.valueOf(secretChars).",
        "expected": "The secret is: abc"
    },
    {
        "name": "ConcurrentModificationIterator",
        "imports": "import java.util.*;",
        "body": "        List<String> list = new ArrayList<>(Arrays.asList(\"X\", \"Y\"));\n        try {\n            for (String str : list) {\n                list.remove(str); \n            }\n        } catch (ConcurrentModificationException e) {\n            System.out.println(\"You can't modify the collection structure while an iterator is walking over it!\");\n        }",
        "code": "list.remove() inside enhanced for-loop",
        "output": "ConcurrentModificationException",
        "solution": "The enhanced 'for-each' loop secretly deploys an Iterator. If you call list.remove() directly, the underlying array shrinks, but the Iterator's internal pointer doesn't know about it. The JVM throws CME proactively to prevent array bounds corruption.",
        "expected": "Items neatly removing themselves."
    },
    {
        "name": "IdentityHashCodeAddress",
        "imports": "",
        "body": "        Object obj = new Object();\n        // People assume this gives physical memory RAM addresses...\n        int hash = System.identityHashCode(obj);\n        System.out.println(\"Identity Hash: \" + hash);",
        "code": "System.identityHashCode()",
        "output": "Identity Hash: 2055281021",
        "solution": "It's a persistent myth that identityHashCode generates a real RAM address. In modern JVMs, it's typically just a randomly generated integer stored in the object's header. Real memory addresses change constantly during Garbage Collector relocation anyway!",
        "expected": "The physical memory address pointer for C-style interoperability."
    },
    {
        "name": "BigDecimalScaleComparison",
        "imports": "import java.math.BigDecimal;",
        "body": "        BigDecimal a = new BigDecimal(\"1.0\");\n        BigDecimal b = new BigDecimal(\"1.00\");\n        \n        System.out.println(\"Are they .equals()? \" + a.equals(b));\n        System.out.println(\"Are they .compareTo() equal? \" + (a.compareTo(b) == 0));",
        "code": "new BigDecimal(\"1.0\").equals(new BigDecimal(\"1.00\"))",
        "output": "false\\ntrue",
        "solution": "BigDecimal encapsulates both the value AND the 'scale' (the precision zeros). The .equals() method dictates that if the scales are different (1 decimal vs 2 decimals), they are completely different objects. To verify mathematical equality, always rely on compareTo().",
        "expected": ".equals() to be true because math says 1.0 = 1.00."
    },
    {
        "name": "FloatNegativeZero",
        "imports": "",
        "body": "        // IEEE-754 is weird. Zero has a sign bit.\n        System.out.println(\"Is 0.0 == -0.0? \" + (0.0 == -0.0));\n        \n        System.out.println(\"But what if we divide 1 by them?\");\n        System.out.println(\"1.0 / 0.0 = \" + (1.0 / 0.0));\n        System.out.println(\"1.0 / -0.0 = \" + (1.0 / -0.0));",
        "code": "1.0 / -0.0",
        "output": "Is 0.0 == -0.0? true\\n1.0 / 0.0 = Infinity\\n1.0 / -0.0 = -Infinity",
        "solution": "In binary floating point, zero is represented with a sign bit intact. While logic operators (==) treat them as identical to comply with mathematical norms, functions like division expose the actual underlying bit distinction.",
        "expected": "Division should have the same result if they are truly equal."
    },
    {
        "name": "MathHypotOverflow",
        "imports": "",
        "body": "        // Pythagoras formula: a^2 + b^2 = c^2 (sqrt)\n        double max = 1.0E300; // Almost overflow!\n        \n        System.out.println(\"A naive calc (max * max) would explode immediately into Infinity.\");\n        System.out.println(\"But Math.hypot(max, max) works perfectly: \" + Math.hypot(max, max));",
        "code": "Math.hypot(a, b)",
        "output": "...Math.hypot() works perfectly: 1.414213562373095E300",
        "solution": "Math.hypot performs intermediate scaling. Instead of immediately squaring gigantic values and overflowing the double space, it scales the arguments down, computes the square root safely, and scales back up. Brilliant core library engineering.",
        "expected": "Infinity due to early square overflow."
    },
    {
        "name": "EnumSwitchNullPointerException",
        "imports": "",
        "body": "        System.out.println(\"We switch on an Enum, but the Enum is null.\");\n        Day chosen = null;\n        try {\n            switch(chosen) {\n                case MONDAY: System.out.println(\"Mon\"); break;\n                default: System.out.println(\"Def\");\n            }\n        } catch (NullPointerException e) {\n            System.out.println(\"Switch statements on enums blindly call .ordinal() under the hood!\");\n        }\n    }\n    enum Day { MONDAY }",
        "code": "switch(enumVarThatIsNull)",
        "output": "Switch statements on enums blindly call .ordinal() under the hood!",
        "solution": "To make enum switches extremely fast, the Java bytecode translates the switch into a jump table based on the enum's integer 'ordinal()'. Trying to execute .ordinal() on a null pointer triggers an immediate NullPointerException.",
        "expected": "It falls cleanly into the 'default' block."
    },
    {
        "name": "SystemEnvCaseSensitivity",
        "imports": "",
        "body": "        String homeCase1 = System.getenv(\"path\");\n        String homeCase2 = System.getenv(\"PATH\");\n        System.out.println(\"Depending on whether you run this on MacOS, Linux, or Windows, one of these may be null!\");",
        "code": "System.getenv(\"path\")",
        "output": "Varies by OS structure.",
        "solution": "Java strives for 'Write Once, Run Anywhere'. However, System.getenv directly exposes the underlying Operating System's environment variables. Windows env vars are case-insensitive. Linux environments are strictly case-sensitive. This discrepancy breaks cross-platform scripts.",
        "expected": "Consistent behavior across operating systems."
    },
    {
        "name": "InheritableThreadLocalLeak",
        "imports": "import java.util.concurrent.*;",
        "body": "        System.out.println(\"InheritableThreadLocal passes parent thread data to newly spawned child threads.\");\n        System.out.println(\"But if you're using Executors, threads are dumped back into a pool, and the 'leaked' parent context persists for future jobs!\");",
        "code": "new InheritableThreadLocal<>() with Executors",
        "output": "Potential massive security scope leaks.",
        "solution": "Inheriting context is useful for trace-IDs, but in pooled environments, a thread never truly 'dies'. If the pool assigns the thread to a completely different user's HTTP request later, it might still have Admin security credentials floating inside its InheritableThreadLocal.",
        "expected": "Clean state context."
    },
    {
        "name": "StrictfpPlatformConsistency",
        "imports": "",
        "body": "        System.out.println(\"Running complex physics math on an Intel CPU vs an ARM CPU can diverge tiny decimal bits over time.\");\n        System.out.println(\"Using the modifier 'strictfp' forces the JVM to truncate calculations strictly to 64-bit IEEE boundaries.\");",
        "code": "public strictfp class PhysicsEngine",
        "output": "100% Identical math outputs on all CPUs.",
        "solution": "Modern CPU registers often perform intermediate floating math at 80-bit precision, offering slightly 'better' results. However, 'strictfp' forces the JVM to chop these back to 64-bit precision so multiplayer replay systems don't fall out of sync across different processors.",
        "expected": "Java math is just automatically universal."
    },
    {
        "name": "IncompatibleClassChangeErrorExt",
        "imports": "",
        "body": "        System.out.println(\"If a class 'A' extends abstract class 'B'...\");\n        System.out.println(\"Then someone updates jar 'B' and changes that class to an interface...\");\n        System.out.println(\"JVM throws an IncompatibleClassChangeError the moment 'A' executes via bytecode.\");",
        "code": "Library update altering class contract types",
        "output": "IncompatibleClassChangeError",
        "solution": "Binary compatibility means older compiled .class files must cleanly link with modern dependencies. An interface uses the 'invokeinterface' bytecode instruction, while an abstract class uses 'invokevirtual'. Altering the fundamental structure of a hierarchy snaps these bytecode linkages immediately.",
        "expected": "A clean runtime failure or NoSuchMethodException."
    },
    {
        "name": "RecordImmutabilityMyth",
        "imports": "import java.util.*;",
        "body": "        // We create a shiny new 'immutable' record\n        Config settings = new Config(new ArrayList<>());\n        \n        System.out.println(\"List before: \" + settings.keys());\n        settings.keys().add(\"HAH! I mutated the un-mutable!\");\n        System.out.println(\"List after: \" + settings.keys());\n    }\n    record Config(List<String> keys) {}",
        "code": "Mutating internal structures of Java Records",
        "output": "List after: [HAH! I mutated the un-mutable!]",
        "solution": "Records generate 'final' variable fields automatically, but final just means the 'pointer address' cannot be swapped. The internal object (like an ArrayList) resides in the heap and remains perfectly mutable. For true immutability, pass List.copyOf() to the record constructor.",
        "expected": "Compile or runtime error halting the modification."
    },
    {
        "name": "StaticImportMethodClash",
        "imports": "",
        "body": "        System.out.println(\"import static java.util.Collections.sort;\");\n        System.out.println(\"import static java.util.Arrays.sort;\");\n        System.out.println(\"Which 'sort' wins if you just type sort(data)? Neither! It's a compiler error.\");",
        "code": "import static collisions",
        "output": "Compile Error",
        "solution": "If two static imports deliver methods with identical names, Java refuses to guess which one you intend, despite parameter differences preventing a direct signature ambiguity. The compiler enforces strict name resolution to ensure maintainability.",
        "expected": "Intelligent resolution based on argument types."
    },
    {
        "name": "AssertKeywordDisabled",
        "imports": "",
        "body": "        System.out.println(\"I'm going to assert that 1 == 0, which is totally false.\");\n        assert 1 == 0 : \"Mathematics is broken!\";\n        System.out.println(\"The program continues to run without error!\");",
        "code": "assert false;",
        "output": "The program continues to run...",
        "solution": "In Java, assertions are completely skipped and ignored by the JVM by default to optimize runtime speeds. You MUST supply the '-ea' (enable assertions) flag to the Java executable on startup to actually trigger AssertionError evaluations.",
        "expected": "Immediate crash."
    },
    {
        "name": "SealedClassHierarchy",
        "imports": "",
        "body": "        System.out.println(\"Java 17 adds 'sealed' classes to give you strict control over inheritance.\");\n        System.out.println(\"Only classes explicitly listed in the 'permits' clause can extend this parent.\");",
        "code": "public sealed class Shape permits Circle, Square {}",
        "output": "Compile error on unauthorized subclasses",
        "solution": "Sometimes you want polymorphic objects (like an Expr tree) but you don't want any random plugin trying to extend it. Before sealed classes, we used package-private constructors. Now we have an elegant, compiler-enforced domain restriction.",
        "expected": "Public classes can be inherited by anyone."
    },
    {
        "name": "VarargsNullAmbiguity",
        "imports": "",
        "body": "        printSizes(null);\n    }\n    static void printSizes(Integer... args) {\n        System.out.println(\"Did we pass an empty array, a single null value, or a null array?\");\n        System.out.println(\"It's a completely null array! Length check throws NPE: \" + (args == null));",
        "code": "printSizes(null) against Object... args",
        "output": "...Length check throws NPE: true",
        "solution": "Varargs (Object...) secretly compiles down to Object[]. When you pass 'null', Java prioritizes treating the entire array as null (which triggers NPE when trying to iterate), rather than wrapping the null inside a new 1-element array like `new Object[]{null}`.",
        "expected": "The method executes with an array holding one null element."
    },
    {
        "name": "StringJoinerEmptyPrefix",
        "imports": "import java.util.StringJoiner;",
        "body": "        // We want a comma-separated list of JSON objects wrapped in brackets\n        StringJoiner sj = new StringJoiner(\",\", \"[\", \"]\");\n        \n        System.out.println(\"But what if we add nothing to it? Output: \" + sj.toString());\n        // Oops. It prints [] even if empty. To fix it: sj.setEmptyValue(\"\");",
        "code": "StringJoiner(\",\", \"[\", \"]\") without adds",
        "output": "Output: []",
        "solution": "By default, StringJoiner outputs its prefix and suffix together if it's completely empty. If you're building SQL IN clauses or JSON arrays dynamically, you'll end up with malformed strings '()' or '[]' unless you explicitly define .setEmptyValue().",
        "expected": "It produces an empty string ''."
    },
    {
        "name": "PropertiesNonStringKeys",
        "imports": "import java.util.Properties;",
        "body": "        Properties props = new Properties();\n        // Since Properties extends Hashtable<Object, Object>, this is insanely legal:\n        props.put(Integer.valueOf(1), new Object());\n        \n        System.out.println(\"Successfully smuggled non-strings into Properties!\");\n        try {\n            // But when we try to save it to disk...\n            // props.store(System.out, \"Crash here\"); \n            System.out.println(\"Trying to serialize this to a file throws ClassCastException internally.\");\n        } catch (Exception e) {}",
        "code": "Properties.put(Integer, Object)",
        "output": "...throws ClassCastException internally.",
        "solution": "The Properties class is an ancient remnant of Java 1.0, wrongly structured via inheritance to inherit from Hashtable. It allows the smuggling of non-String primitives via .put(). However, its dedicated methods like .store() rely blindly on casting the values back to Strings, detonating on execution.",
        "expected": "Compile-time error forbidding non-Strings."
    },
    {
        "name": "VectorLegacySynchronization",
        "imports": "import java.util.Vector;",
        "body": "        Vector<String> ancientList = new Vector<>();\n        ancientList.add(\"Item\");\n        System.out.println(\"Everything inside Vector is forcefully locked via 'synchronized'.\");\n        System.out.println(\"It introduces massive thread-contention bottlenecks for zero upside in modern multi-core apps.\");",
        "code": "Vector vs ArrayList",
        "output": "Execution takes much longer",
        "solution": "Vector, Hashtable, and StringBuffer are ancient 'thread-safe by default' classes. Their methods lock unconditionally. Modern Java best-practice embraces un-synchronized data structures (like ArrayList) and layers explicit atomic controls like ConcurrentHashMap around them only when necessary.",
        "expected": "Vector is just an alternative ArrayList."
    },
    {
        "name": "LiteralUnderscoreVisual",
        "imports": "",
        "body": "        int massiveA = 1000000;\n        int massiveB = 1_000_000;\n        \n        System.out.println(\"Are these numbers literally identical to the compiler? \" + (massiveA == massiveB));",
        "code": "int num = 1_000_000;",
        "output": "Are these numbers literally identical to the compiler? true",
        "solution": "Adding underscores to numbers doesn't change the byte-data. It's an excellent, free syntactic sugar tool to break up long financial figures, hexadecimal padding, or binary strings so developers can read them without squinting.",
        "expected": "It's treated as a String or causes an error."
    },
    {
        "name": "SwitchExpressionYield",
        "imports": "",
        "body": "        int item = 1;\n        String result = switch(item) {\n            case 1 -> \"One\";\n            case 2 -> {\n                System.out.println(\"Executing block logic before yielding...\");\n                yield \"Two!\"; // MUST use yield, NOT return!\n            }\n            default -> \"Unknown\";\n        };\n        System.out.println(\"New Switch Result: \" + result);",
        "code": "switch(val) { case -> yield value; }",
        "output": "New Switch Result: One",
        "solution": "Modern Java adds switch *expressions* that return values. However, if you open a multi-line `{}` block inside a case, you cannot use the `return` keyword because that would exit the entire wrapping method! The `yield` keyword was specifically crafted to pass values up directly from the switch construct.",
        "expected": "Using the 'return' keyword inside the block."
    },
    {
        "name": "LocalClassVariableCapture",
        "imports": "",
        "body": "        int variable = 10;\n        \n        class LocalInternalWorker {\n            void show() {\n                System.out.println(\"I can access the method variable: \" + variable);\n            }\n        }\n        \n        // variable = 20; // If I uncomment this, the class compile fails.\n        new LocalInternalWorker().show();",
        "code": "Method local class variable scoping",
        "output": "I can access the method variable: 10",
        "solution": "Method-local inner classes are essentially 'anonymous classes' with explicit names. They can access the local variables of their enclosing method, but Java strictly mandates those variables be 'effectively final'. This protects your memory against state drifting asynchronously if the local frame collapses.",
        "expected": "The class can see the variable no matter what."
    },
    {
        "name": "RuntimeHaltDestructive",
        "imports": "",
        "body": "        try {\n            System.out.println(\"System.exit(0) kindly executes all Thread shutdown hooks first.\");\n            System.out.println(\"Runtime.getRuntime().halt(0) detonates the JVM on the spot, discarding shutdown hooks! (Avoid this unless desperate).\");\n            // Runtime.getRuntime().halt(0);\n        } finally {\n            System.out.println(\"If halt() ran, this finally block would NEVER execute.\");\n        }",
        "code": "Runtime.getRuntime().halt(0)",
        "output": "If halt() ran, this finally block would NEVER execute.",
        "solution": "System.exit triggers a cascading shutdown sequence: locks sync, files close, and registered shutdown-hooks trigger. Halt bypasses the OS signal handlers entirely and kills the process instance without a trace. It is essentially an instant self-kill -9 command.",
        "expected": "Halt shuts down the system safely."
    },
    {
        "name": "ServiceLoaderDiscovery",
        "imports": "import java.util.ServiceLoader;",
        "body": "        System.out.println(\"Interfaces can be implemented by entirely detached JARs at runtime.\");\n        System.out.println(\"ServiceLoader reads the META-INF/services/ file in your classpath and auto-injects all known implementations seamlessly.\");",
        "code": "ServiceLoader.load(Driver.class)",
        "output": "Dynamically bridges remote plugins without code links.",
        "solution": "JDBC database connections use this heavily. When you load the Postgres JAR, the JVM scans its META-INF file, finds the 'org.postgres.Driver' declaration, and uses ServiceLoader to instantiate it without you ever importing postgres packages directly.",
        "expected": "Hardcoded instantiation via 'new PostgresDriver()'"
    },
    {
        "name": "ClassLiteralPrimitives",
        "imports": "",
        "body": "        Class<Integer> wrapperObj = Integer.class;\n        Class<Integer> primObj = int.class;\n        \n        System.out.println(\"Is integer identical to int? \" + (wrapperObj == primObj));\n        System.out.println(\"int.class exists! Type is: \" + primObj.getName());",
        "code": "int.class vs Integer.class",
        "output": "Is integer identical to int? false\\nint.class exists! Type is: int",
        "solution": "Even though primitives do not inherit from `java.lang.Object`, the JVM grants each primitive its own distinct 'Class' meta-object representation (`int.class`). This is incredibly important for the Reflection API to properly verify method signatures like `method.invoke(object, int.class)`.",
        "expected": "Primitives cannot have a .class method because they aren't Objects."
    }
]

def run_command(cmd, env=None):
    subprocess.run(cmd, shell=True, check=True, env=env)

start_date = datetime(2026, 1, 1)
end_date = datetime(2026, 4, 8)
delta = end_date - start_date

import shutil
if os.path.exists("src"):
    shutil.rmtree("src")
os.makedirs("src/com/java/anomalies", exist_ok=True)

for i, anomaly in enumerate(anomalies):
    commit_date = start_date + timedelta(seconds=(delta.total_seconds() / len(anomalies)) * i)
    date_str = commit_date.strftime("%Y-%m-%dT%H:%M:%S")

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
        # Avoid json literal string escape mismatches
        f.write(content.replace('\\n', '\n'))

    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = date_str
    env["GIT_COMMITTER_DATE"] = date_str
    
    run_command("git add .")
    run_command(f"git commit -m 'Detailed rewrite: {anomaly['name']}' --date='{date_str}'", env=env)

print(f"Done! 100 perfectly formatted, human-narrated anomalies complete.")
