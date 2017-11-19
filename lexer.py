
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


# In[35]:

def main():
    with open(sys.argv[1], 'r') as myfile:
        data=myfile.read()
    myfile.close()
    lex_flow = []
    name_table = []
    name_table, lex_flow = get_tokens(data)
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


# In[39]:

def get_tokens(string):
    brackets = 0
    lex_flow = []
    name_table = []
    value = ''
    i = -1
    while i < len(string)-1:
        i+=1
        if i < len(string)-1:
            if string[i] == '|' and string[i+1] == '#':
                while True:
                    i+=1
                    if string[i] == '#' and string[i+1] == '|':
                        break
                continue
        if string[i] == '\n' or string[i] == ' ':
            if len(value) != 0:
                if isfloat(value):
                    lex_flow.append(len(name_table))
                    name_table.append([len(name_table), value, value, 'atom'])
                else:
                    if value[0].isdigit():
                        sys.exit('error name value!')
                        break
                    if value in key_words:
                        lex_flow.append(key_words[value])
                    else:
                        lex_flow.append(len(name_table))
                        name_table.append([len(name_table), value, '-', '-'])
                value = ''
            continue
        if string[i] == '(' or string[i] == ')':
            if len(value) != 0:
                if isfloat(value):
                    lex_flow.append(len(name_table))
                    name_table.append([len(name_table), value, value, 'integer'])        
                else:
                    if value[0].isdigit():
                        sys.exit('error name value!')
                        break
                    if value in key_words:
                        lex_flow.append(key_words[value])
                    else:
                        lex_flow.append(len(name_table))
                        name_table.append([len(name_table), value, '-', '-'])
                value = ''
            brackets+=1
        if string[i] == '\"':
            while True:
                value+=string[i]
                i+=1
                if string[i] == '\"':
                    value+=string[i]
                    lex_flow.append(len(name_table))
                    name_table.append([len(name_table), value, value, 'string'])
                    value = ''
                    break
            continue
        if string[i] == '.':
            if isfloat(value):
                value+=string[i]
        if string[i].isdigit():
            value+=string[i]
        if string[i].isalpha():
            value+=string[i]
        if string[i] in key_words:
            lex_flow.append(key_words[string[i]])
    
    if brackets%2 == 1:
        sys.exit('syntax brackets error!')
        
    return name_table, lex_flow 


# In[38]:

if __name__ == "__main__":
    main()


# In[ ]:



