Opal1 is a python language extension featuring 41 additional bits of useful syntax that transpile directly to python using a lightweight parser and only standard libraries such as sys and subprocess.

Note: Opal is not an app or a PWA, it is intentionally minimal

Opal1 : Created 11/8/2026 from the core of ESPython 1.07.05
ESPython is very sandbox. Opal1 is not so, the lib system you may know of from ESPython is not featured in opal

ESPython v1.07.05 Release Link: https://github.com/Cetri12/ESPython/releases/tag/ESPython_1.07.05

Open Tutorial.txt, or read this:

Opal1 is AOT transpired to python, meaning there is no slowdown during processed file execution

# Notes on Incremental And Decremental Operators:

☑X++
☑X--
❌++X
☑Y = X++
❌Y=X-- (sensitive parser, add spaces around both sides of "=")

Notes on Library Dependant Functions:
Opal1 will throw an error if the proper library is not imported, and for clear, it will throw an error if you aren't on windows.

## All Syntax:

| Syntax Feature | Opal1 Standard Code Example | Transpiled Python Output |
| :--- | :--- | :--- |
| **Incremental Operator** | `X++` / `Y = X++` | `X = X + 1` |
| **Decremental Operator** | `X--` | `X = X - 1` |
| **Else if Conditional** | `else if condition:` | `elif condition:` |
| **Unless Conditional** | `unless condition:` | `if not condition:` |
| **Text output without a newline** | `out("Text")` | `print("Text", end="")` |
| **Println** | `println("Text")` | `print("Text")` |
| **Formatted Print** | `printf("Score: {score}")` | `print(f"Score: {score}")` |
| **Integer User Input** | `age = intput("Enter age: ")` | `age = int(input("Enter age: "))` |
| **Float User Input** | `gpa = floatput("Enter GPA: ")` | `gpa = float(input("Enter GPA: "))` |
| **Logical OR Block** | `if A \|\| B:` | `if A or B:` |
| **Logical AND Block** | `if A && B:` | `if A and B:` |
| **Logical NOT Block** | `if ! condition:` | `if not condition:` |
| **Untill Conditional**| `untill condition:` | `while not condition:` |
| **State Nullifiers** | `null` / `nil` / `NaN` / `nothing` | `None` |
| **Lowercase Booleans** | `true` / `false` | `True` / `False` |
| **Object Deletion** | `delete database` | `del database` |
| **Main Execution Block**| `name_is_main:` | `if __name__ == "__main__":` |
| **Global Diagnostics** | `debug` | `print(f"DEBUG LAYER CONSOLE: {locals()}")` |
|**Numerical Loop** | `do num` |  `for i in range(num): `|
|**Forever loop** | `forever` | `While True:` |
|**Alternate Function Keywords** | `fn/func/function` | `def`|
|**Printing Lists** | `printlist(List)` | `print("".join(List))` |
|**Do Nothing** | `do_nothing` | `pass` |
|**Time Delay Function** | `delay()` | `time.sleep()` |
|**Alternate Equals Operator** | `is` | `=` |
|**Force Stop Code** | `stop` | `sys.exit`|
|**Clear Terminal** | `clear` | `sys.platform('cls')` |
|**Even Check** | `Number is_even` | `Number % 2 == 0` |
|**Odd Check** | `Number is_odd` | `Number % 2 != 0` |
|**Lowercase Operator Alternative** | `.lowercase()` | `.lower()` |
|**Uppercase Operator Alternative** | `.uppercase()` | `.upper()` |
|**Alternate If Equal Operator** | `a equals b` |  `a == b` |
|**String Reverse Operator**| `text reversed` |  `text[::-1]` 



## ⚙Execution:
Drag code.opal1 into the folder, then double click Run.py
The code will automatically execute the transpiled product. (this may be disabled in settings)
You can go into the folder and take out the transpiled product and use it. In most runtimes you do not get to see the
compiled product, only the results.

Notes From Creator: 
it took me roughly 3-4 hours to make this from ESPython v1.07.05. Character by Character parsing is very efficient, and has made this parser very simple yet strong. ESPython is the base of opal1, and it was always meant to be so when I first began making Python-S (ESPython was originally called Python-S). This really showed me that making these complex things isn't actually so hard... I learned much from this and I will eventually launch opal2 off the back of opal1, or make an opal version that transpiles to a different coding language.

It took three more hours to jump from v1.0 to v1.1. But opal gained 15 new features, totaling at 41 now. And it has error systems for the library dependent ones. 

