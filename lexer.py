
# coding: utf-8

# In[29]:

"""
Scanner CLISP

Author: Gladkikh Anna, 4103
"""

import sys

def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False
    
key_words = {
    'quote': -1,
    '\'': -1,
    '(': -2,
    ')': -3,
    '+': -4,
    '-': -5,
    '*': -6,
    '/': -7,
    'car': -8,
    'cdr': -9,
    'cons': -10,
    'atom': -11,
    'eq': -12,
    'listp': -13,
    'null': -14,
    'nil': -15,
    'T': -16,
    'if': -17,
    'test': -18,
    'then': -19,
    'else': -20,
    'first': -21,
}

START = 'START'
ATOM = 'ATOM'
STR = 'STR'
COMMENT = 'COMMENT'
EXPRESSION = 'EXPRESSION'
NAME = 'NAME'
NUMBER = 'NUMBER'
END = 'END'

SRC = ''
lex_flow = []
#name_table = [['id', 'name', 'value', 'value_type']]
name_table = []
value = ''
brackets = 0

#add_bracket, add_value, save_value - transition functions
def add_bracket(c):
    global brackets
    if c == '(' or c == ')':
        brackets+=1
        
def add_value(c):
    global value
    value+=c

def save_value(c):
    global value
    if SRC == ATOM:
        lex_flow.append(len(name_table))
        name_table.append([len(name_table), value, value, 'atom'])
    elif SRC == STR:
        lex_flow.append(len(name_table))
        name_table.append([len(name_table), value, value, 'string']) 
    elif SRC == NUMBER or SRC == NAME:
        if isfloat(value):
            lex_flow.append(len(name_table))
            name_table.append([len(name_table), value, value, 'atom'])
        else:
            if value[0].isdigit():
                sys.exit('error name value!')
            if value in key_words:
                lex_flow.append(key_words[value])
            else:
                lex_flow.append(len(name_table))
                name_table.append([len(name_table), value, '-', '-'])
    else:
        if value == '(':
            lex_flow.append(key_words[value])
    value=''

def start_states(input_str):
    global SRC, lex_flow, name_table, brackets
    lex_flow = []
    name_table = []
    brackets = 0
    SRC = START
    for c in input_str:
        if SRC == END:
            break
        for rule in rule_set:
            if rule['src'] == SRC:
                if eval(rule['cond']):
                    if rule['action']:
                        if isinstance(rule['action'], list):
                            for act in rule['action']:
                                act(c)
                        else:
                            rule['action'](c)
                    SRC = rule['dst']
                    break    
                    
    if brackets%2 == 1:
        sys.exit('syntax brackets error!')
        
    return name_table, lex_flow       

rule_set = [
    { 'src': START, 'dst': START, 'cond': "c == ' ' or c == '\\n'", 'action': None },
    { 'src': START, 'dst': ATOM, 'cond': "c.isdigit()", 'action': add_value },
    { 'src': START, 'dst': STR, 'cond': "c == '\"'", 'action': add_value },
    { 'src': START, 'dst': COMMENT, 'cond': "c == ';'", 'action': None },
    { 'src': START, 'dst': EXPRESSION, 'cond': "c == '('", 'action': [add_value, save_value, add_bracket] },
    { 'src': ATOM, 'dst': ATOM, 'cond': "c.isdigit() or c == '.'", 'action': add_value },
    { 'src': ATOM, 'dst': END, 'cond': "c == '\\n'", 'action': save_value },
    { 'src': ATOM, 'dst': START, 'cond': "c == ' '", 'action': save_value },
    { 'src': COMMENT, 'dst': START, 'cond': "c == '\\n'", 'action': None },
    { 'src': COMMENT, 'dst': COMMENT, 'cond': "True", 'action': None },
    { 'src': STR, 'dst': START, 'cond': "c == '\"'", 'action': [add_value, save_value] },
    { 'src': STR, 'dst': STR, 'cond': "True", 'action': add_value },
    { 'src': EXPRESSION, 'dst': EXPRESSION, 'cond': "c == ' ' or c == '\\n'", 'action': None },   
    { 'src': EXPRESSION, 'dst': EXPRESSION, 'cond': "c == '(' or c == ')'", 'action': [add_bracket, add_value, save_value] },
    { 'src': EXPRESSION, 'dst': COMMENT, 'cond': "c == ';'", 'action': None },
    { 'src': EXPRESSION, 'dst': NAME, 'cond': "c.isalpha() or c == '+' or c == '-' or c =='\' or c == '*' or c == '%' or c == '_'", 'action': add_value },
    { 'src': EXPRESSION, 'dst': NUMBER, 'cond': "c.isdigit()", 'action': add_value },
    { 'src': NAME, 'dst': NAME, 'cond': "c.isalpha() or c.isdigit() or c == '_'", 'action': add_value },
    { 'src': NAME, 'dst': EXPRESSION, 'cond': "c == ' ' or c =='\\n'", 'action': save_value },
    { 'src': NUMBER, 'dst': NUMBER, 'cond': "c.isdigit() or c == '.'", 'action': add_value },
    { 'src': NUMBER, 'dst': EXPRESSION, 'cond': "c == '(' or c == ')'", 'action': [save_value, add_value, save_value, add_bracket] },
    { 'src': NUMBER, 'dst': EXPRESSION, 'cond': "c == ' ' or c =='\\n'", 'action': save_value },
    { 'src': EXPRESSION, 'dst': END, 'cond': "c == ')'", 'action': [add_value, save_value] },
    { 'src': END, 'dst': '', 'cond': "True", 'action': None },
]

def main():
    with open(sys.argv[1], 'r') as myfile:
        data=myfile.read()
    myfile.close()
    lex_flow = []
    name_table = []
    
    name_table, lex_flow = start_states(data)
    with open('name_table.txt', 'w') as t:
        for _list in name_table:
            for _string in _list:
                t.write(str(_string) + ' ')
            t.write('\n')
    t.close()
    l = open('lex_flow.txt', 'w')
    for item in lex_flow:
        l.write("%s " % item)
    l.close()
    


# In[38]:

if __name__ == "__main__":
    main()


# In[ ]:



