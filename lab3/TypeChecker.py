from collections import defaultdict
import AST
from SymbolTable import VariableSymbol, SymbolTable, FunctionSymbol

__author__ = 'wiktor'


ttype = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: None)))
for op in ['+', '-', '*', '/', '%', '<', '>', '<<', '>>', '|', '&', '^', '<=', '>=', '==', '!=']:
    ttype[op]['int']['int'] = 'int'

for op in ['+', '-', '*', '/']:
    ttype[op]['int']['float'] = 'float'
    ttype[op]['float']['int'] = 'float'
    ttype[op]['float']['float'] = 'float'

for op in ['<', '>', '<=', '>=', '==', '!=']:
    ttype[op]['int']['float'] = 'int'
    ttype[op]['float']['int'] = 'int'
    ttype[op]['float']['float'] = 'int'

ttype['+']['string']['string'] = 'string'
ttype['*']['string']['int'] = 'string'

for op in ['<', '>', '<=', '>=', '==', '!=']:
    ttype[op]['string']['string'] = 'int'



class NodeVisitor(object):

    def __init__(self):
        self.symbol_table = SymbolTable(None, "root")
        self.current_type = ""
        self.current_function = None
        self.is_in_loop = False

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)


    def generic_visit(self, node):        # Called if no explicit visitor function exists for a node.
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            for child in node.children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, AST.Node):
                            self.visit(item)
                elif isinstance(child, AST.Node):
                    self.visit(child)

    # simpler version of generic_visit, not so general
    # def generic_visit(self, node):
    #    for child in node.children:
    #        self.visit(child)



class TypeChecker(NodeVisitor):

    def visit_BinExpr(self, node):
        if isinstance(node.left, str):
            type1 = node.left
        else:
            type1 = self.visit(node.left)     # type1 = node.left.accept(self)
        if isinstance(node.right, str):
            type2 = node.right
        else:
            type2 = self.visit(node.right)    # type2 = node.right.accept(self)
        op = node.op
        if ttype[op][type1][type2] is None:
            print("Wrong expression " + op + " in line: " + self.my_str(node.line))
        return ttype[op][type1][type2]

    def visit_UnaryExpr(self, node):
        return self.visit(node.expr)

    def visit_PrintInstruction(self, node):
        self.visit(node.expr_list)

    def visit_FunctionExpression(self, node):
        function_definition = self.symbol_table.getGlobal(node.name)
        if function_definition is None or not isinstance(function_definition, FunctionSymbol):
            print("function " + node.name + " is not defined" + " in line: " + self.my_str(node.line))
        else:
            if node.expr is not None:
                types = [self.visit(child) for child in node.expr.children]
                declared_types = function_definition.args
                if len(types) != len((declared_types)):
                    print("Wrong arguments in function " + node.name + " in line: " + self.my_str(node.line))
                else:
                    for given_type, declared_type in zip(types, declared_types):
                        if given_type != declared_type:
                            print("Mismatching argument types Expected " + self.my_str(declared_type) + ", got " + self.my_str(given_type) + "in line: " + self.my_str(node.line))
            elif function_definition.args != []:
                print("Worng number of arguments in function: " + node.name + "in line: " + self.my_str(node.line))
            return function_definition.type


    def visit_Variable(self, node):
        dec = self.symbol_table.getGlobal(node.name)
        if dec is None:
            print("Undefined symbol: " + node.name + "in line: " + self.my_str(node.line))
        else:
            return dec.type

    def visit_WhileInstr(self, node):
        self.is_in_loop = True
        self.visit(node.condition)
        self.visit(node.instruction)
        self.is_in_loop = False

    def visit_RepeatInstr(self, node):
        self.is_in_loop = True
        self.visit(node.condition)
        self.visit(node.instructions)
        self.is_in_loop = False

    def visit_Return_instr(self, node):
        if self.current_function is None:
            print("Return placed outside of a function in line " + self.my_str(node.line))
        else:
            type = self.visit(node.expression)
            if type != self.current_function.type:
                print("Expected reutrn type " + self.my_str(self.current_function.type) + " actual" + self.my_str(type)+ "in line: " + self.my_str(self.my_str(node.line)))

    def visit_Fundef(self, node):
        if self.symbol_table.get(node.id):
            print("Function " + node.id + "already defined" + "in line: " + self.my_str(node.line))
        else:
            function = FunctionSymbol(node.id, node.type, SymbolTable(self.symbol_table, node.id))
            self.symbol_table.put(node.id, function)
            self.current_function = function
            self.symbol_table = self.current_function.symbol_table
            if node.arg_list is not None:
                self.visit(node.arg_list)
            self.visit(node.compound_instr)
            self.symbol_table = self.symbol_table.getParentScope()
            self.current_function= None

    def visit_Arg(self, node):
        if self.symbol_table.get(node.id) is not None:
            print("Double argument in function: " + node.id + "in line: " + self.my_str(node.line))
        else:
            self.symbol_table.put(node.id, VariableSymbol(node.id, node.type))
            self.current_function.put_arg(node.type)

    def visit_RelExpr(self, node):
        type1 = self.visit(node.left)     # type1 = node.left.accept(self)
        type2 = self.visit(node.right)    # type2 = node.right.accept(self)
        # ...
        #

    def visit_Integer(self, node):
        return 'int'

    def visit_Float(self, node):
        return 'float'

    def visit_String(self, node):
        return 'string'

    def visit_Init(self, node):
        given_type = self.visit(node.expression)
        if given_type == self.current_type or (given_type == "int" and self.current_type =="float"):
            if self.symbol_table.get(node.id) is not None:
                print("The" +  node.id + "was already defined" + "in line: " + self.my_str(node.line))
            else:
                self.symbol_table.put(node.id, VariableSymbol(node.id, self.current_type))
        else:
            print("Forbidden type assignment " + self.my_str(given_type) + " to " + self.my_str(self.current_type)+ "in line: " + self.my_str(node.line))

    def visit_CompoundInstr(self, node):
        self.symbol_table = SymbolTable(self.symbol_table, "inner")
        self.visit(node.declarations)
        self.visit(node.instructions_opt)
        self.symbol_table = self.symbol_table.getParentScope()


    def visit_ChoiceInstr(self, node):
        self.visit(node.condition)
        self.visit(node.instruction)
        if node.elseInstruction is not None:
            self.visit(node.elseInstruction)

    def visit_Assignment(self, node):
        definition = self.symbol_table.getGlobal(node.id)
        type = self.visit(node.expression)
        if definition is None:
            print("Used undefined symbol " + node.id + "in line: " + self.my_str(node.line))
        elif type != definition.type and (definition.type != "float" and definition != "int"):
            print("Bad assignment of " + self.my_str(type) + " to " +  self.my_str(definition.type) + "in line: " + self.my_str(node.line))

    def visit_Block(self, node):
        self.visit(node.block)

    def visit_Declaration(self,node):
        self.current_type = node.type
        self.visit(node.inits)
        self.current_type = ""

    def visit_ContinueInstr(self, node):
        if self.is_in_loop == False:
            print("Continue instr used outsied of function")


    def visit_BreakInstr(self, node):
        if self.is_in_loop == False:
            print("Break instr used outsied of function")

    def visit_Program(self, node):
        self.visit(node.blocks)

    def my_str(self, s):
        return 'None' if s is None else str(s)