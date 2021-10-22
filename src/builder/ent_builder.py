import ast

from dep.DepDB import DepDB


class EntityBuilder:
    def __init__(self, dep_db: DepDB):
        self._dep_db = dep_db

    def ent_build(self, expr: ast.expr, env: EntEnv) -> List[Tuple[Entity, EntType]]:
        """Visit a node."""
        method = 'build_' + expr.__class__.__name__
        visitor = getattr(self, method, self.generic_aval)
        return visitor(expr, env)

    def generic_aval(self, expr: ast.expr, env: EntEnv) -> List[Tuple[Entity, EntType]]:
        """Called if no explicit visitor function exists for a node."""
        ret: EntType = EntType.get_bot()
        for field, value in ast.iter_fields(expr):
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, ast.expr):
                        avalue = self.aval(item, env)
                        for _, ent_type in avalue:
                            ret = ret.join(ent_type)
            elif isinstance(value, ast.expr):
                avalue = self.aval(value, env)
                for _, ent_type in avalue:
                    ret = ret.join(ent_type)