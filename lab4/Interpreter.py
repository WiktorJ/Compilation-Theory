import AST
from Memory import *
from Exceptions import *
from visit import *
import ast
import sys
import operator as op

sys.setrecursionlimit(10000)


def eval_(node):
    if isinstance(node, ast.Num):  # <number>
        return node.n
    elif isinstance(node, ast.BinOp):  # <left> <operator> <right>
        return operators[type(node.op)](eval_(node.left), eval_(node.right))
    elif isinstance(node, ast.UnaryOp):  # <operator> <operand> e.g., -1
        return operators[type(node.op)](eval_(node.operand))
    elif isinstance(node, ast.Compare):
        return operators[type(node.ops[0])](eval_(node.left), eval_(node.comparators[0]))
    elif isinstance(node, ast.Str):
        return node.s
    else:
        raise TypeError(node)


operators = {ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul,
             ast.Div: op.div, ast.Pow: op.pow, ast.BitXor: op.xor,
             ast.USub: op.neg, ast.Eq: op.eq, ast.NotEq: op.ne, ast.Gt: op.gt,
             ast.GtE: op.ge, ast.Lt: op.lt, ast.LtE: op.le,
             ast.Mod: op.mod}


def eval_expr(expr):
    return eval_(ast.parse(expr, mode='eval').body)


class Interpreter(object):
    def __init__(self):
        self.globalMemory = MemoryStack(Memory("Global"))
        self.functionMemory = MemoryStack()
        self.isFunctionCompound = False

    @on('node')
    def visit(self, node):
        pass

    @when(AST.BinExpr)
    def visit(self, node):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)
        if not isinstance(r1, str) and not isinstance(r2, str):
            s = str(r1) + node.op + str(r2)
            e = eval_expr(s)
        else:
            s = r1 + r2
            e = eval_expr(s)
        return e

    @when(AST.UnaryExpr)
    def visit(self, node):
        return node.expr.accept(self)

    # simplistic while loop interpretation
    @when(AST.WhileInstr)
    def visit(self, node):
        while node.condition.accept(self):
            try:
                node.instruction.accept(self)
            except BreakException:
                break
            except ContinueException:
                pass

    @when(AST.RepeatInstr)
    def visit(self, node):
        while True:
            try:
                node.instruction.accept(self)
                if node.condition.accept(self):
                    break
            except BreakException:
                break
            except ContinueException:
                pass

    @when(AST.ChoiceInstr)
    def visit(self, node):
        if node.condition.accept(self):
            return node.instruction.accept(self)
        elif node.elseInstruction is not None:
            return node.elseInstruction.accept(self)

    @when(AST.ExpressionList)
    def visit(self, node):
        for child in node.children:
            child.accept(self)

    @when(AST.InstructionList)
    def visit(self, node):
        for child in node.children:
            child.accept(self)

    @when(AST.CompoundInstr)
    def visit(self, node):
        fCompound = False
        if not self.isFunctionCompound:
            funFrame = Memory("cpd")
            self.functionMemory.push(funFrame)
            fCompound = True
            self.isFunctionCompound = False
        node.declarations.accept(self)
        node.instructions_opt.accept(self)
        if fCompound:
            self.functionMemory.pop()

    @when(AST.Fundef)
    def visit(self, node):
        self.globalMemory.insert(node.id, node)

    @when(AST.FunctionExpression)
    def visit(self, node):
        fun = self.globalMemory.get(node.name)
        funFrame = Memory(node.name)
        if (fun.arg_list != None):
            for arg, val in list(zip(fun.arg_list.children, node.expr.children)):
                funFrame.put(arg.accept(self), val.accept(self))
        self.functionMemory.push(funFrame)
        self.isFunctionCompound = True
        try:
            fun.compound_instr.accept(self)
        except ReturnValueException as e:
            return e.value
        finally:
            self.functionMemory.pop()

    @when(AST.Arg)
    def visit(self, node):
        return node.id

    @when(AST.ArgList)
    def visit(self, node):
        for child in node.children:
            child.accept(self)

    @when(AST.Assignment)
    def visit(self, node):
        expr = node.expression.accept(self)
        if not (self.functionMemory.set(node.id, expr)):
            self.globalMemory.set(node.id, expr)
        return expr

    @when(AST.BreakInstr)
    def visit(self, node):
        raise BreakException()

    @when(AST.ContinueInstr)
    def visit(self, node):
        raise ContinueException()

    @when(AST.Declaration)
    def visit(self, node):
        node.inits.accept(self)

    @when(AST.DeclarationList)
    def visit(self, node):
        for child in node.children:
            child.accept(self)

    @when(AST.ExpressionList)
    def visit(self, node):
        for child in node.children:
            child.accept(self)

    @when(AST.Float)
    def visit(self, node):
        return float(node.val)

    @when(AST.Init)
    def visit(self, node):
        expr = node.expression.accept(self)
        if not self.functionMemory.is_empty():
            self.functionMemory.insert(node.id, expr)
        else:
            self.globalMemory.insert(node.id, expr)
        return expr

    @when(AST.InitList)
    def visit(self, node):
        for child in node.children:
            child.accept(self)

    @when(AST.Integer)
    def visit(self, node):
        return int(node.val)

    @when(AST.LabeledInstr)
    def visit(self, node):
        pass

    @when(AST.PrintInstruction)
    def visit(self, node):
        print(node.expr_list.accept(self))

    @when(AST.BlockList)
    def visit(self, node):
        for child in node.children:
            child.accept(self)

    @when(AST.Block)
    def visit(self, node):
        node.block.accept(self)

    @when(AST.Program)
    def visit(self, node):
        node.blocks.accept(self)

    @when(AST.Return_instr)
    def visit(self, node):
        raise ReturnValueException(node.expression.accept(self))

    @when(AST.String)
    def visit(self, node):
        return node.val

    @when(AST.Variable)
    def visit(self, node):
        v = self.functionMemory.get(node.name)
        return v if v is not None else self.globalMemory.get(node.name)
