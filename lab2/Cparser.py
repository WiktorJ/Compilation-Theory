__author__ = 'wiktor'
#!/usr/bin/python

from scanner import Scanner
import AST



class Cparser(object):


    def __init__(self):
        self.scanner = Scanner()
        self.scanner.build()

    tokens = Scanner.tokens


    precedence = (
       ("nonassoc", 'IFX'),
       ("nonassoc", 'ELSE'),
       ("right", '='),
       ("left", 'OR'),
       ("left", 'AND'),
       ("left", '|'),
       ("left", '^'),
       ("left", '&'),
       ("nonassoc", '<', '>', 'EQ', 'NEQ', 'LE', 'GE'),
       ("left", 'SHL', 'SHR'),
       ("left", '+', '-'),
       ("left", '*', '/', '%'),
    )


    def p_error(self, p):
        if p:
            print("Syntax error at line {0}, column {1}: LexToken({2}, '{3}')".format(p.lineno, self.scanner.find_tok_column(p), p.type, p.value))
        else:
            print("Unexpected end of input")


    def p_program(self, p):
        """program : blocks"""

        p[0] = AST.Program(p[1])
        # p[0] = ('PROGRAM',p[1], p[2], p[3])


    def p_blocks(self, p):
        """blocks : blocks block
                  |"""
        if len(p) == 3:
            p[0] = AST.Blocks(p[1], p[2])
        else:
            p[0] = AST.Blocks(None, None)


    def p_block(self, p):
        """block : declaration
                 | fundef
                 | instruction"""
        p[0] = AST.Block(p[1])


    def p_declarations(self, p):
        """declarations : declarations declaration
                        | """


        if len(p) == 3:
            p[0] = AST.Declarations(p[1], p[2])
        else:
            p[0] = AST.Declarations(None, None)
        # else:
        #     p[0] = AST.Declarations(p[1], p[2])

        # if len(p) == 2:
        #     p[0] = ("DECLARATIONS", p[1])
        # elif len(p) == 3:
        #     p[0] = ("DECLARATIONS", p[1], p[2])
        # else:
        #     p[0] = ("DECLARATIONS")


    def p_declaration(self, p):
        """declaration : TYPE inits ';'
                       | error ';' """


        p[0] = AST.Declaration(p[1], p[2])
        # p[0] = ("DECLARATION",)
        #
        # for i in range(1, len(p)):
        #     p[0] += (p[i],)


    def p_inits(self, p):
        """inits : inits ',' init
                 | init """
        if len(p) == 2:
            p[0] = AST.Inits(None, p[1])
        else:
            p[0] = AST.Inits(p[1], p[3])

        # p[0] = ("INITS", p[1])

    def p_init(self, p):
        """init : ID '=' expression """

        p[0] = AST.Init(p[1], p[2], p[3])
        # p[0] = ("INIT", p[1], p[2], p[3])


    def p_instructions_opt(self, p):
        """instructions_opt : instructions
                            | """
        if len(p) == 2:
            p[0] = AST.Instructions(p[1], None)
        else:
            p[0] = AST.Instructions(None, None)
        # else:
        #     p[0] = AST.Instructions(p[1], p[2])
        #
        #
        # p[0] = ("INSTRUCTIONS_OPT", p[1])


    def p_instructions(self, p):
        """instructions : instructions instruction
                        | instruction """

        if len(p) == 2:
            p[0] = AST.Instructions(p[1], None)
        else:
            p[0] = AST.Instructions(p[1], p[2])
        # p[0] = ("INSTRUCTIONS", p[1])

    def p_instruction(self, p):
        """instruction : print_instr
                       | labeled_instr
                       | assignment
                       | choice_instr
                       | while_instr
                       | repeat_instr
                       | return_instr
                       | break_instr
                       | continue_instr
                       | compound_instr
                       | expression ';' """

        # for i in (0, len(p)):
        #     print(str(i) + " " + str(p[i]))




        p[0] = AST.Instruction(p[1])
        # p[0] = ("INSTRUCTION", p[1])


    def p_print_instr(self, p):
        """print_instr : PRINT expr_list ';'
                       | PRINT error ';' """

        p[0] = AST.PrintInstruction(p[1], p[2])
        # p[0] = ("PRINT_INSTR", p[1], p[2], p[3])


    def p_labeled_instr(self, p):
        """labeled_instr : ID ':' instruction """
        p[0] = AST.LabeledInstr(p[1], p[3])
        # p[0] = ("LABELED_INSTR", p[1], p[2], p[3])


    def p_assignment(self, p):
        """assignment : ID '=' expression ';' """
        p[0] = AST.Assignment(p[1], p[2], p[3])
        # p[0] = ("ASSIGNMENT", p[1], p[2], p[3])

    def p_choice_instr(self, p):
        """choice_instr : IF '(' condition ')' instruction  %prec IFX
                        | IF '(' condition ')' instruction ELSE instruction
                        | IF '(' error ')' instruction  %prec IFX
                        | IF '(' error ')' instruction ELSE instruction """

        # for i in range(0, len(p)):
        #     print(str(i) + " " + str(p[i]))
        p[0] = AST.ChoiceInstr(p[3], p[5], p[7])
        # p[0] = ("CHOICE_INSTR", p[1], p[3], p[5])

    def p_while_instr(self, p):
        """while_instr : WHILE '(' condition ')' instruction
                       | WHILE '(' error ')' instruction """
        p[0] = AST.WhileInstr(p[3], p[5])
        # p[0] = ("WHILE_INSTR", p[1], p[3], p[5], )


    def p_repeat_instr(self, p):
        """repeat_instr : REPEAT instructions UNTIL condition ';' """
        p[0] = AST.RepeatInstr(p[2], p[4])
        # p[0] = ("REPEAt_INSTR", p[1], p[2], p[3])

    def p_return_instr(self, p):
        """return_instr : RETURN expression ';' """
        p[0] = AST.Return_instr(p[2])
        # p[0] = ("REPEAT_INSTR", p[1], p[2], p[3])

    def p_continue_instr(self, p):
        """continue_instr : CONTINUE ';' """
        p[0] = AST.ContinueInstr()

    def p_break_instr(self, p):
        """break_instr : BREAK ';' """
        p[0] = AST.BreakInstr()

    def p_compound_instr(self, p):
        """compound_instr : '{' declarations instructions_opt '}' """
        p[0] = AST.CompoundInstr(p[2], p[3])
        # p[0] = ("COMPOUND_INSTR", p[2], p[3])

    def p_condition(self, p):
        """condition : expression"""
        p[0] = AST.Condition(p[1])

    def p_const(self, p):
        """const : INTEGER
                 | FLOAT
                 | STRING"""
        p[0] = AST.Const(p[1])
        # p[0] = ("CONST", p[1])


    def p_expression(self, p):
        """expression : const
                      | ID
                      | expression '+' expression
                      | expression '-' expression
                      | expression '*' expression
                      | expression '/' expression
                      | expression '%' expression
                      | expression '|' expression
                      | expression '&' expression
                      | expression '^' expression
                      | expression AND expression
                      | expression OR expression
                      | expression SHL expression
                      | expression SHR expression
                      | expression EQ expression
                      | expression NEQ expression
                      | expression '>' expression
                      | expression '<' expression
                      | expression LE expression
                      | expression GE expression
                      | '(' expression ')'
                      | '(' error ')'
                      | ID '(' expr_list_or_empty ')'
                      | ID '(' error ')' """



        # for i in range(0, len(p)):
        #     print(str(i) + " " + str(p[i]))
        #
        # if len(p) == 2:
        #     p[0] = AST.BinExpr(None,p[1],None)
        #
        # else:
        #     p[0] = AST.BinExpr(p[2],p[1],p[3])

        if len(p) == 2:
            p[0] = AST.BinExpr(None,p[1],None)
        elif len(p) == 4 and p[1] != '(':
            p[0] = p[0] = AST.BinExpr(p[2],p[1],p[3])
        elif len(p) == 4:
            p[0] = AST.BinExpr(None,p[2],None)
        elif len(p) == 5:
            p[0] = AST.BinExpr(None, p[1], p[3])

        # p[0] = ("EXPRESSIONxD" + str(len(p)),)
        # for i in range(1, len(p)):
        #         p[0] += (p[i],)

    def p_expr_list_or_empty(self, p):
        """expr_list_or_empty : expr_list
                              | """
        if len(p) == 2:
            p[0] = AST.FunDefs(p[1], None)
        else:
            p[0] = AST.FunDefs(p[1], p[2])
        # p[0] = ("EXPRESSION_LIST_OR_EMPTY",)
        #
        # for i in range(1, len(p)):
        #     p[0] += (p[i],)

    def p_expr_list(self, p):
        """expr_list : expr_list ',' expression
                     | expression """


        if len(p) == 2:
            p[0] = AST.ExpressionList(p[1], None)
        else:
            p[0] = AST.ExpressionList(p[1], p[3])

        # p[0] = ("EXPRESSION_LIST",)
        #
        # for i in range(1, len(p)):
        #     p[0] += (p[i],)



    def p_fundef(self, p):
        """fundef : TYPE ID '(' args_list_or_empty ')' compound_instr """

        p[0] = AST.Fundef( p[1], p[2], p[4], p[6])
        # p[0] = ("FUNDEF",)
        #
        # for i in range(1, len(p)):
        #     p[0] += (p[i],)

    def p_args_list_or_empty(self, p):
        """args_list_or_empty : args_list
                              | """


        if len(p) == 2:
            p[0] = AST.ArgList(p[1], None)

        # p[0] = ("ARGS_LIST_OR_EMPTY",)
        #
        # for i in range(1, len(p)):
        #     p[0] += (p[i],)

    def p_args_list(self, p):
        """args_list : args_list ',' arg
                     | arg """


        if len(p) == 2:
            p[0] = AST.ArgList(p[1], None)
        else:
            p[0] = AST.ArgList(p[1], p[3])

        # p[0] = ("ARGS_LIST",)
        #
        # for i in range(1, len(p)):
        #     p[0] += (p[i],)

    def p_arg(self, p):
        """arg : TYPE ID """
        p[0] = AST.Arg(p[1], p[2])
        # p[0] = ("ARGS", p[1], p[2])

