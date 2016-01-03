__author__ = 'wiktor'

import AST


def addToClass(cls):

    def decorator(func):
        setattr(cls,func.__name__,func)
        return func
    return decorator


class TreePrinter:



    @addToClass(AST.Node)
    def printTree(self):
        # return self.printTree()
        raise Exception("printTree not defined in class " + self.__class__.__name__)


    @addToClass(AST.BinExpr)
    def printTree(self):
        node_list = ""
        if self.op is not None:
            if isinstance(self.op, str):
                node_list += "| " + str(self.op) + "\n"
            else:
                node_list +=  "| " + str(self.op.printTree())
        if self.left is not None:
            if isinstance(self.left, str):
                node_list += "| " +  str(self.left) + "\n"
            else:
                node_list +=  "| " + str(self.left.printTree())
        if self.right is not None:
            if isinstance(self.right, str):
                node_list +=  "| "+ str(self.right) + "\n"
            else:
                node_list += "| " + str(self.right.printTree())

        return node_list
        # ...


    @addToClass(AST.Const)
    def printTree(self):
        return self.val + "\n"

    @addToClass(AST.Program)
    def printTree(self):
        node_list = ""
        if self.blocks is not None:
            node_list += self.blocks.printTree()

        return node_list

    @addToClass(AST.Blocks)
    def printTree(self):
        node_list = ""
        if self.blocks is not None:
            node_list += self.blocks.printTree()

        if self.block is not None:
            node_list += self.block.printTree()

        return node_list

    @addToClass(AST.Block)
    def printTree(self):
        node_list = ""
        if self.block is not None:
            node_list += "| " + self.block.printTree()

        return node_list

    @addToClass(AST.Declarations)
    def printTree(self):
        node_list = ""
        if self.declarations is not None:
            node_list += self.declarations.printTree()

        if self.declaration is not None:
            node_list += self.declaration.printTree()
        return node_list

    @addToClass(AST.Declaration)
    def printTree(self):
        node_list = "DECL\n"
        # if self.type is not None:
        #     node_list += "| " + self.type + "\n"

        if self.inits is not None:
            node_list += self.inits.printTree()
        return node_list

    @addToClass(AST.Inits)
    def printTree(self):
        node_list = ""
        if self.inits is not None:
            node_list += self.inits.printTree()

        if self.init is not None:
            if isinstance(self.init, str):
                node_list += self.init + "\n"
            else:
                node_list += self.init.printTree()
        return node_list

    @addToClass(AST.Init)
    def printTree(self):
        node_list = ""

        if self.sign is not None:
            node_list += "| " +  self.sign + "\n"

        if self.id is not None:
            node_list += "| " + self.id + "\n"

        if self.expression is not None:
            node_list += self.expression.printTree()


        return node_list

    @addToClass(AST.Assignment)
    def printTree(self):
        node_list = ""
        if self.id is not None:
            node_list += "| " + self.id + "\n"

        if self.sign is not None:
            node_list += "| " + self.sign + "\n"

        if self.expression is not None:
            node_list += "| " + self.expression.printTree()


        return node_list


    @addToClass(AST.FunDefs)
    def printTree(self):
        node_list = ""
        if self.fun_list is not None:
            node_list += self.fun_list.printTree()

        if self.fun is not None:
            node_list += self.fun.printTree()

        return node_list

    @addToClass(AST.Fundef)
    def printTree(self):
        node_list = "FUNDEF\n"
        if self.type is not None:
            node_list += "| | RET " + self.type + "\n"

        if self.id is not None:
            node_list += "| | " + self.id + "\n"

        if self.arg_list is not None:
            node_list += self.arg_list.printTree()

        if self.compound_instr is not None:
            node_list += self.compound_instr.printTree()

        return node_list

    @addToClass(AST.ArgList)
    def printTree(self):
        node_list = ""
        if self.arg_list is not None:
            node_list += self.arg_list.printTree()

        if self.arg is not None:
            if isinstance(self.arg, str):
                node_list += self.arg + "\n"
            else:
                node_list += self.arg.printTree()

        return node_list

    @addToClass(AST.ExpressionList)
    def printTree(self):
        node_list = ""
        if self.expr_list is not None:
            node_list += self.expr_list.printTree()

        if self.expr is not None:
            if isinstance(self.expr, str):
                node_list += self.expr + "\n"
            else:
                node_list += self.expr.printTree()

        return node_list

    @addToClass(AST.Arg)
    def printTree(self):
        node_list = ""
        if self.type is not None:
            node_list += "| " + self.type + "\n"

        if self.id is not None:
            node_list += "| " +  self.id + "\n"

        return node_list

    @addToClass(AST.CompoundInstr)
    def printTree(self):
        node_list = ""

        if self.declarations is not None:
            node_list +=  self.declarations.printTree()

        if self.instructions_opt is not None:
            node_list += self.instructions_opt.printTree()


        return node_list

    @addToClass(AST.PrintInstruction)
    def printTree(self):
        node_list = ""
        if self.instr is not None:
            node_list += "| " + self.instr + "\n"

        if self.expr_list is not None:
            node_list += self.expr_list.printTree()

        return node_list

    @addToClass(AST.Instructions)
    def printTree(self):
        node_list = ""
        # print(type(self.instruction))
        if self.instructions is not None:
            node_list += self.instructions.printTree()

        if self.instruction is not None:
            node_list += self.instruction.printTree()

        return node_list

    @addToClass(AST.Instruction)
    def printTree(self):
        node_list = ""
        if self.instruction is not None:
            node_list += "| " + self.instruction.printTree()

        return node_list

    @addToClass(AST.WhileInstr)
    def printTree(self):
        node_list = "WHILE\n"

        if self.condition is not None:
            node_list += "| " + self.condition.printTree()


        if self.instruction is not None:
            node_list += "| " +  self.instruction.printTree()

        return node_list

    @addToClass(AST.Condition)
    def printTree(self):
        node_list = ""
        if self.expression is not None:
            node_list += "| " + self.expression.printTree()


        return node_list


    @addToClass(AST.Return_instr)
    def printTree(self):
        node_list = "RETURN\n"
        if self.expression is not None:
            node_list += "| " + self.expression.printTree()


        return node_list

    @addToClass(AST.ChoiceInstr)
    def printTree(self):
        node_list = "IF\n"
        if self.condition is not None:
            node_list += "| " + self.condition.printTree()

        if self.instruction is not None:
            node_list += "| " +  self.instruction.printTree()

        if self.elseInstruction is not None:
            node_list += "| " +  self.elseInstruction.printTree()
        return node_list
    # @addToClass ...
    # ...
