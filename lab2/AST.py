__author__ = 'wiktor'

class Node(object):

    def __str__(self):
        return self.printTree()


class BinExpr(Node):

    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


class Program(Node):

    def __init__(self, blocks):
        self.blocks  = blocks

class Blocks(Node):

    def __init__(self, blocks, block):
        self.blocks = blocks
        self.block = block

class Block(Node):

    def __init__(self, block):
        self.block = block
    #
    # def __str__(self):
    #     return self.printTree()

class Declarations(Node):

    def __init__(self, declarations, declaration):
        self.declarations = declarations
        self.declaration = declaration

class Declaration(Node):

    def __init__(self, type, inits):
        self.type = type
        self.inits = inits

class Const(Node):

    def __init__(self, val):
        self.val = val

class Integer(Const):

    def __init__(self, val):
        Const.__init__(self, val)
    #...


class Float(Const):

    def __init__(self, val):
        Const.__init__(self, val)
    #...


class String(Const):

    def __init__(self, val):
        Const.__init__(self, val)
    #...


class Variable(Node):
    pass
    #...

class Init(Node):

    def __init__(self, id, sign, expression):
        self.id = id
        self.sign = sign
        self.expression = expression

class Inits(Node):

    def __init__(self, inits, init):
        self.inits = inits
        self.init = init

class PrintInstruction(Node):

    def __init__(self, instr, expr_list):
        self.instr = instr
        self.expr_list = expr_list

class LabeledInstr(Node):
    def __init__(self, id, instruction):
        self.instruction = instruction
        self.id = id

class Assignment(Node):

    def __init__(self, id, sign, expression):
        self.id = id
        self.sign = sign
        self.expression = expression

class Instruction(Node):
    def __init__(self, instruction):
        self.instruction = instruction

class Instructions(Node):
    def __init__(self, instructions, instruction):
        self.instruction = instruction
        self.instructions = instructions

class ChoiceInstr(Node):

    def __init__(self, condition, instruction, elseInstruction):
        self.condition = condition
        self.instruction = instruction
        self.elseInstruction = elseInstruction

class WhileInstr(Node):

    def __init__(self, condition, instruction):
        self.condition = condition
        self.instruction = instruction

class RepeatInstr(Node):

    def __init__(self, instruction, condition):
        self.condition = condition
        self.instruction = instruction


class Return_instr(Node):

    def __init__(self, expression):
        self.expression = expression

class ContinueInstr(Node):
    pass

class BreakInstr(Node):
    pass

class CompoundInstr(Node):

    def __init__(self, declarations, instructions_opt):
        self.instructions_opt = instructions_opt
        self.declarations = declarations

class Fundef(Node):

    def __init__(self, type, id, arg_list, compound_instr):
        self.type = type
        self.id = id
        self.arg_list = arg_list
        self.compound_instr = compound_instr

class Arg(Node):

    def __init__(self, type, id):
        self.type = type
        self.id = id

class ArgList(Node):

    def __init__(self, arg_list, arg):
        self.arg_list = arg_list
        self.arg = arg

class FunDefs(Node):

    def __init__(self, fun_list, fun):
        self.fun_list = fun_list
        self.fun = fun

class ExpressionList(Node):

    def __init__(self, expr_list, expr):
        self.expr_list = expr_list
        self.expr = expr

class Condition(Node):

    def __init__(self, expression):
        self.expression = expression



