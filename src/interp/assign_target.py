import ast
from _ast import AST
from abc import ABC
from dataclasses import dataclass
from typing import List, Tuple, TypeAlias, Callable, Optional

from ent.EntKind import RefKind
from ent.entity import Entity, Variable, Parameter, UnknownVar, UnresolvedAttribute, ClassAttribute, Class
from interp.aval import UseAvaler, SetAvaler, AbstractValue, MemberDistiller
from interp.enttype import EntType, ClassType
from interp.env import EntEnv
from interp.manager_interp import ModuleDB, PackageDB
from ref.Ref import Ref


class PatternBuilder:

    def visit(self, node: ast.expr) -> "Target":
        method = 'visit_' + node.__class__.__name__
        visitor: Callable[[ast.expr], "Target"] = getattr(self, method, self.visit_Lvalue)
        return visitor(node)

    def visit_Attribute(self, node: ast.Attribute) -> "LvalueTar":
        return LvalueTar(node)

    def visit_Lvalue(self, node: ast.expr) -> "LvalueTar":
        return LvalueTar(node)

    def visit_List(self, node: ast.List) -> "ListTar":
        tar_list: List[Target] = []
        for e in node.elts:
            tar_list.append(self.visit(e))
        return ListTar(tar_list)

    def visit_Tuple(self, node: ast.Tuple) -> "TupleTar":
        tar_list: List[Target] = []
        for e in node.elts:
            tar_list.append(self.visit(e))
        return TupleTar(tar_list)

    def visit_Starred(self, node: ast.Starred) -> "StarTar":
        return StarTar(self.visit(node.value))



class Target(ABC):
    ...


# `Tar` stands for target
@dataclass
class TupleTar(Target):
    tar_list: List[Target]


@dataclass
class LvalueTar(Target):
    lvalue_expr: ast.expr


@dataclass
class ListTar(Target):
    tar_list: List[Target]


@dataclass
class StarTar(Target):
    target: Target


def build_target(tar_expr: ast.expr) -> Target:
    return PatternBuilder().visit(tar_expr)


def dummy_unpack(_: AbstractValue) -> MemberDistiller:
    def wrapper(_: int) -> AbstractValue:
        return [(Entity.get_anonymous_ent(), EntType.get_bot())]

    return wrapper


def dummy_iter(_: AbstractValue) -> AbstractValue:
    return [(Entity.get_anonymous_ent(), EntType.get_bot())]


def assign_semantic(tar_ent: Entity, value_type: EntType, frame_entities: List[Tuple[Entity, EntType]],
                    ctx: "InterpContext"):
    # depends on which kind of the context entity is, define/set/use variable entity of the environment or
    # the current
    target_lineno, target_col_offset = ctx.coordinate
    # target should be the entity which the target_expr could possiblelly eval to
    if isinstance(tar_ent, Variable) or isinstance(tar_ent, Parameter):
        # if target entity is a defined variable or parameter, just add the target new type to the environment
        # env.add(target, value_type)
        frame_entities.append((tar_ent, value_type))
        # add_target_var(target, value_type, env, self.dep_db)
        # self.dep_db.add_ref(env.get_ctx(), Ref(RefKind.DefineKind, target, target_expr.lineno, target_expr.col_offset))
        ctx.env.get_ctx().add_ref(Ref(RefKind.SetKind, tar_ent, target_lineno, target_col_offset))
        # record the target assign to target entity
    # if the target is a newly defined variable
    elif isinstance(tar_ent, UnknownVar):
        ctx_ent = ctx.env.get_ctx()
        location = ctx.env.get_scope().get_location()
        location = location.append(tar_ent.longname.name)
        if isinstance(ctx_ent, Class):
            new_attr = ClassAttribute(location.to_longname(), location)
            frame_entities.append((new_attr, value_type))
            ctx.current_db.add_ent(new_attr)
            ctx_ent.add_ref(Ref(RefKind.DefineKind, new_attr, target_lineno, target_col_offset))
            ctx_ent.add_ref(Ref(RefKind.SetKind, new_attr, target_lineno, target_col_offset))
        else:
            # newly defined variable
            new_var = Variable(location.to_longname(), location)
            frame_entities.append((new_var, value_type))
            ctx.current_db.add_ent(new_var)
            ctx.env.get_ctx().add_ref(Ref(RefKind.DefineKind, new_var, target_lineno, target_col_offset))
            ctx.env.get_ctx().add_ref(Ref(RefKind.SetKind, new_var, target_lineno, target_col_offset))
            # record the target assign to target entity
            # do nothing if target is not a variable, record the possible Set relation in add_ref method of DepDB
    elif isinstance(tar_ent, UnresolvedAttribute):
        if isinstance(tar_ent.receiver_type, ClassType):
            new_location = tar_ent.receiver_type.class_ent.location.append(tar_ent.longname.name)
            new_attr = ClassAttribute(new_location.to_longname(), new_location)
            ctx.current_db.add_ent(new_attr)
            tar_ent.receiver_type.class_ent.add_ref(
                Ref(RefKind.DefineKind, new_attr, target_lineno, target_col_offset))
            ctx.env.get_ctx().add_ref(Ref(RefKind.SetKind, new_attr, target_lineno, target_col_offset))
    else:
        ctx.env.get_ctx().add_ref(Ref(RefKind.SetKind, tar_ent, target_lineno, target_col_offset))


