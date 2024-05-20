import re

def is_identifier(text):
    """Checks if the text is a valid identifier using a regular expression."""
    pattern = r"^[a-zA-Z_][a-zA-Z0-9_]*$"
    return bool(re.match(pattern, text))

def is_int_literal(text):
    """Checks if the text is a valid integer literal using a regular expression."""
    pattern = r"^-?\d+$"
    return bool(re.match(pattern, text))

def is_float_literal(text):
    """Checks if the text is a valid float literal using a regular expression."""
    pattern = r"^-?\d+\.\d+$"
    return bool(re.match(pattern, text))

def is_boolean_literal(text):
    """Checks if the text is a valid boolean literal ('True' or 'False')."""
    return text.lower() in ("true", "false")

def varmap(targetVar, state):
    """Searches for a variable in the state and returns its value, raising an error if not found."""
    if targetVar in state:
        return state[targetVar]
    else:
        raise ValueError("Error: Variable not found")

def test_regular_expressions():
    # Test identifier regular expression
    assert is_identifier("variable") == True
    assert is_identifier("Variable") == True
    assert is_identifier("_variable") == True
    assert is_identifier("var123") == True
    assert is_identifier("123var") == False  # Should not start with a digit
    assert is_identifier("var-123") == False  # Should not contain special characters other than underscore

    # Test integer literal regular expression
    assert is_int_literal("123") == True
    assert is_int_literal("-123") == True
    assert is_int_literal("0") == True
    assert is_int_literal("123.0") == False  # Should not contain a decimal point

    # Test float literal regular expression
    assert is_float_literal("123.456") == True
    assert is_float_literal("-123.456") == True
    assert is_float_literal("0.0") == True
    assert is_float_literal("123") == False  # Should contain a decimal point

    # Test boolean literal
    assert is_boolean_literal("True") == True
    assert is_boolean_literal("False") == True
    assert is_boolean_literal("true") == True  # Expected to be True (case-insensitive)

    print("All regular expression tests passed successfully.")


def executeProgram(program):
    state = dict()
    lines = program.splitlines()

    for linenum, line in enumerate(lines):
        if len(line.split()) == 0:
            continue # Skip blank lines
        instruction, expression = line.split(maxsplit=1)

        if instruction == "SHIFT":
            var, val = expression.split('=')
            if not is_identifier(var):
                print(f"Error: Invalid identifier '{var}' in assignment.")
                continue
            if is_identifier(val):
                val = varmap(val, state)
            state[var] = val
        elif instruction == "WINDSHIELD":
            if "'" in expression:
                printed_string = expression.replace("'", "")
                print(printed_string)
                continue
            try:
                val = varmap(expression.strip(), state)
                print(val)
            except:
                print("Error: Val not found")
        elif instruction == "AXLE":
            var, myRange = expression.split("=")
            expression = expression.replace(":","")
            start_val, stop_val = myRange.split(",")
            state[var] = start_val
            for i in range(linenum+1, len(lines)):
                scanLine = lines[i]
                if "NEXT" in scanLine:
                    stop_line = i
                    for_body = lines[linenum+1:stop_line]
                    for x in range(int(start_val), int(stop_val)+1):
                        state[var] = x
                        newProgram = "".join(for_body)
                        executeProgram(newProgram)
                    break
        elif instruction == "NEXT":
            continue
        elif instruction == "DRIVER":
            conditions = expression.split("ELIF")  # Split the expression based on "ELIF"
            for condition in conditions:
                if "ELSE" in condition:
                    condition, else_block = condition.split("ELSE")


# Test the interpreter with a sample program
sampleProgram = """ASSIGN X=4
ASSIGN Y=5
PRINT X
PRINT Y
PRINT X
PRINT Z
ASSIGN Z=10
ASSIGN _=Hello World
Woo hoo!
PRINT X
PRINT Z
PRINT _
"""

for_loop = """
FOR I=1,100:
PRINT I
NEXT I
"""

while_loop = """
"""

factorial = """
ASSIGN x=10
IF x == 10:
    PRINT x
ELIF x == 20:
    PRINT x
ELSE:
    PRINT x
ENDIF
"""

print_vars = """ASSIGN I=3
PRINT I
"""

print_words = """PRINT 'FIZZ'
PRINT 'BUZZ'
"""

prints = print_vars + print_words


label_and_jump = """
ASSIGN i = 0
i++
Label1:
PRINT i
JUMP Label1
"""

sampleProgram1 = """
SHIFT X=10
SHIFT Y=20
WINDSHIELD 'Value of X:'
WINDSHIELD X
WINDSHIELD 'Value of Y:'
WINDSHIELD Y
"""

executeProgram(sampleProgram1)

Hello_World = """
SHIFT X=Hello World!
WINDSHIELD X
"""

executeProgram(Hello_World)



#executeProgram(factorial)
#test_regular_expressions()
