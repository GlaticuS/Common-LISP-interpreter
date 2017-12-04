
# coding: utf-8

# In[31]:

import sys


# In[33]:

"""
Scanner CLISP
Comments are |# #|

Author: Gladkikh Anna, 4103
"""


# In[34]:

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
#name_table = [['id', 'name', 'value', 'value_type']]


# In[3]:

from string import upper
class StateMachine:
    def __init__(self):
        self.handlers = {}
        self.startState = None
        self.endStates = []
 
    def add_state(self, name, handler, end_state=0):
        name = upper(name)
        self.handlers[name] = handler
        if end_state:
            self.endStates.append(name)
 
    def set_start(self, name):
        self.startState = upper(name)
 
    def run(self, cargo):
        try:
            handler = self.handlers[self.startState]
        except:
            raise "InitializationError", "must call .set_start() before .run()"
       
        if not self.endStates:
            raise  "InitializationError", "at least one state must be an end_state"
       
        while 1:
            (newState, cargo) = handler(cargo)
            if upper(newState) in self.endStates:
                break
            else:
                handler = self.handlers[upper(newState)]


# In[5]:

def start_state(string):
    global i
    i = -1
    nextState = "NEXT"
    return (nextState, string)
            
def next_state(string):
    global i
    if i < len(string) -1:
        i+=1
        if i < len(string)-1:
            if string[i] == '|' and string[i+1] == '#':
                nextState = "COMMENT"
        if string[i] == '\n' or string[i] == ' ':
            nextState = "FINISH"
        if string[i] == '(' or string[i] == ')':
            nextState = "BRACKET"
        if string[i] == '\"':
            nextState = "STRING"
        if string[i] == '.':
            nextState = "ATOM"
        if string[i].isdigit():
            nextState = "ATOM"
        if string[i].isalpha():
            nextState = "NAME"
        if string[i] in key_words:
            nextState = "KEYWORD"
    else:
        nextState = "END"
    return (nextState, string)
            
def comment_state(string):
    global i
    print "COMMENT state",
    if i < len(string)-1:
        if string[i] == '|' and string[i+1] == '#':
            while True:
                i+=1
                if string[i] == '#' and string[i+1] == '|':
                    break
    newState = "NEXT"
    return (newState, string)

def end_val(string):
    pass

def atom_state(string):
    pass

def error_state(string):
    pass

def keyword_state(string):
    pass

def name_state(string):
    pass

def string_state(string):
    pass


# In[6]:

def main():
    with open(sys.argv[1], 'r') as myfile:
        data=myfile.read()
    myfile.close()
    lex_flow = []
    name_table = []
    m = StateMachine()
    m.add_state("START", start_state)
    m.add_state("NEXT", next_state)
    m.add_state("FINISH", end_val)
    m.add_state("END", None, end_state = 1)
    m.add_state("COMMENT", comment_state)
    m.add_state("ATOM", atom_state)
    m.add_state("ERROR", error_state)
    m.add_state("KEYWORD", keyword_state)
    m.add_state("NAME", name_state)
    m.add_state("STRING", string_state)
    m.set_start("START")
    m.run(data)
    
    #name_table, lex_flow = get_tokens(data)
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


# In[36]:

def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


# In[7]:

"""def get_tokens(string):
    brackets = 0
    lex_flow = []
    name_table = []
    value = ''
    i = -1
    while i < len(string)-1:
        i+=1
        #STATE COMMENT
        if i < len(string)-1:
            if string[i] == '|' and string[i+1] == '#':
                while True:
                    i+=1
                    if string[i] == '#' and string[i+1] == '|':
                        break
                continue
        #END STATE
        if string[i] == '\n' or string[i] == ' ':
            if len(value) != 0:
                #STATE ATOM
                if isfloat(value):
                    lex_flow.append(len(name_table))
                    name_table.append([len(name_table), value, value, 'atom'])
                else:
                    if value[0].isdigit():
                        #STATE ERROR
                        sys.exit('error name value!')
                        break
                    if value in key_words:
                        #STATE KEY WORD
                        lex_flow.append(key_words[value])
                    else:
                        #STATE NAME
                        lex_flow.append(len(name_table))
                        name_table.append([len(name_table), value, '-', '-'])
                #CLEAR
                value = ''
            continue
        if string[i] == '(' or string[i] == ')':
            #STATE BRACKET
            if len(value) != 0:
                #STATE ATOM
                if isfloat(value):
                    lex_flow.append(len(name_table))
                    name_table.append([len(name_table), value, value, 'integer'])        
                else:
                    if value[0].isdigit():
                        #STATE ERROR
                        sys.exit('error name value!')
                        break
                    if value in key_words:
                        #STATE KEY WORD
                        lex_flow.append(key_words[value])
                    else:
                        #STATE NAME
                        lex_flow.append(len(name_table))
                        name_table.append([len(name_table), value, '-', '-'])
                #CLR
                value = ''
            #BR++
            brackets+=1
        if string[i] == '\"':
            #STATE STRING
            while True:
                value+=string[i]
                i+=1
                if string[i] == '\"':
                    value+=string[i]
                    #STATE NAME
                    lex_flow.append(len(name_table))
                    name_table.append([len(name_table), value, value, 'string'])
                    value = ''
                    break
            continue
        if string[i] == '.':
            if isfloat(value):
                #STATE ATOM
                value+=string[i]
        if string[i].isdigit():
            #STATE ATOM
            value+=string[i]
        if string[i].isalpha():
            #STATE NAME
            value+=string[i]
        if string[i] in key_words:
            #STATE KEYWORD
            lex_flow.append(key_words[string[i]])
    
    if brackets%2 == 1:
        
        sys.exit('syntax brackets error!')
        
    return name_table, lex_flow 
"""


# In[38]:

if __name__ == "__main__":
    main()


# In[ ]:



