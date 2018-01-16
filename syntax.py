
# coding: utf-8

# In[9]:

"""
Syntax analyser CLISP

Author: Gladkikh Anna, 4103

s_expression = atomic_symbol \
              / "(" s_expression "."s_expression ")" \
              / list 

list = "(" s_expression < s_expression > ")"

atomic_symbol = letter atom_part

atom_part = empty / letter atom_part / number atom_part

letter = "a" / "b" / " ..." / "z"

number = "1" / "2" / " ..." / "9"

empty = " "
"""

S_EXPRESSION = 'S_EXPRESSION'
ATOMIC_SYMBOL = 'ATOMIC_SYMBOL'
LIST = 'LIST'
ATOM_PART = 'ATOM_PART'
#LETTER = 'LETTER'
#NUMBER = 'NUMBER'
#EMPTY = 'EMPTY'
SYMBOL = 'SYMBOL'
KEYWORD = 'KEYWORD'
#BRACKET = 'BRACKET'

"""rule_set = [
    {'src': S_EXPRESSION, 'dst': ATOMIC_SYMBOL, 'rule':'', 'cond':''},
    #{'src': S_EXPRESSION, 'dst': '\''+KEYWORD + S_EXPRESSION + '.' + S_EXPRESSION + KEYWORD+'\'', 'rule':'', 'cond':''},
    {'src': S_EXPRESSION, 'dst': LIST, 'rule':'', 'cond':'brackets//2==0'},
    {'src': S_EXPRESSION, 'dst': '-2'+KEYWORD+S_EXPRESSION+S_EXPRESSION+'-3'},
    {'src': LIST, 'dst': '-2' + S_EXPRESSION + '-3', 'rule':'', 'cond':''},
    {'src':LIST, 'dst': '-2'+KEYWORD+S_EXPRESSION+'-3', 'rule':'', 'cond':''},
    #{'src':LIST, 'dst': '-2'+KEYWORD+S_EXPRESSION+SYMBOL+'-3', 'rule':'', 'cond':''},
    {'src': ATOMIC_SYMBOL, 'dst': KEYWORD + ATOM_PART, 'rule':'', 'cond':''},
    #{'src': ATOM_PART, 'dst': EMPTY, 'rule':'', 'cond':''},
    {'src': ATOM_PART, 'dst': '-2' + KEYWORD +ATOM_PART + '-3', 'rule':'', 'cond':''},
    {'src': ATOM_PART, 'dst': SYMBOL + SYMBOL , 'rule':'', 'cond':''},
   # {'src': ATOM_PART, 'dst': SYMBOL, 'rule':'', 'cond':''}
    #{'src': LETTER, 'dst':'token <= 0' , 'rule':'', 'cond':''},
    #{'src': NUMBER, 'dst': '', 'rule':'', 'cond':''},
   # {'src': SYMBOL, 'dst': SYMBOL, 'cond':''},
   # {'src': ATOM_PART, 'dst': '\''+SYMBOL+SYMBOL+'\'', 'cond':''},
    #{'src': EMPTY, 'dst': '\' \'', 'rule':'', 'cond':''},
]"""

stack = []
lex_stack = []
new_stack = []
end_stack = []
def roll():
    global stack, lex_stack
    j = 0
    for i in range(len(lex_stack)):
        if lex_stack[i] == '-2':
            j = i
    tmp_stack = lex_stack[j:]
    lex_stack = lex_stack[:len(lex_stack)-len(tmp_stack)]
    lex_stack.append(tmp_stack)
    
def begin_list():
    global stack, lex_stack, new_stack
    #new_stack = lex_stack
    new_stack.append(lex_stack)
    #print new_stack
    #lex_stack = []
    #lex_stack.append('-2')
    
def end_list():
    global stack, lex_stack, new_stack
    #print new_stack
    new_stack = []
    #end_stack.append(lex_stack)
    
rule_set = [
    {'src':S_EXPRESSION, 'dst':[ATOMIC_SYMBOL], 'cond':'True', 'action':''},
    {'src':S_EXPRESSION, 'dst':[LIST], 'cond':'True', 'action':''},
    {'src':S_EXPRESSION, 'dst': [KEYWORD, S_EXPRESSION], 'cond':'True', 'action':''},
    {'src':'OPEN_BRACKET', 'dst':['-2'], 'cond':'True', 'action':begin_list},
    {'src':'CLOSE_BRACKET', 'dst':['-3'], 'cond':'True', 'action':end_list},
    {'src':LIST, 'dst':['OPEN_BRACKET', S_EXPRESSION, S_EXPRESSION, S_EXPRESSION, 'CLOSE_BRACKET'], 'cond':'True', 'action':roll},
    {'src':LIST, 'dst':['OPEN_BRACKET', S_EXPRESSION, S_EXPRESSION, 'CLOSE_BRACKET'], 'cond':'True', 'action':roll},
    {'src':LIST, 'dst':['OPEN_BRACKET', S_EXPRESSION, 'CLOSE_BRACKET'], 'cond':'True', 'action':roll},
    {'src':ATOMIC_SYMBOL, 'dst':[KEYWORD, ATOM_PART], 'cond':'True', 'action':''},
    {'src':ATOMIC_SYMBOL, 'dst':[ATOM_PART], 'cond':'True', 'action':''},
    {'src':ATOM_PART, 'dst':[KEYWORD, ATOM_PART], 'cond':'True', 'action':''},
    {'src':ATOM_PART, 'dst':[SYMBOL, ATOM_PART], 'cond':'True', 'action':''},
    {'src':ATOM_PART, 'dst':[SYMBOL], 'cond':'True', 'action':''},


]


def loop_rules():
    global stack,lex_stack
    for rule in rule_set:
        #print stack
        if str(rule['dst'])[1:-1] in str(stack)[1:-1]:
            #print rule['dst']
            if eval(rule['cond']):
                if rule['action']:
                    rule['action']()
                stack = stack[:len(stack)-len(rule['dst'])]
                stack.append(rule['src'])
                loop_rules()
                break
            #print stack
    return

def syntax_translation(lex_flow):
    global stack, lex_stack
    for token in lex_flow:
        token_ch = ''
        if token.isdigit():
            token_ch = SYMBOL
        elif token!='':
            if token == '-2' or token == '-3':
                token_ch=token
            else:
                token_ch = KEYWORD
        lex_stack.append(token)
        #new_stack.append(token)
        stack.append(token_ch)
        loop_rules()
    return stack, lex_stack
                       
def main():
    with open('lex_flow.txt', 'r') as lex_file:
        data = lex_file.read()
    lex_file.close()
    
    lex_flow = []
    lex_flow = data.split(' ')
    
    #print lex_flow
    stack, lex_stack = syntax_translation(lex_flow)
    
    with open('lex_stack.txt', 'w') as t:
        print >>t, lex_stack
    t.close()


# In[8]:

if __name__ == "__main__":
    main()


# In[ ]:



