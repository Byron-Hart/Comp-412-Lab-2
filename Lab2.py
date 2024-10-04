import math
import sys

class IRnode:
    def __init__(self, data):
        global lineNum
        self.data = data
        self.next = None
        self.prev = None
        self.lineNum = lineNum
    
    def __str__(self):
        printIR(self)
        return ""

def insertIR(data):
    global irHead
    
    node = IRnode(data)
    
    if irHead == None:
        irHead = node
        irHead.next = irHead
        irHead.prev = irHead
    else:
        headPrev = irHead.prev
        headPrev.next = node
        node.prev = headPrev
        irHead.prev = node
        node.next = irHead
        
def scan():
    global line, lineNum, charNum, nextline
    #Check for EOF
    if len(line) == 0:
        return ((9, 0))

    c = line[charNum]

    #Get rid of whitespace
    if c == " " or c == "\t":
        charNum += 1
        c = line[charNum]
        while c == " " or c == "\t":
            charNum += 1   
            c = line[charNum]

    #Check for comment
    if c == "/":
        charNum += 1
        c = line[charNum]
        if c == "/":
            charNum += 1
            c = line[charNum]
            if line[-1] == "\n":
                return((10, 0))
            else:
                return((9, 0))
        else:
            return print_lexical_error(lineNum, "Invalid ILOC. / not followed by /.")

    #Check for load, loadI, lshift
    elif c == "l":
        charNum += 1
        c = line[charNum]
        if c == "o":
            charNum += 1
            c = line[charNum]
            if c == "a":
                charNum += 1
                c = line[charNum]
                if c == "d":
                    charNum += 1
                    c = line[charNum]
                    if c == "I":
                        charNum += 1
                        return((1, 0))
                    else:
                        return((0, 0))
                else:
                    return print_lexical_error(lineNum, "Invalid ILOC. loa not followed by d or dI.")                
            else:
                return print_lexical_error(lineNum, "Invalid ILOC. lo not followed by a.")                
        elif c == "s":
            charNum += 1
            c = line[charNum]
            if c == "h":
                charNum += 1
                c = line[charNum]
                if c == "i":
                    charNum += 1
                    c = line[charNum]
                    if c == "f":
                        charNum += 1
                        c = line[charNum]
                        if c == "t":
                            charNum += 1
                            return((2, 3))
                        else:
                            return print_lexical_error(lineNum, "Invalid ILOC. lshif not followed by t.")                
                    else:
                        return print_lexical_error(lineNum, "Invalid ILOC. lshi not followed by f.")                
                else:
                    return print_lexical_error(lineNum, "Invalid ILOC. lsh not followed by i.")                
            else:
                return print_lexical_error(lineNum, "Invalid ILOC. ls not followed by h.")
        else:
            return print_lexical_error(lineNum, "Invalid ILOC. l not followed by o or s.")


    #Check for store, sub
    elif c == "s":
        charNum += 1
        c = line[charNum]
        if c == "u":
            charNum += 1
            c = line[charNum]
            if c == "b":
                charNum += 1
                return((2, 1))
            else:
                return print_lexical_error(lineNum, "Invalid ILOC. su not followed by b.")                
        elif c == "t":
            charNum += 1
            c = line[charNum]
            if c == "o":
                charNum += 1
                c = line[charNum]
                if c == "r":
                    charNum += 1
                    c = line[charNum]
                    if c == "e":
                        charNum += 1
                        return((0, 1))
                    else:
                        return print_lexical_error(lineNum, "Invalid ILOC. stor not followed by e.")                
                else:
                    return print_lexical_error(lineNum, "Invalid ILOC. sto not followed by r.")                
            else:
                return print_lexical_error(lineNum, "Invalid ILOC. st not followed by o.")
        else:
            return print_lexical_error(lineNum, "Invalid ILOC. s not followed by u or t.")

    #Check for add
    elif c == "a":
        charNum += 1
        c = line[charNum]
        if c == "d":
            charNum += 1
            c = line[charNum]
            if c == "d":
                charNum += 1
                return((2, 0))
            else:
                return print_lexical_error(lineNum, "Invalid ILOC. ad not followed by d.")                
        else:
            return print_lexical_error(lineNum, "Invalid ILOC. a not followed by d.")

    #Check for mult
    elif c == "m":
        charNum += 1
        c = line[charNum]
        if c == "u":
            charNum += 1
            c = line[charNum]
            if c == "l":
                charNum += 1
                c = line[charNum]
                if c == "t":
                    charNum += 1
                    return((2, 2))
                else:
                    return print_lexical_error(lineNum, "Invalid ILOC. mul not followed by t.")                
            else:
                return print_lexical_error(lineNum, "Invalid ILOC. mu not followed by l.")                
        else:
            return print_lexical_error(lineNum, "Invalid ILOC. m not followed by u.")
    
    #Check for rshift or register
    elif c == "r":
        charNum += 1
        c = line[charNum]
        if c == "s":
            charNum += 1
            c = line[charNum]
            if c == "h":
                charNum += 1
                c = line[charNum]
                if c == "i":
                    charNum += 1
                    c = line[charNum]
                    if c == "f":
                        charNum += 1
                        c = line[charNum]
                        if c == "t":
                            charNum += 1
                            return ((2,4))
                        else:
                            return print_lexical_error(lineNum, "Invalid ILOC. rshif not followed by t.") 
                    else:
                        return print_lexical_error(lineNum, "Invalid ILOC. rshi not followed by f.")                
                else:
                    return print_lexical_error(lineNum, "Invalid ILOC. rsh not followed by i.")                
            else:
                return print_lexical_error(lineNum, "Invalid ILOC. rs not followed by h.")                
        elif c >= "0" and c <= "9":
            n = int(c)
            charNum += 1
            c = line[charNum]
            while c >= "0" and c <= "9":
                n = n * 10 + int(c)
                charNum += 1
                c = line[charNum]
            return ((6, n))
        else:
            return print_lexical_error(lineNum, "Invalid ILOC. r not followed by s or constant.")                
    
    #Check for output
    elif c == "o":
        charNum += 1
        c = line[charNum]
        if c == "u":
            charNum += 1
            c = line[charNum]
            if c == "t":
                charNum += 1
                c = line[charNum]
                if c == "p":
                    charNum += 1
                    c = line[charNum]
                    if c == "u":
                        charNum += 1
                        c = line[charNum]
                        if c == "t":
                            charNum += 1
                            return ((3,0))
                        else:
                            return print_lexical_error(lineNum, "Invalid ILOC. outpu not followed by t.") 
                    else:
                        return print_lexical_error(lineNum, "Invalid ILOC. outp not followed by u.")                
                else:
                    return print_lexical_error(lineNum, "Invalid ILOC. out not followed by p.")                
            else:
                return print_lexical_error(lineNum, "Invalid ILOC. ou not followed by t.")                
        else:
            return print_lexical_error(lineNum, "Invalid ILOC. o not followed by u.")                


    #Check for nop
    elif c == "n":
        charNum += 1
        c = line[charNum]
        if c == "o":
            charNum += 1
            c = line[charNum]
            if c == "p":
                charNum += 1
                return((4, 0))
            else:
                return print_lexical_error(lineNum, "Invalid ILOC. no not followed by p.")                
        else:
            return print_lexical_error(lineNum, "Invalid ILOC. n not followed by o.")
        
    #Check for constant
    elif c >= "0" and c <= "9":
        n = int(c)
        charNum += 1
        c = line[charNum]
        while c >= "0" and c <= "9":
            n = n * 10 + int(c)
            charNum += 1
            c = line[charNum]
        return ((5, n))

    #Check for comma
    elif c == ",":
        charNum += 1
        return((7, 0))
    
    #Check for =>
    elif c == "=":
        charNum += 1
        c = line[charNum]
        if c == ">":
            charNum += 1
            return((8, 0))
        else:
            return print_lexical_error(lineNum, "Invalid ILOC. = not followed by >.")
    
    #Check for EOL
    elif c == "\n":
        return((10, 0))
    elif c == "\r":
        charNum += 1
        if c == "\n":
            return((10, 0))
        else:
            return print_lexical_error(lineNum, "Invalid ILOC. \r not followed by \n.")

    else:
        return print_lexical_error(lineNum, "Text is not detectable ILOC.")

