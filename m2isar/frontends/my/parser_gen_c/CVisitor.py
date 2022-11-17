# Generated from C.g4 by ANTLR 4.11.1
import traceback
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .CParser import CParser
else:
    from CParser import CParser

# This class defines a complete generic visitor for a parse tree produced by CParser.

class CVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by CParser#primaryExpression.
    def visitPrimaryExpression(self, ctx:CParser.PrimaryExpressionContext):
        print("visitPrimaryExpression")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#genericSelection.
    def visitGenericSelection(self, ctx:CParser.GenericSelectionContext):
        print("visitGenericSelection")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#genericAssocList.
    def visitGenericAssocList(self, ctx:CParser.GenericAssocListContext):
        print("visitGenericAssocList")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#genericAssociation.
    def visitGenericAssociation(self, ctx:CParser.GenericAssociationContext):
        print("visitGenericAssociation")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#postfixExpression.
    def visitPostfixExpression(self, ctx:CParser.PostfixExpressionContext):
        traceback.print_stack()
        print("visitPostfixExpression")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#argumentExpressionList.
    def visitArgumentExpressionList(self, ctx:CParser.ArgumentExpressionListContext):
        print("visitArgumentExpressionList")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#unaryExpression.
    def visitUnaryExpression(self, ctx:CParser.UnaryExpressionContext):
        print("visitUnaryExpression")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#unaryOperator.
    def visitUnaryOperator(self, ctx:CParser.UnaryOperatorContext):
        print("visitUnaryOperator")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#castExpression.
    def visitCastExpression(self, ctx:CParser.CastExpressionContext):
        print("visitCastExpression")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#multiplicativeExpression.
    def visitMultiplicativeExpression(self, ctx:CParser.MultiplicativeExpressionContext):
        print("visitMultiplicativeExpression")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#additiveExpression.
    def visitAdditiveExpression(self, ctx:CParser.AdditiveExpressionContext):
        print("visitAdditiveExpression")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#shiftExpression.
    def visitShiftExpression(self, ctx:CParser.ShiftExpressionContext):
        print("visitShiftExpression")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#relationalExpression.
    def visitRelationalExpression(self, ctx:CParser.RelationalExpressionContext):
        print("visitRelationalExpression")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#equalityExpression.
    def visitEqualityExpression(self, ctx:CParser.EqualityExpressionContext):
        print("visitEqualityExpression")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#andExpression.
    def visitAndExpression(self, ctx:CParser.AndExpressionContext):
        print("visitAndExpression")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#exclusiveOrExpression.
    def visitExclusiveOrExpression(self, ctx:CParser.ExclusiveOrExpressionContext):
        print("visitExclusiveOrExpression")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#inclusiveOrExpression.
    def visitInclusiveOrExpression(self, ctx:CParser.InclusiveOrExpressionContext):
        print("visitInclusiveOrExpression")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#logicalAndExpression.
    def visitLogicalAndExpression(self, ctx:CParser.LogicalAndExpressionContext):
        print("visitLogicalAndExpression")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#logicalOrExpression.
    def visitLogicalOrExpression(self, ctx:CParser.LogicalOrExpressionContext):
        print("visitLogicalOrExpression")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#conditionalExpression.
    def visitConditionalExpression(self, ctx:CParser.ConditionalExpressionContext):
        print("visitConditionalExpression")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#assignmentExpression.
    def visitAssignmentExpression(self, ctx:CParser.AssignmentExpressionContext):
        print("visitAssignmentExpression")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#assignmentOperator.
    def visitAssignmentOperator(self, ctx:CParser.AssignmentOperatorContext):
        print("visitAssignmentOperator")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#expression.
    def visitExpression(self, ctx:CParser.ExpressionContext):
        print("visitExpression")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#constantExpression.
    def visitConstantExpression(self, ctx:CParser.ConstantExpressionContext):
        print("visitConstantExpression")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#declaration.
    def visitDeclaration(self, ctx:CParser.DeclarationContext):
        print("visitDeclaration")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#declarationSpecifiers.
    def visitDeclarationSpecifiers(self, ctx:CParser.DeclarationSpecifiersContext):
        print("visitDeclarationSpecifiers")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#declarationSpecifiers2.
    def visitDeclarationSpecifiers2(self, ctx:CParser.DeclarationSpecifiers2Context):
        print("visitDeclarationSpecifiers2")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#declarationSpecifier.
    def visitDeclarationSpecifier(self, ctx:CParser.DeclarationSpecifierContext):
        print("visitDeclarationSpecifier")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#initDeclaratorList.
    def visitInitDeclaratorList(self, ctx:CParser.InitDeclaratorListContext):
        print("visitInitDeclaratorList")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#initDeclarator.
    def visitInitDeclarator(self, ctx:CParser.InitDeclaratorContext):
        print("visitInitDeclarator")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#storageClassSpecifier.
    def visitStorageClassSpecifier(self, ctx:CParser.StorageClassSpecifierContext):
        print("visitStorageClassSpecifier")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#typeSpecifier.
    def visitTypeSpecifier(self, ctx:CParser.TypeSpecifierContext):
        print("visitTypeSpecifier")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#structOrUnionSpecifier.
    def visitStructOrUnionSpecifier(self, ctx:CParser.StructOrUnionSpecifierContext):
        print("visitStructOrUnionSpecifier")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#structOrUnion.
    def visitStructOrUnion(self, ctx:CParser.StructOrUnionContext):
        print("visitStructOrUnion")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#structDeclarationList.
    def visitStructDeclarationList(self, ctx:CParser.StructDeclarationListContext):
        print("visitStructDeclarationList")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#structDeclaration.
    def visitStructDeclaration(self, ctx:CParser.StructDeclarationContext):
        print("visitStructDeclaration")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#specifierQualifierList.
    def visitSpecifierQualifierList(self, ctx:CParser.SpecifierQualifierListContext):
        print("visitSpecifierQualifierList")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#structDeclaratorList.
    def visitStructDeclaratorList(self, ctx:CParser.StructDeclaratorListContext):
        print("visitStructDeclaratorList")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#structDeclarator.
    def visitStructDeclarator(self, ctx:CParser.StructDeclaratorContext):
        print("visitStructDeclarator")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#enumSpecifier.
    def visitEnumSpecifier(self, ctx:CParser.EnumSpecifierContext):
        print("visitEnumSpecifier")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#enumeratorList.
    def visitEnumeratorList(self, ctx:CParser.EnumeratorListContext):
        print("visitEnumeratorList")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#enumerator.
    def visitEnumerator(self, ctx:CParser.EnumeratorContext):
        print("visitEnumerator")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#enumerationConstant.
    def visitEnumerationConstant(self, ctx:CParser.EnumerationConstantContext):
        print("visitEnumerationConstant")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#atomicTypeSpecifier.
    def visitAtomicTypeSpecifier(self, ctx:CParser.AtomicTypeSpecifierContext):
        print("visitAtomicTypeSpecifier")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#typeQualifier.
    def visitTypeQualifier(self, ctx:CParser.TypeQualifierContext):
        print("visitTypeQualifier")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#functionSpecifier.
    def visitFunctionSpecifier(self, ctx:CParser.FunctionSpecifierContext):
        print("visitFunctionSpecifier")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#alignmentSpecifier.
    def visitAlignmentSpecifier(self, ctx:CParser.AlignmentSpecifierContext):
        print("visitAlignmentSpecifier")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#declarator.
    def visitDeclarator(self, ctx:CParser.DeclaratorContext):
        print("visitDeclarator")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#directDeclarator.
    def visitDirectDeclarator(self, ctx:CParser.DirectDeclaratorContext):
        print("visitDirectDeclarator")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#vcSpecificModifer.
    def visitVcSpecificModifer(self, ctx:CParser.VcSpecificModiferContext):
        print("visitVcSpecificModifer")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#gccDeclaratorExtension.
    def visitGccDeclaratorExtension(self, ctx:CParser.GccDeclaratorExtensionContext):
        print("visitGccDeclaratorExtension")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#gccAttributeSpecifier.
    def visitGccAttributeSpecifier(self, ctx:CParser.GccAttributeSpecifierContext):
        print("visitGccAttributeSpecifier")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#gccAttributeList.
    def visitGccAttributeList(self, ctx:CParser.GccAttributeListContext):
        print("visitGccAttributeList")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#gccAttribute.
    def visitGccAttribute(self, ctx:CParser.GccAttributeContext):
        print("visitGccAttribute")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#nestedParenthesesBlock.
    def visitNestedParenthesesBlock(self, ctx:CParser.NestedParenthesesBlockContext):
        print("visitNestedParenthesesBlock")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#pointer.
    def visitPointer(self, ctx:CParser.PointerContext):
        print("visitPointer")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#typeQualifierList.
    def visitTypeQualifierList(self, ctx:CParser.TypeQualifierListContext):
        print("visitTypeQualifierList")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#parameterTypeList.
    def visitParameterTypeList(self, ctx:CParser.ParameterTypeListContext):
        print("visitParameterTypeList")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#parameterList.
    def visitParameterList(self, ctx:CParser.ParameterListContext):
        print("visitParameterList")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#parameterDeclaration.
    def visitParameterDeclaration(self, ctx:CParser.ParameterDeclarationContext):
        print("visitParameterDeclaration")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#identifierList.
    def visitIdentifierList(self, ctx:CParser.IdentifierListContext):
        print("visitIdentifierList")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#typeName.
    def visitTypeName(self, ctx:CParser.TypeNameContext):
        print("visitTypeName")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#abstractDeclarator.
    def visitAbstractDeclarator(self, ctx:CParser.AbstractDeclaratorContext):
        print("visitAbstractDeclarator")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#directAbstractDeclarator.
    def visitDirectAbstractDeclarator(self, ctx:CParser.DirectAbstractDeclaratorContext):
        print("visitDirectAbstractDeclarator")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#typedefName.
    def visitTypedefName(self, ctx:CParser.TypedefNameContext):
        print("visitTypedefName")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#initializer.
    def visitInitializer(self, ctx:CParser.InitializerContext):
        print("visitInitializer")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#initializerList.
    def visitInitializerList(self, ctx:CParser.InitializerListContext):
        print("visitInitializerList")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#designation.
    def visitDesignation(self, ctx:CParser.DesignationContext):
        print("visitDesignation")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#designatorList.
    def visitDesignatorList(self, ctx:CParser.DesignatorListContext):
        print("visitDesignatorList")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#designator.
    def visitDesignator(self, ctx:CParser.DesignatorContext):
        print("visitDesignator")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#staticAssertDeclaration.
    def visitStaticAssertDeclaration(self, ctx:CParser.StaticAssertDeclarationContext):
        print("visitStaticAssertDeclaration")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#statement.
    def visitStatement(self, ctx:CParser.StatementContext):
        print("visitStatement")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#labeledStatement.
    def visitLabeledStatement(self, ctx:CParser.LabeledStatementContext):
        print("visitLabeledStatement")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#compoundStatement.
    def visitCompoundStatement(self, ctx:CParser.CompoundStatementContext):
        print("visitCompoundStatement")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#blockItemList.
    def visitBlockItemList(self, ctx:CParser.BlockItemListContext):
        print("visitBlockItemList")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#blockItem.
    def visitBlockItem(self, ctx:CParser.BlockItemContext):
        print("visitBlockItem")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#expressionStatement.
    def visitExpressionStatement(self, ctx:CParser.ExpressionStatementContext):
        print("visitExpressionStatement")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#selectionStatement.
    def visitSelectionStatement(self, ctx:CParser.SelectionStatementContext):
        print("visitSelectionStatement")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#iterationStatement.
    def visitIterationStatement(self, ctx:CParser.IterationStatementContext):
        print("visitIterationStatement")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#forCondition.
    def visitForCondition(self, ctx:CParser.ForConditionContext):
        print("visitForCondition")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#forDeclaration.
    def visitForDeclaration(self, ctx:CParser.ForDeclarationContext):
        print("visitForDeclaration")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#forExpression.
    def visitForExpression(self, ctx:CParser.ForExpressionContext):
        print("visitForExpression")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#jumpStatement.
    def visitJumpStatement(self, ctx:CParser.JumpStatementContext):
        print("visitJumpStatement")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#compilationUnit.
    def visitCompilationUnit(self, ctx:CParser.CompilationUnitContext):
        print("visitCompilationUnit")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#translationUnit.
    def visitTranslationUnit(self, ctx:CParser.TranslationUnitContext):
        print("visitTranslationUnit")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#externalDeclaration.
    def visitExternalDeclaration(self, ctx:CParser.ExternalDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#functionDefinition.
    def visitFunctionDefinition(self, ctx:CParser.FunctionDefinitionContext):
        print("visitFunctionDefinition")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#declarationList.
    def visitDeclarationList(self, ctx:CParser.DeclarationListContext):
        print("visitDeclarationList")
        return self.visitChildren(ctx)



del CParser
