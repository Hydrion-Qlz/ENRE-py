import ast
from typing import Optional

from enre.ent.entity import UnknownVar
from enre.analysis.assign_target import assign_semantic
from enre.analysis.analyze_expr import AbstractValue, UseAvaler
from enre.analysis.analyze_stmt import InterpContext
from enre.analysis.enttype import ConstructorType, EntType


def abstract_capture(name: str, err_constructor: AbstractValue, ctx: "InterpContext") -> None:
    frame_entities: AbstractValue = []
    new_var_ent = UnknownVar.get_unknown_var(name)
    for ent, ent_type in err_constructor:
        if isinstance(ent_type, ConstructorType):
            assign_semantic(new_var_ent, ent_type.to_class_type(), frame_entities, ctx)
        else:
            assign_semantic(new_var_ent, EntType.get_bot(), frame_entities, ctx)
    ctx.env.get_scope().add_continuous(frame_entities)


def handler_semantic(name: Optional[str], error_expr: ast.Expr, ctx: "InterpContext") -> None:
    use_avaler = UseAvaler(ctx.package_db, ctx.current_db)
    err_constructor = use_avaler.aval(error_expr.value, ctx.env)
    if name is not None:
        abstract_capture(name, err_constructor, ctx)