def getNextToken():
    global ilocFile, lineNum, charNum, line, fakeEOL
    token = scan()
    if token[0] == 10 and fakeEOL:
        return((9, 0))
    if token[0] == 10 or token[0] == 11:
        line = ilocFile.readline()
        lineNum += 1
        charNum = 0
        if len(line) != 0 and line[-1] != "\n":
            line = line + "\n"
            fakeEOL = True
    return token
    
def parse():
    global lineNum, operations
    token = 0
    while token != (9, 0):
        token = getNextToken()
        data = [token, None, None, None, None, None, None, None, None, None, None, None, None]
        #MEMOP, REG, INTO, REG, EOL
        if token[0] == 0:
            token = getNextToken()
            if token[0] == 6:
                data[1] = token[1]
                token = getNextToken()
                if token[0] == 8:
                    token = getNextToken()
                    if token[0] == 6:
                        data[9] = token[1]
                        token = getNextToken()
                        if token[0] == 10:
                            operations += 1
                            insertIR(data)
                        elif token[0] != 11:
                            print_syntax_error(lineNum, "MEMOP REG INTO REG not followed by EOL.")
                    elif token[0] != 11:
                        print_syntax_error(lineNum, "MEMOP REG INTO not followed by REG.")
                elif token[0] != 11:
                    print_syntax_error(lineNum, "MEMOP REG not followed by INTO.")
            elif token[0] != 11:
                print_syntax_error(lineNum, "MEMOP not followed by REG.")

        #LOADI, CONSTANT, INTO, REG, EOL
        elif token[0] == 1:
            token = getNextToken()
            if token[0] == 5:
                data[1] = token[1]
                token = getNextToken()
                if token[0] == 8:
                    token = getNextToken()
                    if token[0] == 6:
                        data[9] = token[1]
                        token = getNextToken()
                        if token[0] == 10:
                            operations += 1
                            insertIR(data)
                        elif token[0] != 11:
                            print_syntax_error(lineNum, "LOADI CONSTANT INTO REG not followed by EOL.")
                    elif token[0] != 11:
                        print_syntax_error(lineNum, "LOADI CONSTANT INTO not followed by REG.")
                elif token[0] != 11:
                    print_syntax_error(lineNum, "LOADI CONSTANT not followed by INTO.")
            elif token[0] != 11:
                print_syntax_error(lineNum, "LOADI not followed by CONSTANT.")

        #ARITHOP, REG, COMMA, REG, INTO, REG, EOL
        elif token[0] == 2:
            token = getNextToken()
            if token[0] == 6:
                data[1] = token[1]
                token = getNextToken()
                if token[0] == 7:
                    token = getNextToken()
                    if token[0] == 6:
                        data[5] = token[1]
                        token = getNextToken()
                        if token[0] == 8:
                            token = getNextToken()
                            if token[0] == 6:
                                data[9] = token[1]
                                token = getNextToken()
                                if token[0] == 10:
                                    operations += 1
                                    insertIR(data)
                                elif token[0] != 11:
                                    print_syntax_error(lineNum, "ARITHOP REG COMMA REG INTO REG not followed by EOL.")
                            elif token[0] != 11:
                                print_syntax_error(lineNum, "ARITHOP REG COMMA REG INTO not followed by REG.")
                        elif token[0] != 11:
                            print_syntax_error(lineNum, "ARITHOP REG COMMA REG not followed by INTO.")
                    elif token[0] != 11:
                        print_syntax_error(lineNum, "ARITHOP REG COMMA not followed by REG.")
                elif token[0] != 11:
                    print_syntax_error(lineNum, "ARITHOP REG not followed by COMMA.")
            elif token[0] != 11:
                print_syntax_error(lineNum, "ARITHOP not followed by REG.")

        #OUTPUT, CONSTANT, EOL
        elif token[0] == 3:
            token = getNextToken()
            if token[0] == 5:
                data[1] = token[1]
                token = getNextToken()
                if token[0] == 10:
                    operations += 1
                    insertIR(data)
                elif token[0] != 11:
                    print_syntax_error(lineNum, "OUTPUT CONSTANT not followed by EOL.")
            elif token[0] != 11:
                print_syntax_error(lineNum, "OUTPUT not followed by CONSTANT.")

        #NOP, EOL
        elif token[0] == 4:
            token = getNextToken()
            if token[0] == 10:
                operations += 1
                insertIR(data)
            elif token[0] != 11:
                print_syntax_error(lineNum, "NOP not followed by EOL.")

        #EOF
        elif token[0] == 9:
            insertIR(data)

        #EOL, EOF, or ERROR
        elif token[0] == 10 or token[0] == 11:
            continue

        else:
            print_syntax_error(lineNum, "Sentence start is not MEMOP, LOADI, ARITHOP, OUTPUT, NOP, or EOF.")

