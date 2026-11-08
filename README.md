Opal1 is a python language extension featuring 26 additional bits of useful syntax that transpile directly to python using a lightweight parser and only standard libraries such as sys and subprocess.

Note: Opal is not an app or a PWA, it is intentionally minimal

Opal1 : Created 11/8/2026 from the core of ESPython 1.07.05
ESPython is very sandbox. Opal1 is not so, the lib system you may know of from ESPython is 

ESPython v1.07.05 Release Link: https://github.com/Cetri12/ESPython/releases/tag/ESPython_1.07.05

Open Tutorial.txt, or read this:


# Notes on Incremental And Decremental Operators:

☑X++
☑X--
❌++X
☑Y = X++
❌Y=X-- (sensitive parser, add spaces around both sides of "=")

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
| **Global Diagnostics** | `debug` | `print(f"DEBUG LAYER CONSOLE: {locals()}


## ⚙Execution:
Drag code.opal1 into the folder, then double click Run.py
The code will automatically execute the transpiled product. (this may be disabled in settings)




