def block(code):
    opened = []
    blocks = {}
    for i in range(len(code)):
        if code[i] == '[':
            opened.append(i)
        elif code[i] == ']':
            blocks[i] = opened[-1]
            blocks[opened.pop()] = i
    return blocks

def parse(code):
    return ''.join(c for c in code if c in '><+-.,[]')

def encode(data):
    glyphs = len(set([c for c in data]))
    number_of_bins = max(max([ord(c) for c in data]) // glyphs,1)
    bins = [(i + 1) * number_of_bins for i in range(glyphs)]
    code="+" * number_of_bins + "["
    code+="".join([">"+("+"*(i+1)) for i in range(1,glyphs)])
    code+="<"*(glyphs-1) + "-]"
    code+="+" * number_of_bins
    current_bin=0
    for char in data:
        new_bin=[abs(ord(char)-b)for b in bins].index(min([abs(ord(char)-b)for b in bins]))
        appending_character=""
        if new_bin-current_bin>0:
            appending_character=">"
        else:
            appending_character="<"
        code+=appending_character * abs(new_bin-current_bin)
        if ord(char)-bins[new_bin]>0:
            appending_character="+"
        else:
            appending_character="-"
        code+=(appending_character * abs( ord(char)-bins[new_bin])) +"."
        current_bin=new_bin
        bins[new_bin]=ord(char)
    return code

def run(code):
    code = parse(code)
    x = i = 0
    bf = {0: 0}
    blocks = block(code)
    l = len(code)
    r = ''
    while i < l:
        sym = code[i]
        if sym == '>':
            x += 1
            bf.setdefault(x, 0)
        elif sym == '<':
            x -= 1
        elif sym == '+':
            bf[x] += 1
        elif sym == '-':
            bf[x] -= 1
        elif sym == '.':
            #print(chr(bf[x]), end='')
            r += str(chr(bf[x]))
       # elif sym == ',':
      #      bf[x] = int(input('Input: '))
        elif sym == '[':
            if not bf[x]: i = blocks[i]
        elif sym == ']':
            if bf[x]: i = blocks[i]
        i += 1
    return r