def printIR(data):
    if data[0][0] == 0:  
        if data[0][1] == 0:
            print("LOAD r%i INTO r%i" % (data[1], data[9]))
        else:
            print("STORE r%i INTO r%i" % (data[1], data[9]))
    elif data[0][0] == 1:  
        print("LOADI %i INTO r%i" % (data[1], data[9]))
    elif data[0][0] == 2:          
        if data[0][1] == 0:  
            print("ADD r%i , r%i INTO r%i" % (data[1], data[5], data[9]))
        elif data[0][1] == 1:        
            print("SUB r%i , r%i INTO r%i" % (data[1], data[5], data[9]))
        elif data[0][1] == 2:        
            print("MULT r%i , r%i INTO r%i" % (data[1], data[5], data[9]))
        elif data[0][1] == 3:        
            print("LSHIFT r%i , r%i INTO r%i" % (data[1], data[5], data[9]))
        else:        
            print("RSHIFT r%i , r%i INTO r%i" % (data[1], data[5], data[9]))
    elif data[0][0] == 3:
        print("OUTPUT %i" % data[1])          
    elif data[0][0] == 4:
        print("NOP")          
    else:
        print("EOF")

def rename():
    maxRegister = 0
    idx = 0 
    
    currNode = irHead
    while currNode.data[0][0] != 9:
        idx += 1
        if currNode.data[1] and currNode.data[1] > maxRegister:
            maxRegister = currNode.data[1]
        if currNode.data[5] and currNode.data[5] > maxRegister:
            maxRegister = currNode.data[5]
        if currNode.data[9] and currNode.data[9] > maxRegister:
            maxRegister = currNode.data[9]
        currNode = currNode.next
    
    SRtoVR = [None] * (maxRegister + 1)
    LU = [math.inf] * (maxRegister + 1)
    VRName = 0
        
    currNode = irHead.prev.prev
    while currNode.data[0][0] != 9:
        #Load
        if currNode.data[0] == (0,1):
            if not SRtoVR[currNode.data[1]]:
                SRtoVR[currNode.data[1]] = VRName
                VRName += 1
            currNode.data[2] = SRtoVR[currNode.data[1]]
            currNode.data[4] = LU[currNode.data[1]]

            SRtoVR[currNode.data[1]] = None
            LU[currNode.data[1]] = math.inf
                            
            if not SRtoVR[currNode.data[9]]:
                SRtoVR[currNode.data[9]] = VRName
                VRName += 1
            currNode.data[10] = SRtoVR[currNode.data[9]]
            currNode.data[12] = LU[currNode.data[9]]
            
            LU[currNode.data[9]] = idx

        #Store
        if currNode.data[0] == (0,1):
            if not SRtoVR[currNode.data[1]]:
                SRtoVR[currNode.data[1]] = VRName
                VRName += 1
            currNode.data[2] = SRtoVR[currNode.data[1]]
            currNode.data[4] = LU[currNode.data[1]]

            if not SRtoVR[currNode.data[9]]:
                SRtoVR[currNode.data[9]] = VRName
                VRName += 1
            currNode.data[10] = SRtoVR[currNode.data[9]]
            currNode.data[12] = LU[currNode.data[9]]
            
            LU[currNode.data[1]] = idx
            LU[currNode.data[9]] = idx

        #LoadI
        if currNode.data[0][0] == 1:
            if not SRtoVR[currNode.data[9]]:
                SRtoVR[currNode.data[9]] = VRName
                VRName += 1
            currNode.data[10] = SRtoVR[currNode.data[9]]
            currNode.data[12] = LU[currNode.data[9]]
            
            LU[currNode.data[9]] = idx

        #Arithop
        if currNode.data[0][0] == 2:          
            if not SRtoVR[currNode.data[1]]:
                SRtoVR[currNode.data[1]] = VRName
                VRName += 1
            currNode.data[2] = SRtoVR[currNode.data[1]]
            currNode.data[4] = LU[currNode.data[1]]

            SRtoVR[currNode.data[1]] = None
            LU[currNode.data[1]] = math.inf
            
            if not SRtoVR[currNode.data[5]]:
                SRtoVR[currNode.data[5]] = VRName
                VRName += 1
            currNode.data[6] = SRtoVR[currNode.data[5]]
            currNode.data[8] = LU[currNode.data[5]]
            
            SRtoVR[currNode.data[5]] = None
            LU[currNode.data[5]] = math.inf
                
            if not SRtoVR[currNode.data[9]]:
                SRtoVR[currNode.data[9]] = VRName
                VRName += 1
            currNode.data[10] = SRtoVR[currNode.data[9]]
            currNode.data[12] = LU[currNode.data[9]]
            
            LU[currNode.data[9]] = idx
            
        idx -= 1
        currNode = currNode.next


            
    
