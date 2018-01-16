
# coding: utf-8

# In[30]:

"""
Interpreter CLISP

Author: Gladkikh Anna, 4103
"""

name_table = []
def quote(args):
    result = ''
    for arg in args:
        if not isinstance(arg, int):
            result += name_table[int(arg)][2]
            result += ' '
        else:
            result += str(arg)
            result += ' '

    return '(' + result + ')'

def sum_lisp(args):
    result = 0
    for arg in args:
        if not isinstance(arg, int):
            result += int(name_table[int(arg)][2])
        else:
            result += arg
    return result
    
def sub_lisp(args):
    result = 0
    if not isinstance(args[0], int):
        result = int(name_table[int(args[0])][2])
    else:
        result = int(args[0])
    for arg in args[1:]:
        if not isinstance(arg, int):
            result -= int(name_table[int(arg)][2])
        else:
            result -= arg

    return result

def mul_lisp(args):
    result = 0
    if not isinstance(args[0], int):
        result = int(name_table[int(args[0])][2])
    else:
        result = int(args[0])
    for arg in args[1:]:
        if not isinstance(arg, int):
            result *= int(name_table[int(arg)][2])
        else:
            result *= arg

    return result

def div_lisp(args):
    result = 0
    if not isinstance(args[0], int):
        result = float(name_table[int(args[0])][2])
    else:
        result = int(args[0])
    for arg in args[1:]:
        if not isinstance(arg, int):
            result /= float(name_table[int(arg)][2])
        else:
            result /= arg

    return result

def car(args):
    result = ''
    if not isinstance(args[0], int):
        result = name_table[int(args[0])][2]
    else:
        result = args[0]
    
    return result

def cdr(args):
    result = ''
    for arg in args[1:]:
        if not isinstance(arg, int):
            result += name_table[int(arg)][2]
            result += ' '
        else:
            result += str(arg)
            result += ' '

    return '(' + result + ')'
    
    
key_words = {
    '-1': quote,
    '-4': sum_lisp,
    '-5': sub_lisp,
    '-6': mul_lisp,
    '-7': div_lisp,
    '-8': car,
    '-9': cdr,
    '-10': 'cons',
    '-11': 'atom',
    '-12': 'eq',
    '-13': 'listp',
    '-14': 'null',
    '-15': 'nil',
    '-16': 'T',
    '-21': 'first',
}

def evaluation(function, args):
    result = key_words[function](args)
    return result
    
def interpret(lex_stack):
    global stack, number
    for i in range(len(lex_stack)):
        if isinstance(lex_stack[i], list):
            if all(not isinstance(elem, list) for elem in lex_stack[i]):
                lex_stack[i].pop()
                print lex_stack[i]
                lex_stack[i] = evaluation(lex_stack[i][1], lex_stack[i][2:])
            else:
                interpret(lex_stack[i])
    
def main():
    #preprocessing files
    with open('lex_stack.txt', 'r') as lex:
        data = lex.read()
    lex.close()
    lex_stack = eval(data)
    lex_stack = filter(None, lex_stack)
	
    
    global name_table
    with open('name_table.txt', 'r') as name:
        sentences = [elem for elem in name.read().split('\n') if elem]
        for sentence in sentences:
            name_table.append(sentence.split())
    name.close()

    #interpretation
    while any(isinstance(elem, list) for elem in lex_stack):
        interpret(lex_stack)
    #print lex_stack[1]
    if len(lex_stack) >= 2 and int(lex_stack[1]) < 0:
        lex_stack.pop()
        lex_stack = evaluation(lex_stack[1], lex_stack[2:])
        print lex_stack
    else:
        for elem in lex_stack:
            if not isinstance(elem, int):
                print name_table[int(elem)][1]
            else:
                print elem


# In[ ]:

if __name__ == "__main__":
    main()

