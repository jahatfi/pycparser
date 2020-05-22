#!/usr/bin/python3
#https://programmer.group/introduction-of-c-language-source-code-analysis-library-pycparser.html
from __future__ import print_function
import sys
import re
import json

sys.path.extend(['.', '..'])

from pycparser import c_parser, c_ast, parse_file, c_generator

def extract_funcDef(node,defList):
	if node is None:
		return

	childrens = [item[1] for item in node.children()]

	for item in childrens:
		if isinstance(item,c_ast.FuncDef):
			defList.append(item)
		else:
			extract_funcDef(item,defList)

def extract_funcCall(node,funcList):
	if isinstance(node, c_ast.Node): # for AST node
		node = (node,None)
	if node[0] is None:
		return
	childrens = [item[1] for item in node[0].children()]
	
	for item in childrens:
		if isinstance(item, c_ast.FuncCall):
			funcList.append(item)
		else:
			extract_funcCall(item,funcList)


class FuncDefVisitor(c_ast.NodeVisitor):

	def __init__(self,funcname,funcList):
		self.funcname = funcname
		self.funcList = funcList
	
	def visit_FuncDef(self, node):
		if node.decl.name == self.funcname:
			extract_funcCall(node,self.funcList)
			# print('%s at %s' % (node.decl.name, node.decl.coord))

def show_deflist(defList):
	for defFunc in defList:
		name = defFunc.decl.name
		# print(name,defFunc.decl.coord)
		# pass

def show_func_defs(ast, funcname,the_dict,invoke_dict):
    # ast = parse_file(filename, use_cpp=True)
    funcList = []
    v = FuncDefVisitor(funcname,funcList)
    v.visit(ast)
    # print(len(funcList))
    invoke_dict[funcname] = [func.name.name for func in funcList]

    for func in funcList:

    	try:
    		the_dict[func.name.name].append(funcname)
    	except Exception as e:
    		the_dict[func.name.name] = [funcname]
    		# raise e

    	# print('funcDefs:',func.name.name,func.name.coord)

if __name__ == '__main__':
	filename = "./codes/notes.c"
	defList = []
	the_dict = {}
	invoke_dict = {}
	ast = parse_file(filename, use_cpp=True)
	extract_funcDef(ast,defList)
	# print(len(defList))
	show_deflist(defList)
	nameList = [item.decl.name for item in defList]
	for name in nameList:
		show_func_defs(ast,name,the_dict,invoke_dict)
	# parser(filename)

	print('====Ref_dict====')
	for k,v in the_dict.items():
		print('{}:{}'.format(k,v))

	print('====Invoke_dict====')
	for k,v in invoke_dict.items():
		print('{}:{}'.format(k,v))