def xmode():
    global irHead, success
    parse()
    rename()
    
    if success:
        curr = irHead
        while curr.data[0][0] != 9:
            print(curr.data)
            curr = curr.next
        print(curr.data)
    else:
        print_error("Since there were errors in the input file, IR is not printed.")
        
def kmode():
    global success, operations
    parse()
    
    if success:
        print_error("Parse succeeded. Processed %i operations." % operations)
    else:
        print_error("Parse found errors.")

def print_error(*args):
     print(*args, file=sys.stderr)

def print_lexical_error(lineNumber, message):
    global success
    success = False
    print_error(("ERROR %i: " % lineNumber) + message)
    return ((11, 0))
    
def print_syntax_error(lineNumber, message):
    global line, charNum, lineNum, fakeEOL, success
    success = False
    if charNum == 0:
        print_error(("ERROR %i: " % (lineNumber-1)) + message)
    else:
        print_error(("ERROR %i: " % lineNumber) + message)
    line = ilocFile.readline()
    lineNum += 1
    charNum = 0
    if len(line) != 0 and line[-1] != "\n":
        line = line + "\n"
        fakeEOL = True


def initializeFile(ilocFilePath):
    global line, lineNum, nextline, ilocFile
    try:
        ilocFile = open(ilocFilePath, 'r')
        line = ilocFile.readline()
        lineNum = lineNum + 1;
        return True
    except:
        print_error("ERROR: The argument following the -x flag or k constant is not a valid filepath.")
        print(helpstring)
        return False