def abstract_assign(lvalue: AbstractValue, rvalue: AbstractValue, ctx: "InterpContext") -> None:
    for _, value_type in rvalue:
        frame_entities: List[Tuple[Entity, EntType]] = []
        for target, _ in lvalue:
            assign_semantic(target, value_type, frame_entities, ctx)
        ctx.env.get_scope().add_continuous(frame_entities)


def unpack_list(tar_list: List[Target], distiller: MemberDistiller, ctx: "InterpContext") -> None:
    for i, tar in enumerate(tar_list):
        rvalue = distiller(i)
        unpack_semantic(tar, rvalue, ctx)


def unpack_semantic(target: Target, rvalue: AbstractValue, ctx: "InterpContext") -> None:
    set_avaler = SetAvaler(ctx.package_db, ctx.current_db)
    distiller = dummy_unpack(rvalue)
    # replace pattern match to use mypy
    # match target:
    #     case LvalueTar(lvalue_expr):
    #         lvalue: AbstractValue = set_avaler.aval(lvalue_expr, ctx.env)
    #         abstract_assign(lvalue, rvalue, ctx)
    #     case TupleTar(tar_list):
    #         unpack_list(tar_list, distiller, ctx)
    #     case ListTar(tar_list):
    #         unpack_list(tar_list, distiller, ctx)
    #     case StarTar(tar):
    #         unpack_list([tar], distiller, ctx)

    if isinstance(target, LvalueTar):
        lvalue: AbstractValue = set_avaler.aval(target.lvalue_expr, ctx.env)
        abstract_assign(lvalue, rvalue, ctx)
    elif isinstance(target, TupleTar):
        unpack_list(target.tar_list, distiller, ctx)
    elif isinstance(target, ListTar):
        unpack_list(target.tar_list, distiller, ctx)
    elif isinstance(target, StarTar):
        unpack_list([target.target], distiller, ctx)


def assign2target(target: Target, rvalue_expr: Optional[ast.expr], ctx: "InterpContext") -> None:
    avaler = UseAvaler(ctx.package_db, ctx.current_db)
    rvalue: AbstractValue
    if rvalue_expr is None:
        rvalue = [(Entity.get_anonymous_ent(), EntType.get_bot())]
    else:
        rvalue = avaler.aval(rvalue_expr, ctx.env)
    unpack_semantic(target, rvalue, ctx)


from interp.checker import InterpContext

if __name__ == '__main__':
    tree = ast.parse("*[(x, y), y]")
    tar = build_target(tree.body[0].value) # type: ignore
    print(tar)
