__author__ = 'wiktor'

class Node(object):
    def accept(self, visitor):
        return visitor.visit(self)

class BinExpr(Node):

    def __init__(self, op, left, right, line):
        self.op = op
        self.left = left
        self.right = right
        self.line = line

class UnaryExpr(Node):

    def __init__(self, expr):
        self.expr = expr

class FunctionExpression(Node):

    def __init__(self, name, expr, line):
        self.name = name
        self.expr = expr
        self.line = line

class Program(Node):

    def __init__(self, blocks):
        self.blocks = blocks

class BlockList(Node):
    def __init__(self):
        self.children = []

    def addArgument(self, fundef):
        self.children.append(fundef)

class Block(Node):

    def __init__(self, block):
        self.block = block
    #
    # def __str__(self):
    #     return self.printTree()

class DeclarationList(Node):
    def __init__(self):
        self.children = []

    def addArgument(self, fundef):
        self.children.append(fundef)

class Declaration(Node):

    def __init__(self, type, inits):
        self.type = type
        self.inits = inits

class Const(Node):

    def __init__(self, val):
        self.val = val

class Integer(Const):

    def __init__(self, val):
        super(Integer, self).__init__(val)


class Float(Const):

    def __init__(self, val):
        super(Float, self).__init__(val)


class String(Const):

    def __init__(self, val):
        super(String, self).__init__(val)


class Variable(Node):

    def __init__(self, name, line):
        self.name = name
        self.line = line

class Init(Node):

    def __init__(self, id, sign, expression, line):
        self.id = id
        self.sign = sign
        self.expression = expression
        self.line = line

class InitList(Node):

    def __init__(self):
        self.children = []

    def addArgument(self, fundef):
        self.children.append(fundef)

class PrintInstruction(Node):

    def __init__(self, instr, expr_list, line):
        self.instr = instr
        self.expr_list = expr_list
        self.line = line

class LabeledInstr(Node):
    def __init__(self, id, instruction, line):
        self.instruction = instruction
        self.id = id
        self.line = line

class Assignment(Node):

    def __init__(self, id, sign, expression, line):
        self.id = id
        self.sign = sign
        self.expression = expression
        self.line = line

class Instruction(Node):
    def __init__(self, instruction):
        self.instruction = instruction

class InstructionList(Node):
    def __init__(self):
        self.children = []

    def addArgument(self, fundef):
        self.children.append(fundef)

class ChoiceInstr(Node):

    def __init__(self, condition, instruction, elseInstruction, line):
        self.condition = condition
        self.instruction = instruction
        self.elseInstruction = elseInstruction
        self.line = line

class WhileInstr(Node):

    def __init__(self, condition, instruction, line):
        self.condition = condition
        self.instruction = instruction
        self.line = line

class RepeatInstr(Node):

    def __init__(self, instruction, condition, line):
        self.condition = condition
        self.instruction = instruction
        self.line = line


class Return_instr(Node):

    def __init__(self, expression, line):
        self.expression = expression
        self.line = line

class ContinueInstr(Node):
      def __init__(self, line):
        self.line = line

class BreakInstr(Node):
      def __init__(self, line):
        self.line = line


class CompoundInstr(Node):

    def __init__(self, declarations, instructions_opt):
        self.instructions_opt = instructions_opt
        self.declarations = declarations

class Fundef(Node):

    def __init__(self, type, id, arg_list, compound_instr, line):
        self.type = type
        self.id = id
        self.arg_list = arg_list
        self.compound_instr = compound_instr
        self.line = line

class Arg(Node):

    def __init__(self, type, id):
        self.type = type
        self.id = id

class ArgList(Node):
    def __init__(self):
        self.children = []

    def addArgument(self, fundef):
        self.children.append(fundef)

class FunDefList(Node):
    def __init__(self):
        self.children = []

    def addArgument(self, fundef):
        self.children.append(fundef)

class ExpressionList(Node):
    def __init__(self):
        self.children = []

    def addArgument(self, fundef):
        self.children.append(fundef)

class Condition(Node):

    def __init__(self, expression, line):
        self.expression = expression
        self.line = line