#OpCode=0, SR1=1,  VR1=2,  PR1=3,  NU1=4,  SR2,  VR2,  PR2,  NU2,  SR3,  VR3,  PR3,  NU3 
irHead = None
ilocFile = ""
lineNum = 0
charNum = 0
line = ""
fakeEOL = False
operations = 0
hflag, xflag = (False,)*2
lastArg = len(sys.argv) - 1
success = True
helpstring = """Command Line Options for 412alloc:
-h: Prints a list of valid command line arguments with descriptions of the function of each option.\n
-x <name>, where <name> is a valid filepath: If <name> leads to valid ILOC, performs register renaming and prints the result to standard output.\n
k <name>, where 3<=k<=64 and <name> is a valid filepath: If <name> leads to valid ILOC, allocates input to k registers and printsthe result to standard output.\n"""

#           MEMOP=0, LOADI=1, ARITHOP=2, OUTPUT=3, NOP=4, CONSTANT=5, REGISTER=6, COMMA=7, INTO=8, EOF=9, EOL=10, ERROR=11
ilocPOS = ("MEMOP", "LOADI", "ARITHOP", "OUTPUT", "NOP", "CONSTANT", "REGISTER", "COMMA", "INTO", "EOF", "EOL",  "ERROR")
#           load=0, store=1
memopPOS = ("load", "store")
#              add=0, sub=1, mult=2, lshift=3, rshift=4
arithopPOS = ("add", "sub", "mult", "lshift", "rshift")

if "-h" in sys.argv:
    hflag = True
if "-x" in sys.argv:
    xflag = True
    xloc = sys.argv.index("-x")
    
if hflag:
    if xflag:
        print_error("ERROR: Only one command line flag may be used at a time. Implementing highest present priority flag, -h.")
    print(helpstring)
elif xflag:
    if xloc == lastArg:
        print_error("ERROR: -x flags must be proceeded by a filepath.")
        print(helpstring)
    else:
        if initializeFile(sys.argv[xloc+1]):
            xmode()
else:
    if lastArg != 2:
        print_error("ERROR: When no flags are selected, 2 arguments are required, a constant 3<=k<=64, and a filepath.")
        print(helpstring)  
    try:
        if int(sys.argv[1]) < 3 or int(sys.argv[1]) > 64:
            print_error("ERROR: The number of physical registers must be 3<=k<=64.")    
    except:
        print_error("ERROR: If using no flags, the first argument must be an integer of value 3<=k<=64.")
    else:
        if initializeFile(sys.argv[2]):
            kmode(int(sys.argx[1]))