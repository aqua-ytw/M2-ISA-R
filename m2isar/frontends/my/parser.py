# SPDX-License-Identifier: Apache-2.0
#
# This file is part of the M2-ISA-R project: https://github.com/tum-ei-eda/M2-ISA-R
#
# Copyright (C) 2022
# Chair of Electrical Design Automation
# Technical University of Munich

import argparse
import itertools
import logging
import pathlib
import pickle
import sys

from antlr4 import *

from ... import M2Error, M2SyntaxError
from ...metamodel import arch, behav, patch_model
from . import expr_interpreter
# from .architecture_model_builder import ArchitectureModelBuilder
# from .behavior_model_builder import BehaviorModelBuilder
from .utils import RADIX, SHORTHANDS, SIGNEDNESS, flatten_list
# from .importer import recursive_import
# from .load_order import LoadOrder
from .utils import make_parser

from .parser_gen import CoreDSL2Lexer, CoreDSL2Listener, CoreDSL2Parser, CoreDSL2Visitor


class MyVisitor(CoreDSL2Visitor):
    """ANTLR visitor to build an M2-ISA-R behavioral model of a function or instruction
    of a CoreDSL 2 specification.
    """

    # def __init__(self, constants: "dict[str, arch.Constant]", memories: "dict[str, arch.Memory]", memory_aliases: "dict[str, arch.Memory]",
    #    fields: "dict[str, arch.BitFieldDescr]", functions: "dict[str, arch.Function]", warned_fns: "set[str]"):
    def __init__(self):

        super().__init__()

        self._constants = {}
        self._memories = {}
        self._memory_aliases = {}
        self._fields = {}
        self._functions = {}
        self._scalars = {}
        # self._functions = functions
        self.warned_fns = set()
        self.level = 0

    def print(self, *args, **kwargs):
        print(*(["  " * self.level] + list(args)), **kwargs)

    def visitChildren(self, node):
        """Helper method to return flatter results on tree visits."""
        # print("visitChildren")

        ret = super().visitChildren(node)
        if isinstance(ret, list) and len(ret) == 1:
            return ret[0]
        return ret

    def aggregateResult(self, aggregate, nextResult):
        """Aggregate results from multiple children into a list."""

        ret = aggregate
        if nextResult is not None:
            if ret is None:
                ret = [nextResult]
            else:
                ret += [nextResult]
        return ret

    def visitProcedure_call(self, ctx: CoreDSL2Parser.Procedure_callContext):
        """Generate a procedure (method call without return value) call."""
        self.print("visitProcedure_call")
        self.level += 1

        # extract name and reference to procedure object to be called
        name = ctx.ref.text
        self.print("name", name)
        ref = self._functions.get(name, None)

        # generate method arguments
        args = [self.visit(obj) for obj in ctx.args] if ctx.args else []
        self.print("args", args)

        ret = behav.ProcedureCall(ref, args)
        self.level -= 1
        return ret

    def visitMethod_call(self, ctx: "CoreDSL2Parser.Method_callContext"):
        """Generate a function (method call with return value) call."""
        self.print("visitMethod_call")
        self.level += 1

        # extract name and reference to function object to be called
        name = ctx.ref.text
        ref = self._functions.get(name, None)

        # generate method arguments
        args = [self.visit(obj) for obj in ctx.args] if ctx.args else []

        ret = behav.FunctionCall(ref, args)
        self.level -= 1
        return ret


    def visitBlock(self, ctx: CoreDSL2Parser.BlockContext):
        """Generate a block of statements, return a list."""
        self.print("visitBlock")
        self.level += 1

        items = [self.visit(obj) for obj in ctx.items]
        items = flatten_list(items)
        ret = items
        self.level -= 1
        return ret

    def visitDeclaration(self, ctx: CoreDSL2Parser.DeclarationContext):
        """Generate a declaration statement. Can be multiple declarations of
        the same type at once. Each declaration can have an initial value.
        """
        self.print("visitDeclaration")
        self.level += 1

        # extract variable qualifiers, currently unused
        storage = [self.visit(obj) for obj in ctx.storage]
        qualifiers = [self.visit(obj) for obj in ctx.qualifiers]
        attributes = [self.visit(obj) for obj in ctx.attributes]

        type_ = self.visit(ctx.type_)

        decls: "list[CoreDSL2Parser.DeclaratorContext]" = ctx.declarations

        ret_decls = []

        # iterate over all contained declarations
        for decl in decls:
            name = decl.name.text
            self.print("name", name)

            # instantiate a scalar and its definition
            s = arch.Scalar(name, None, StaticType.NONE, type_.width, arch.DataType.S if type_.signed else arch.DataType.U)
            self._scalars[name] = s
            sd = behav.ScalarDefinition(s)

            # if initializer is present, generate an assignment to apply
            # initialization to the scalar
            if decl.init:
                init = self.visit(decl.init)
                self.print("init", init)

                a = behav.Assignment(sd, init)
                ret_decls.append(a)

            # if not only generate the declaration
            else:
                ret_decls.append(sd)

        ret = ret_decls
        self.level -= 1
        return ret

    def visitReturn_statement(self, ctx: CoreDSL2Parser.Return_statementContext):
        """Generate a return statement."""
        self.print("visitReturn_statement")
        self.level += 1

        expr = self.visit(ctx.expr) if ctx.expr else None
        ret = behav.Return(expr)
        self.level -= 1
        return ret

    def visitWhile_statement(self, ctx: CoreDSL2Parser.While_statementContext):
        """Generate a while loop."""
        self.print("visitWhile_statement")
        self.level += 1

        stmt = self.visit(ctx.stmt) if ctx.stmt else None
        cond = self.visit(ctx.cond)

        if not isinstance(stmt, list):
            stmt = [stmt]

        ret = behav.Loop(cond, stmt, False)
        self.level -= 1
        return ret

    def visitDo_statement(self, ctx: CoreDSL2Parser.Do_statementContext):
        """Generate a do .. while loop."""
        self.print("visitDo_statement")
        self.level += 1


        stmt = self.visit(ctx.stmt) if ctx.stmt else None
        cond = self.visit(ctx.cond)

        if not isinstance(stmt, list):
            stmt = [stmt]

        ret = behav.Loop(cond, stmt, True)
        self.level -= 1
        return ret

    def visitFor_statement(self, ctx: CoreDSL2Parser.For_statementContext):
        """Generate a for loop. Currently hacky, untested and mostly broken."""
        self.print("visitFor_statement")
        self.level += 1

        start_decl, start_expr, end_expr, loop_exprs = self.visit(ctx.cond)
        stmt = self.visit(ctx.stmt) if ctx.stmt else None

        if not isinstance(stmt, list):
            stmt = [stmt]

        ret = []

        if start_decl is not None:
            ret.append(start_decl)
        if start_expr is not None:
            ret.append(start_expr)

        if loop_exprs:
            stmt.extend(loop_exprs)

        ret.append(behav.Loop(end_expr, stmt, False))

        ret = ret
        self.level -= 1
        return ret

    def visitFor_condition(self, ctx: CoreDSL2Parser.For_conditionContext):
        """Generate the condition of a for loop."""
        self.print("visitFor_condition")
        self.level += 1

        start_decl = self.visit(ctx.start_decl) if ctx.start_decl else None
        start_expr = self.visit(ctx.start_expr) if ctx.start_expr else None
        end_expr = self.visit(ctx.end_expr) if ctx.end_expr else None
        loop_exprs = [self.visit(obj) for obj in ctx.loop_exprs] if ctx.loop_exprs else None

        ret = start_decl, start_expr, end_expr, loop_exprs
        self.level -= 1
        return ret

    def visitIf_statement(self, ctx: CoreDSL2Parser.If_statementContext):
        """Generate an if statement. Packs all if, else if and else branches
        into one object.
        """
        self.print("visitIf_statement")
        self.level += 1

        conds = [self.visit(x) for x in ctx.cond]
        stmts = [self.visit(x) for x in ctx.stmt]

        stmts = [[x] if not isinstance(x, list) else x for x in stmts]

        ret = behav.Conditional(conds, stmts)
        self.level -= 1
        return ret

    def visitConditional_expression(self, ctx: CoreDSL2Parser.Conditional_expressionContext):
        """Generate a ternary expression."""
        self.print("visitConditional_expression")
        self.level += 1

        cond = self.visit(ctx.cond)
        then_expr = self.visit(ctx.then_expr)
        else_expr = self.visit(ctx.else_expr)

        ret = behav.Ternary(cond, then_expr, else_expr)
        self.level -= 1
        return ret

    def visitBinary_expression(self, ctx: CoreDSL2Parser.Binary_expressionContext):
        """Generate a binary expression."""
        self.print("visitBinary_expression")
        self.level += 1

        left = self.visit(ctx.left)
        op =  behav.Operator(ctx.bop.text)
        self.print("op", ctx.bop.text)
        right = self.visit(ctx.right)

        ret = behav.BinaryOperation(left, op, right)
        self.level -= 1
        return ret

    def visitPreinc_expression(self, ctx: CoreDSL2Parser.Preinc_expressionContext):
        """Generate a pre-increment expression. Not yet supported, throws
        :exc:`NotImplementedError`."""
        self.print("visitPreinc_expression")
        self.level += 1

        raise NotImplementedError("pre-increment expressions are not supported yet")

    def visitPostinc_expression(self, ctx: CoreDSL2Parser.Preinc_expressionContext):
        """Generate a post-increment expression. Not yet supported, throws
        :exc:`NotImplementedError`."""
        self.print("visitPostinc_expression")
        self.level += 1

        raise NotImplementedError("post-increment expressions are not supported yet")

    def visitPrefix_expression(self, ctx: CoreDSL2Parser.Prefix_expressionContext):
        """Generate an unary expression."""
        self.print("visitPrefix_expression")
        self.level += 1

        op = behav.Operator(ctx.prefix.text)
        right = self.visit(ctx.right)

        ret = behav.UnaryOperation(op, right)
        self.level -= 1
        return ret

    def visitParens_expression(self, ctx: CoreDSL2Parser.Parens_expressionContext):
        """Generate a parenthesized expression."""
        self.print("visitParens_expression")
        self.level += 1

        expr = self.visit(ctx.expr)
        ret = behav.Group(expr)
        self.level -= 1
        return ret

    def visitSlice_expression(self, ctx: CoreDSL2Parser.Slice_expressionContext):
        """Generate a slice expression. Depending on context, this is translated
        to either an actual :class:`m2isar.metamodel.behav.SliceOperation`or
        an :class:`m2isar.metamodel.behav.IndexedReference` if a :class:`m2isar.metamodel.arch.Memory
        object is to be sliced.
        """
        self.print("visitSlice_expression")
        self.level += 1

        expr = self.visit(ctx.expr)

        left = self.visit(ctx.left)
        right = self.visit(ctx.right) if ctx.right else left

        if isinstance(expr, behav.NamedReference) and isinstance(expr.reference, arch.Memory) and expr.reference.data_range.length > 1:
            ret = behav.IndexedReference(expr.reference, left, right)
            self.level -= 1
            return ret
        else:
            ret = behav.SliceOperation(expr, left, right)
            self.level -= 1
            return ret

    def visitConcat_expression(self, ctx: CoreDSL2Parser.Concat_expressionContext):
        """Generate a concatenation expression."""
        self.print("visitConcat_expression")
        self.level += 1

        left = self.visit(ctx.left)
        right = self.visit(ctx.right)

        ret = behav.ConcatOperation(left, right)
        self.level -= 1
        return ret

    def visitAssignment_expression(self, ctx: CoreDSL2Parser.Assignment_expressionContext):
        """Generate an assignment. If a combined arithmetic-assignment is present,
        generate an additional binary operation and use it as the RHS.
        """
        self.print("visitAssignment_expression")
        self.level += 1

        op = ctx.bop.text
        left = self.visit(ctx.left)
        right = self.visit(ctx.right)

        if op != "=":
            op2 = behav.Operator(op[:-1])
            right = behav.BinaryOperation(left, op2, right)

        ret = behav.Assignment(left, right)
        self.level -= 1
        return ret

    def visitReference_expression(self, ctx: CoreDSL2Parser.Reference_expressionContext):
        """Generate a simple reference."""
        self.print("visitReference_expression")
        self.level += 1

        name = ctx.ref.text
        self.print("name", name)

        var = self._scalars.get(name) or \
            self._fields.get(name) or \
            self._constants.get(name) or \
            self._memory_aliases.get(name) or \
            self._memories.get(name)

        ret = behav.NamedReference(var)
        self.level -= 1
        return ret

    def visitInteger_constant(self, ctx: CoreDSL2Parser.Integer_constantContext):
        """Generate an integer literal."""
        self.print("visitInteger_constant")
        self.level += 1

        text: str = ctx.value.text.lower()
        self.print("text", text)

        tick_pos = text.find("'")

        if tick_pos != -1:
            width = int(text[:tick_pos])
            radix = text[tick_pos+1]
            value = int(text[tick_pos+2:], RADIX[radix])

        else:
            value = int(text, 0)
            width = value.bit_length()

        ret = behav.IntLiteral(value, width)
        self.level -= 1
        return ret

    def visitCast_expression(self, ctx: CoreDSL2Parser.Cast_expressionContext):
        """Generate a type cast."""
        self.print("visitCast_expression")
        self.level += 1

        expr = self.visit(ctx.right)
        if ctx.type_:
            type_ = self.visit(ctx.type_)
            sign = arch.DataType.S if type_.signed else arch.DataType.U
            size = type_.width

        if ctx.sign:
            sign = self.visit(ctx.sign)
            sign = arch.DataType.S if sign else arch.DataType.U
            size = None

        ret = behav.TypeConv(sign, size, expr)
        self.level -= 1
        return ret

    def visitType_specifier(self, ctx: CoreDSL2Parser.Type_specifierContext):
        """Generate a generic type specifier."""
        self.print("visitType_specifier")
        self.level += 1

        type_ = self.visit(ctx.type_)
        if ctx.ptr:
            type_.ptr = ctx.ptr.text
        ret = type_
        self.level -= 1
        return ret

    def visitInteger_type(self, ctx: CoreDSL2Parser.Integer_typeContext):
        """Generate an integer type specifier."""
        self.print("visitInteger_type")
        self.level += 1

        signed = True
        width = None

        if ctx.signed is not None:
            signed = self.visit(ctx.signed)

        if ctx.size is not None:
            width = self.visit(ctx.size)

        if ctx.shorthand is not None:
            width = self.visit(ctx.shorthand)

        if isinstance(width, behav.BaseNode):
            width = width.generate(None)
        else:
            raise M2TypeError("width has wrong type")

        ret = arch.IntegerType(width, signed, None)
        self.level -= 1
        return ret

    def visitVoid_type(self, ctx: CoreDSL2Parser.Void_typeContext):
        """Generate a void type specifier."""
        self.print("visitVoid_type")
        self.level += 1

        ret = arch.VoidType(None)
        self.level -= 1
        return ret

    def visitBool_type(self, ctx: CoreDSL2Parser.Bool_typeContext):
        """Generate a bool type specifier. Aliases to unsigned<1>."""
        self.print("visitBool_type")
        self.level += 1

        ret = arch.IntegerType(1, False, None)
        self.level -= 1
        return ret

    def visitInteger_signedness(self, ctx: CoreDSL2Parser.Integer_signednessContext):
        """Generate integer signedness."""
        self.print("visitInteger_signedness")
        self.level += 1

        ret = SIGNEDNESS[ctx.children[0].symbol.text]
        self.level -= 1
        return ret

    def visitInteger_shorthand(self, ctx: CoreDSL2Parser.Integer_shorthandContext):
        """Lookup a shorthand type specifier."""
        self.print("visitInteger_shorthand")
        self.level += 1

        ret = behav.IntLiteral(SHORTHANDS[ctx.children[0].symbol.text])
        self.level -= 1
        return ret

    # Visit a parse tree produced by CoreDSL2Parser#deref_expression.
    def visitDeref_expression(self, ctx:CoreDSL2Parser.Deref_expressionContext):
        self.print("visitDeref_expression")
        self.level += 1
        ret = self.visitChildren(ctx)
        self.print("ref", ctx.ref.text)
        self.level -= 1
        return ret


