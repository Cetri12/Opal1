#Opal1 Parser. Modified 11/8/2026 for opal1 use. origianlly ESPython parser
import shutil
import sys
import subprocess
from pathlib import Path
import os
import time

LINES = [] #The individual lines
POS = 0 #Position in the line
READ = True #Tells the parser if it should read the code. off for comments and strings
DEPTH = 0 #Depth in the parenthesis
LCHAR = [] #line split into it's chars
STRIN = False #If the parser is in a string
GRID = [] #The list of each edited line. is re-inserted back into the file at the end.
COMMENT = False #Tracker to check if the parer is in a comment
runtime = "python" #The runtime of final executable
LIBS = [] #The python libraries used in the code
EQONLIN = False #If there is an operator such as =, ==, or != on that line
output = "" #the final code to be executed by the opal1 module

Version = "Version 1.1.2"
Build_Data = [Version, "Opal1 Modular Parser", "Gen1"]
def run(opal):
    global READ
    global DEPTH
    global POS
    global LCHAR
    global STRIN
    global GRID
    global COMMENT
    global LIBS
    global EQONLIN
    global output

    with open(opal, "r") as file:
        lines = file.readlines()

    if not lines:
        print()
        print("Opal1 Error: File is empty")
        print("\033[31m~~~~~~~~~~~~~~~~~~~~~~~~~~\033[0m")
        print()
        return "fail"

    for line in lines:
        LCHAR = list(line)
        POS = 0
        READ = True
        STRIN = False
        COMMENT = False
        EQONLIN = False

        #provides a copy of the line split by whitespace
        linestring = line.strip().split(" ")

        #records libraries
        if line.startswith("import"):
            LIBS.append(linestring[1])

        while POS < len(LCHAR):

            if not COMMENT:
                
                if LCHAR[POS] == '"' or LCHAR[POS] == "'":
                    READ = not READ #Flips reading state
                    STRIN = not STRIN #Flips string mode

                if LCHAR[POS] == '\\' and LCHAR[POS+1] == '"':
                    print("Escaped qoute")
                    READ = not READ
                    STRIN = not STRIN


            if READ:
                if LCHAR[POS] == "#":
                    READ = False
                    COMMENT = True


            #====================
            #Main syntax loop 
            #=====================
            if READ and STRIN == False and not COMMENT:

                # $$ Comments
                if "".join(LCHAR[POS:POS+2]) == "$$":
                    del LCHAR[POS:POS+2]
                    LCHAR.insert(POS, "#")
                    POS += 2
                    READ = False #Turns off for the comment :D
                    COMMENT = True


                # // Comments
                startingslash = False
                endingslash = False
                if line.startswith("//") and startingslash == False: 
                    startingslash = True
                    del LCHAR[POS:POS+2]
                    LCHAR.insert(POS, "#")
                    POS += 1
                    READ = False
                    COMMENT = True
                    continue

                if "".join(LCHAR[POS:POS+3]) == ";//" and endingslash == False:
                    endingslash = True
                    del LCHAR[POS:POS+3]
                    LCHAR.insert(POS, " #")
                    POS += 1
                    READ = False
                    COMMENT = True
                    continue

                    if "".join(LCHAR[POS:POS+4]) == "; //" and endingslash == False:
                        endingslash = True
                        del LCHAR[POS:POS+4]
                        LCHAR.insert(POS, " #")
                        POS += 1
                        READ = False
                        COMMENT = True
                        continue


                #Removing semicolons
                if LCHAR[POS:POS+1] == ";":
                    del LCHAR[POS]
                    continue   

                #Formal Detector for =
                if LCHAR[POS] == "=":
                    EQONLIN = True    

                #equals --> ==
                if "".join(LCHAR[POS:POS+6]) == "equals":
                    del LCHAR[POS:POS+6]
                    LCHAR.insert(POS, "==")
                    POS += 2
                    EQONLIN = True
                    continue


                #Incremental
                if "".join(LCHAR[POS:POS+2]) == "++":
                    if not EQONLIN:
                        del LCHAR[POS:POS+2]
                        LCHAR.insert(POS, " += 1")
                        POS += len(" += 1")
                        continue
                        
                    elif EQONLIN:
                        del LCHAR[POS:POS+2]
                        LCHAR.insert(POS, " + 1")
                        POS += len(" + 1")
                        EQONLIN = False
                        continue

                    else:
                        print("Unexpected Error Parsing ++")
                        return "fail"
            
                #Decremental
                if "".join(LCHAR[POS:POS+2]) == "--":
                    if not EQONLIN:
                        del LCHAR[POS:POS+2]
                        LCHAR.insert(POS, " -= 1")
                        POS += len(" -= 1")
                        EQONLIN
                        continue
                        
                    elif EQONLIN:
                        del LCHAR[POS:POS+2]
                        LCHAR.insert(POS, " - 1")
                        POS += len(" - 1")
                        EQONLIN = False
                        continue

                    else:
                        print("Unexpected Error Parsing --")
                        return "fail"
            
                # else if
                if "".join(LCHAR[POS:POS+7]) == "else if":
                    del LCHAR[POS:POS+7]
                    LCHAR.insert(POS, "elif")
                    POS += 7
                    continue

                #unless
                if "".join(LCHAR[POS:POS+6]) == "unless":
                    del LCHAR[POS:POS+6]
                    LCHAR.insert(POS, "if not")
                    POS += 6
                    continue

                # && (logical and)
                if "".join(LCHAR[POS:POS+2]) == "&&":
                    del LCHAR[POS:POS+2]
                    LCHAR.insert(POS, "and")
                    POS += 3
                    continue 

                # || (logical or)
                if "".join(LCHAR[POS:POS+2]) == "||":
                    del LCHAR[POS:POS+2]
                    LCHAR.insert(POS, "or")
                    POS += 2
                    continue     

                # ! (logical not)
                if "".join(LCHAR[POS:POS+2]) == " !":
                    del LCHAR[POS:POS+2]
                    LCHAR.insert(POS, "not")
                    POS += 3
                    continue      

                # println()
                if "".join(LCHAR[POS:POS+7]) == "println":
                    del LCHAR[POS:POS+7]
                    LCHAR.insert(POS, "print")
                    POS += 5
                    continue    

                #out(). prints text without a newline
                #A horrible pain to code
                if "".join(LCHAR[POS:POS+4]) == "out(":
                    posahead = POS + 4
                    found = False

                    while posahead < len(LCHAR):
                        if LCHAR[posahead] == ")":
                            found = True
                            break
                        posahead += 1
                    
                    if found:
                        end = (', end="")')
                        LCHAR[posahead] = end
                        del LCHAR[POS:POS+4]
                        LCHAR[POS:POS] = "print("
                        POS = posahead + len(end) + 1
                        continue

                #do_nothing --> pass
                if "".join(LCHAR[POS:POS+10]) == "do nothing" or "".join(LCHAR[POS:POS+10]) == "do_nothing":
                    del LCHAR[POS:POS+10]
                    LCHAR.insert(POS, "pass")
                    POS += 4
                    continue

                # null, NaN, nil, and nothing
                if "".join(LCHAR[POS:POS+3]) == "NaN" or "".join(LCHAR[POS:POS+3]) == "nil":
                    del LCHAR[POS:POS+3]

                if "".join(LCHAR[POS:POS+4]) == "Null":
                    del LCHAR[POS:POS+4]

                if "".join(LCHAR[POS:POS+7]) == "nothing":
                    del LCHAR[POS:POS+7]

                    LCHAR.insert(POS, "None")
                    POS += 4
                    continue

                #Lowercase booleans: true and false
                if "".join(LCHAR[POS:POS+4]) == "true":
                    del LCHAR[POS:POS+4]
                    LCHAR.insert(POS, "True")
                    POS += 4
                    continue

                elif "".join(LCHAR[POS:POS+5]) == "false":
                    del LCHAR[POS:POS+5]
                    LCHAR.insert(POS, "False")
                    POS += 5
                    continue          

                # name_is_main
                if "".join(LCHAR[POS:POS+12]) == "name_is_main":
                    del LCHAR[POS:POS+12]
                    LCHAR.insert(POS, '__name__ == "__main__"')
                    POS += 22
                    continue  

                #printf()
                if "".join(LCHAR[POS:POS+6]) == "printf(":
                    del LCHAR[POS:POS+6]
                    LCHAR.insert(POS, 'print(f')
                    POS += 7
                    continue  

                #delete --> del
                if "".join(LCHAR[POS:POS+6]) == "delete":
                    del LCHAR[POS:POS+6]
                    LCHAR.insert(POS, "del")
                    POS += 3
                    continue

                # intput( --> int(input(  
                #Easier to code than out(), but still a pain ;-;
                if "".join(LCHAR[POS:POS+7]) == "intput(":

                    iPOS = POS + 1
                    ifound = False
                    for i in LCHAR:
                        if i == ")" and ifound == False:
                            LCHAR.insert(iPOS, ")" )
                            ifound = True
                        iPOS += 1

                    del LCHAR[POS:POS+7]
                    LCHAR.insert(POS, "int(input(")
                    POS += 10
                    continue

                # floatput( --> float(input(  
                if "".join(LCHAR[POS:POS+8]) == "floatput(":

                    iPOS = POS + 1
                    ifound = False
                    for i in LCHAR:
                        if i == ")" and ifound == False:
                            LCHAR.insert(iPOS, ")" )
                            ifound = True
                        iPOS += 1

                    del LCHAR[POS:POS+8]
                    LCHAR.insert(POS, "float(input(")
                    POS += 12
                    continue

                #until --> while not
                if "".join(LCHAR[POS:POS+6]) == "untill":
                    del LCHAR[POS:POS+6]
                    LCHAR.insert(POS, "while not")
                    POS += 9
                    continue

                #debug
                if "".join(LCHAR[POS:POS+5]) == "debug":
                    del LCHAR[POS:POS+5]
                    LCHAR.insert(POS, 'print(f"DEBUG LAYER CONSOLE: {locals()}")')
                    POS += len(print(f"DEBUG LAYER CONSOLE: {locals()}"))
                    continue

                #do (number): loop
                if "".join(LCHAR[POS:POS+2]) == "do":

                    iPOS = POS + 1
                    ifound = False
                    for i in LCHAR:
                        if i == ":" and ifound == False:
                            LCHAR.insert(iPOS-1, ")" )
                            ifound = True
                        iPOS += 1

                    del LCHAR[POS:POS+3]
                    LCHAR.insert(POS, "for i in range(")
                    POS += len("for i in range(")
                    continue

                #forever loop --> While True:
                if "".join(LCHAR[POS:POS+7]) == "forever":
                    del LCHAR[POS:POS+7]
                    LCHAR.insert(POS, "While True")
                    POS += 10
                    continue

                #fn/func/function --> def
                if "".join(LCHAR[POS:POS+2]) == "fn":
                    del LCHAR[POS:POS+2]

                if "".join(LCHAR[POS:POS+4]) == "func":
                    del LCHAR[POS:POS+4]

                if "".join(LCHAR[POS:POS+8]) == "function":
                    del LCHAR[POS:POS+8]

                    LCHAR.insert(POS, "def")
                    POS += 3
                    continue

                #printlist. prints a list
                if "".join(LCHAR[POS:POS+10]) == "printlist(":

                    iPOS = POS + 1
                    ifound = False
                    for i in LCHAR[iPOS:len(LCHAR)]:
                        if i == ")" and ifound == False:
                            LCHAR.insert(iPOS, ")" )
                            ifound = True
                        iPOS += 1

                    del LCHAR[POS:POS+10]
                    LCHAR.insert(POS, 'print("".join(')
                    POS += len('print("".join(')
                    continue

                #delay --> time.sleep if time is imported
                if "".join(LCHAR[POS:POS+5]) == "wait(":
                    if "time" in LIBS:
                        del LCHAR[POS:POS+5]
                        LCHAR.insert(POS, "time.sleep(")
                        POS += 11
                        continue

                    elif not "time" in LIBS:
                        print()
                        print("Opal1 Error:")
                        print("Missing Library: 'time'")
                        print(f"\033[31m{line}", end = "")
                        print("~" * len(line))
                        print("\033[0m")
                        return "fail"
                
            
                #stop --> sys.exit() halts the executing script entirely
                if "".join(LCHAR[POS:POS+4]) == "stop":
                    if "sys" in LIBS:
                        del LCHAR[POS:POS+4]
                        LCHAR.insert(POS, "sys.exit()")
                        POS += 8
                        continue

                    elif not "sys" in LIBS:
                        print()
                        print("Opal1 Error:")
                        print("Missing Library: 'sys'")
                        print(f"\033[31m{line}", end = "")
                        print("~" * len(line))
                        print("\033[0m")
                        return "fail"
                    
                #clear --> os.system('cls') clear terminal on windows
                if "".join(LCHAR[POS:POS+5]) == "clear":
                    if "sys" in LIBS:
                        if sys.platform == "win32":
                            del LCHAR[POS:POS+5]
                            LCHAR.insert(POS, "os.system('cls')")
                            POS += 8
                            continue

                        else:
                            print()
                            print("Opal1 Error:")
                            print("Platform Does not support os.system('cls')")
                            print("This can only be used on windows")
                            print(f"\033[31m{line}")
                            print("~" * len(line))
                            print("\033[0m")
                            return "fail"

                    elif not "sys" in LIBS:
                        print()
                        print("Opal1 Error:")
                        print("Missing Library: 'sys'")
                        print(f"\033[31m{line} ")
                        print("~" * len(line))
                        print("\033[0m")
                        return "fail"
                    
                #is_even --> % 2 == 0
                if "".join(LCHAR[POS:POS+7]) == "is_even":
                    del LCHAR[POS:POS+7]
                    LCHAR.insert(POS, "% 2 == 0")
                    POS += 8
                    continue

                #is_odd --> % 2 == 0
                if "".join(LCHAR[POS:POS+6]) == "is_odd":
                    del LCHAR[POS:POS+6]
                    LCHAR.insert(POS, "% 2 != 0")
                    POS += 8
                    continue       

                #.uppercase() --> .upper()
                if "".join(LCHAR[POS:POS+11]) == ".uppercase(":
                    del LCHAR[POS:POS+11]
                    LCHAR.insert(POS, ".upper()")
                    POS += 8
                    continue

                #.lowercase() --> .lower()
                if "".join(LCHAR[POS:POS+11]) == ".lowercase(":
                    del LCHAR[POS:POS+11]
                    LCHAR.insert(POS, ".lower()")
                    POS += 8
                    continue       

                #uppercase --> .upper()
                if "".join(LCHAR[POS:POS+13]) == " uppercase ":
                    del LCHAR[POS:POS+13]
                    LCHAR.insert(POS, ".upper() ")
                    POS += 9
                    continue

                #lowercase --> .lower()
                if "".join(LCHAR[POS:POS+13]) == " lowercase ":
                    del LCHAR[POS:POS+13]
                    LCHAR.insert(POS, ".lower() ")
                    POS += 9
                    continue


                #reversed --> [::-1] 
                if "".join(LCHAR[POS:POS+9]) == " reversed":
                    del LCHAR[POS:POS+9]
                    LCHAR.insert(POS, "[::-1]")
                    POS += 6
                    continue

                #resetvar -->  = ""
                if "".join(LCHAR[POS:POS+8]) == "resetvar":
                    del LCHAR[POS:POS+8]
                    LCHAR.insert(POS, ' = "" ')
                    POS += 6
                    continue

                #resetlist -->  = []
                if "".join(LCHAR[POS:POS+9]) == "resetlist":
                    del LCHAR[POS:POS+9]
                    LCHAR.insert(POS, ' = [] ')
                    POS += 6
                    continue
                    
            POS += 1
        GRID.append("".join(LCHAR))
    output = "".join(GRID)

    #Running the file
    exec(output, globals())



