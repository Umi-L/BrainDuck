pointer = 0
values = {}
output = ""
tLoop = 0

#compiler options
formatCode = True
byteValue = 8

def rollValue(value):
    maxValue = (2 ** byteValue) - 1
    while True:
        if value > maxValue:
            value = value - maxValue
        elif value < 0:
            value = maxValue + value
        else:
            return value

def simulateLoop(bfCode):
    global pointer

    running = True
    while running:
        for ch in bfCode:
            if ch == "+":
                values[pointer] += 1
            if ch == '-':
                values[pointer] += 1
            if ch == ',':
                print("!!! Inputs are not supported with static operations !!! Do not use SET !!!")
            if ch == ']':
                if values[pointer] == 0:
                    running = False
                    break
            if ch == '>':
                pointer += 1
            if ch == '<':
                pointer -= 1

def setValue(value):
    global output

    if pointer not in values:
        values[pointer] = 0

    # sets current value to 0
    output += "[-]"
    output += '+' * value

    values[pointer] = rollValue(values[pointer])

with open("test.bd", "r") as bdFile:
    bdCode = [line.replace("\n", "") for line in bdFile.readlines()]

for line in bdCode:
    params = line.split(" ")

    #basic instructions
    if params[0] == 'point':
        if params[1] == ">":
            times = 1
            if len(params) == 3:
                times = int(params[2])
            output += ">"*times
            pointer += times
            continue
        elif params[1] == "<":
            times = 1
            if len(params) == 3:
                times = int(params[2])
            output += "<"*times
            pointer -= times
            continue
        elif pointer < int(params[1]):
            output += ">" * (int(params[1]) - pointer)
        elif pointer > int(params[1]):
            output += '<' * (abs(int(params[1]) - pointer))

        pointer = int(params[1])

    elif params[0] == "add":
        output += "+" * int(params[1])

        if pointer not in values:
            values[pointer] = 0

        values[pointer] += int(params[1])
        values[pointer] = rollValue(values[pointer])
    elif params[0] == "sub":
        output += "-" * int(params[1])

        if pointer not in values:
            values[pointer] = 0

        values[pointer] -= int(params[1])
        values[pointer] = rollValue(values[pointer])
    elif params[0] == "set":
        if pointer not in values:
            values[pointer] = 0
        setValue(int(params[1]))

    #loops
    elif params[0] == 'loop':
        if len(params) == 2:
            output += '>'

            setValue(int(params[1]))

            output += '[-<'

            tLoop += 1
        else:
            output += '['
    elif params[0] == '/loop':
        if tLoop > 0:
            output += '>]'
            tLoop -= 1
        else:
            output += ']'

    #i/o
    elif params[0] == "input":
        output += ','

    elif params[0] == 'print':
        if len(params) == 1:
            output += '.'
        else:
            for ch in line[6:]:
                value = ord(ch)

                if ch == '\\':
                    value = 10

                setValue(value)
                output += '.'
                if formatCode == True:
                    output += '\n'


    #debug instructions
    elif params[0] == "bpoint":
        print({key: val for key, val in sorted(values.items())})
        exit()

    #Code formatting
    if formatCode == True:
        output += "\n"

with open("out.bf", "w") as out:
    out.write(output)