def main():
    # data = InputStream(input(">>> "))
    # text = "res17[x] = (ZE17(Rs1.H[x]) - ZE17(Rs2.H[x])) u>> 1;"
    # text = "res17[x] = (ZE17(Rs1.H[x]) - ZE17(Rs2.H[x])) >> 1;"
    # text = "{ union myunion {int a; long b;}; union myunion x; int aa; aa = x->a;}"
    # text = "{ x = a->b; }"
    # text = "res17[x] = (ZE17(Rs1[x]) - ZE17(Rs2[x])) >> 1;"
    # text = "res17[x] = (ZE17(Rs1[x]) - ZE17(Rs2[x])) u>> 1;"
    # text = "res17[x] = (ZE17(Rs1[x]) - ZE17(Rs2[x])) u>> 1;\nRd[x] = res17[x][0];"
    text = """
 if (Rs2[5:0] s< 0) {
   sa = -Rs2[5:0];
   sa = (sa == 32)? 31 : sa;
   res[31:-1] = SE33(Rs1.W[x][31:sa-1]) + 1;
   Rd.W[x] = res[31:0];
 } else {
   sa = Rs2[4:0];
   res[(31+sa):0] = Rs1.W[x] u<< sa;
   if (res s> (2^31)-1) {
     res[31:0] = 0x7fffffff; OV = 1;
   } else if (res s< -2^31) {
     res[31:0] = 0x80000000; OV = 1;
   }
   Rd.W[x] = res.W[0];
 }
 """
    data = InputStream("{" + text + "}")
    print("data", data, dir(data))
    print()

    lexer = CoreDSL2Lexer(data)
    print("lexer", lexer, dir(lexer))
    print()

    stream = CommonTokenStream(lexer)
    print("stream", stream, dir(stream))
    print()

    parser = CoreDSL2Parser(stream)
    print("parser", parser, dir(parser))
    print()

    # tree = parser.expr()
    tree = parser.statement()
    print("tree", tree, dir(tree))
    print()

    visitor = MyVisitor()
    print("visitor", visitor, dir(visitor))
    print()

    output = visitor.visit(tree)
    print(output)

    sys.exit(0)


if __name__ == '__main__':
      main()
