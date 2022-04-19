import operator as op
import ast
from dataclasses import dataclass, field
from typing import Union

@dataclass
class EquationSolver(ast.AST):

    ops: field(default_factory=dict) = None

    def __post_init__(self):
        self.ops = {ast.Add: op.add,
                    ast.Sub: op.sub,
                    ast.Mult: op.mul,
                    ast.Div: op.truediv,
                    ast.FloorDiv: op.floordiv,
                    ast.Pow: op.pow,
                    ast.BitXor: op.xor,
                    ast.BitAnd: op.and_,
                    ast.BitOr: op.or_,
                    ast.Mod: op.mod}

    def __eval(self, node: Union[ast.BinOp, ast.UnaryOp, ast.Num]):

        if isinstance(node,ast.Num):
            return node.n

        if isinstance(node,ast.BinOp):
            return self.ops[type(node.op)](self.__eval(node.left),self.__eval(node.right))

        if isinstance(node,ast.UnaryOp):
            return self.ops[type(node.op)](self.__eval(node.operand))

        raise TypeError(node)

    def solve(self, equation: str) -> Union[int,float]:
        return self.__eval(ast.parse(equation,mode="eval").body)


        
        
                    
                    
