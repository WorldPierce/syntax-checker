import sys
variables = dict()
token = None
index = -1
tokens = []
#node class that I will pass tokens in for data
class Node(object):
    def __init__(self, data):
        self.data = data
        self.children = []
        

    def add_child(self, obj):
        self.children.append(obj)
#general error function I will send if syntax is incorrect
def error():
	print "Error in code, exiting"
	exit()

#lexme is used to set token to the next token
def lexme():
	global index
	global token
	index = index + 1
	if index == len(tokens):
		if token != ';':
			print "Error: statement does not end in semi colon"
			exit()
		return
	token = tokens[index]

#type will identify if a number is an integer or float
def type(number):
	try:
		return int(number)
	except ValueError:
		return float(number)
#eval grabs all operators and performs operations
def eval(root):
	if len(root.children) == 2:
		op = root.data
		if op.isdigit() or op == ';':
			error()
		child1 = eval(root.children[0])
		child2 = eval(root.children[1])
		
		if op == '+':
			value = (type(child1) + type(child2))
			#print "sum = %d" % value
		#elif op == '-':
			#print "here"
		#	value = (type(child1) - type(child2))
		elif op == '*':
			value = (type(child1) * type(child2))
		elif op == '/':
			value = (type(child1) / type(child2))
		elif op == '^':
			value = (type(child1) ** type(child2))
		else: 
		#was not recognizing '-' so made it the default
			value = (type(child1) - type(child2))
		
		return value

	return root.data
#decl is for adding variables to our list of variables declared
def decl():
	global variables
	integer = 0
	if token == 'int':
		integer = 1
	while index != len(tokens):
		lexme()
		if token != ',' and token != ';':
			variables[token] = None
		#making sure variable after comma is legal
		if token == ',':
			lexme()
			if token.isalpha() == False:
				error()
			else:
				variables[token] = None
	if token != ';':
		print "Error: does not end in semi colon"
		exit()
	return


def expr():

	left = term()
	# does token = + or -
	if token == '+' or token == '-':
		op = Node(token)

		lexme()
		right = expr()
		#add children
		op.add_child(left)
		op.add_child(right)
		if op.children[0].data == ';' or op.children[1].data == ';':
			error()
		
		return op
	return left

def term():

	left = factor()
	#does token = * or /
	if token == '*' or token == '/':
		op = Node(token)

		lexme()
		right = expr()
		#add children
		op.add_child(left)
		op.add_child(right)
		if op.children[0].data == ';' or op.children[1].data == ';':
			error()
		return op
	return left

def factor():
	#does token = ^
	left = base()
	if token == "^":
		op = Node(token)
		
		lexme()
		right = expr()
		#add children
		op.add_child(left)
		op.add_child(right)
		if op.children[0].data == ';' or op.children[1].data == ';':
			error()
		return op
	return left

def base():
	global variables
	#does token = () or id or number
	if token == '(':
		lexme() #skip opening paranthesis
		left = expr() #parse expression within paraethesis
		if token != ')':
			op = Node(token)
			lexme()
			temp = expr()
			#add expr and temp as children
			op.add_child(left)
			op.add_child(temp)
			left = op
		if index != len(tokens): # skip end parenthesis
			lexme()

		return left

	elif token in variables: #chec if variable is stored
		
		#add variable to dict
		#if assignment check if variable exits in dict and ad value to key
		var = token
		
		lexme()
		if token == '=':
			#checking for correct syntax
			if index != 1:
				error()
			lexme()
			value = expr()
			value = eval(value)
			#setting variable value
			variables[var] = value
			if token != ';':
				error()
			#print  value.data

			return
			#print token	
		else:
			digit = Node(variables[var])
			return digit

	else: 
		#token is numeric
		#checking for error situations
		if index == len(tokens) and token != ';':
			error()
		if token.isalpha() and token not in variables:
			error()
		if index == 0 and token.isdigit():
			error()
		num = Node(token)

		if index != len(tokens):
			lexme()
		return num

s = sys.argv[1]
	#open file and read
try:
	file = open(s)
except:
	print 'File not found: ', file
	exit()

#check if EOF
#token = tokens[index]
#null is None
#declare root node

#declare my dictionary for variable and values
def main():
	global variables
	global index
	global tokens
	#take input line by line and evaluate
	for line in file:
		index = -1
		tokens = line.split()

		lexme()
		#declaring variables
		if token == 'int' or token == 'real':
			if index != 0:
				error()
			decl()	
		#printing line
		elif token == 'print':
			if index != 0:
				error()
			lexme()
			root = expr()
			if token != ';':
				error()

			ans = eval(root)

			print ans
			#evaluating anything else
		else:
			root = expr()
		
			while index != len(tokens):
				lexme()
				op = Node(token)
				
				temp = expr()

				op.add_child(root)
				op.add_child(temp)

				root = op
if __name__ == '__main__':main()


