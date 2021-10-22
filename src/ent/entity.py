from abc import abstractmethod, ABC
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from ent.EntKind import EntKind
from ent.behavior import Behavior
from ref.Ref import Ref

_EntityID = 0


class EntLongname:
    @property
    def longname(self) -> str:
        return '.'.join(self._scope)

    @property
    def name(self) -> str:
        return self._scope[-1]

    def __init__(self, scope: List[str]):
        self._scope = scope

    def __eq__(self, other: object):
        if isinstance(other, EntLongname) and len(other._scope) == len(self._scope):
            for lhs, rhs in zip(self._scope, other._scope):
                if lhs != rhs:
                    return False
            return True
        return False

    def __hash__(self):
        return hash(tuple(self._scope))


class Location:
    def append(self, name: str) -> "Location":
        return Location(self._scope + [name])

    def to_longname(self) -> EntLongname:
        return EntLongname(self._scope)

    def __init__(self, scope: Optional[List[str]] = None):
        if scope is None:
            scope = []
        self._scope: List[str] = scope

    def __eq__(self, other: object):
        if isinstance(other, Location) and len(other._scope) == len(self._scope):
            for lhs, rhs in zip(self._scope, other._scope):
                if lhs != rhs:
                    return False
            return True
        return False

    def __hash__(self):
        return hash(tuple(self._scope))

    @classmethod
    def global_name(cls, name: str) -> "Location":
        return Location([name])


@dataclass
class EntitySpan:
    file_path: Path
    start_line: int
    end_line: int
    start_col: int
    end_col: int


# Entity is the abstract domain of the Abstract Interpreter
class Entity(ABC):
    @classmethod
    def get_anonymous_ent(cls) -> "Entity":
        return _anonymous_ent

    def __init__(self, longname: EntLongname, span: EntitySpan, ent_type: "Optional[EntType]" = None):
        global _EntityID
        self._id = _EntityID
        # make sure the id is unique
        _EntityID += 1
        self._refs: List[Ref] = []
        self.behaviors: List[Behavior] = []
        self.longname = longname
        self.span = span
        self.ent_type = ent_type

    def refs(self) -> List[Ref]:
        return self._refs

    def set_refs(self, refs: List[Ref]):
        self._refs = refs

    @property
    def id(self) -> int:
        return self._id

    @abstractmethod
    def kind(self) -> EntKind:
        ...

    def add_ref(self, ref: Ref):
        # todo: should we remove reference with same representation?
        for ref_1 in self._refs:
            if ref_1 == ref:
                return
        self._refs.append(ref)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return other.longname == self.longname and other.span == self.span
        return False

    def direct_type(self) -> "EntType":
        from interp.enttype import EntType
        return EntType.get_bot()

    def __hash__(self):
        return hash((self.longname, self.span))


class Variable(Entity):
    def __init__(self, longname: EntLongname, span: EntitySpan, ent_type=EntType.get_bot()):
        super().__init__(longname, span, ent_type)

    def kind(self) -> EntKind:
        return EntKind.Variable


class Function(Entity):
    def __init__(self, longname: EntLongname, span: EntitySpan):
        super(Function, self).__init__(longname, span, None)

    def kind(self) -> EntKind:
        return EntKind.Function


class Module(Entity):
    def __init__(self, file_path: Path, span: EntitySpan):
        import os
        self.module_path = file_path
        path = os.path.normpath(str(file_path)[:-len(".py")])
        path_list = path.split(os.sep)
        longname = EntLongname(path_list)
        location = Location(path_list)
        super(Module, self).__init__(longname, span, self.direct_type())

    def kind(self) -> EntKind:
        return EntKind.Module

    @property
    def module_longname(self) -> EntLongname:
        return self.longname

    def direct_type(self) -> "ModuleType":
        return ModuleType.get_module_type()


def located_module_longname(span: EntitySpan, name: str) -> EntLongname:
    ...


class ModuleAlias(Entity):
    def __init__(self, file_path: Path, alias_span: EntitySpan, name: str):
        self.module_path = file_path
        located_module_longname(alias_span, name)
        super(ModuleAlias, self).__init__(located_module_longname(alias_span, name),
                                          alias_span,
                                          ModuleType.get_module_type())

    @property
    def module_longname(self) -> EntLongname:
        import os
        module_path = self.module_path
        path = os.path.normpath(str(module_path))
        path_list = path.split(os.sep)
        longname = EntLongname(path_list)
        return longname

    def kind(self) -> EntKind:
        return EntKind.ModuleAlias


class Alias(Entity):
    def __init__(self, longname: EntLongname, span: EntitySpan, ent: Entity):
        # todo:
        super(Alias, self).__init__(longname, )
        self.target_ent = ent

    def kind(self) -> EntKind:
        return EntKind.Alias


class Package(Entity):
    # todo: represent Package in proper way
    def __init__(self, file_path: Path):
        import os
        path = os.path.normpath(str(file_path))
        path_list = path.split(os.sep)
        longname = EntLongname(path_list)
        location = Location(path_list)
        super(Package, self).__init__(longname, location)

    def kind(self) -> EntKind:
        return EntKind.Package


class Class(Entity):
    def __init__(self, longname: EntLongname, span: EntitySpan):
        super(Class, self).__init__(longname, span, self.direct_type())

    def kind(self) -> EntKind:
        return EntKind.Class

    def direct_type(self) -> "EntType":
        return ConstructorType(self)


class UnknownVar(Entity):
    def __init__(self, name: str, span: EntitySpan):
        super(UnknownVar, self).__init__(EntLongname([name]), location)

    def kind(self) -> EntKind:
        return EntKind.UnknownVar


class UnknownModule(Module):
    def __init__(self, name: str, span: EntitySpan):
        super(UnknownModule, self).__init__(Path(f"{name}.py"), span)

    def kind(self) -> EntKind:
        return EntKind.UnknownModule


class Parameter(Entity):
    def __init__(self, longname: EntLongname, span: EntitySpan):
        super(Parameter, self).__init__(longname, span)

    def kind(self) -> EntKind:
        return EntKind.Parameter


class Anonymous(Entity):
    def __init__(self, longname: EntLongname, span: EntitySpan):
        super(Anonymous, self).__init__(longname, span)

    def kind(self) -> EntKind:
        return EntKind.Anonymous


class ClassAttribute(Entity):
    def __init__(self, longname: EntLongname, span: EntitySpan):
        super(ClassAttribute, self).__init__(longname, span)

    def kind(self) -> EntKind:
        return EntKind.ClassAttr


 
class ReferencedAttribute(Entity):
    def __init__(self, longname: EntLongname, span: EntitySpan, ent_type: "EntType" = None):
        super(ReferencedAttribute, self).__init__(longname, span, ent_type)

    def kind(self) -> EntKind:
        return EntKind.ReferencedAttr


# removed
class UnresolvedAttribute(Entity):
    def __init__(self, longname: EntLongname, span: EntitySpan, receiver_type):
        self.receiver_type = receiver_type
        super(UnresolvedAttribute, self).__init__(longname, location)

    def kind(self) -> EntKind:
        return EntKind.UnresolvedAttr


_anonymous_ent: Anonymous = Anonymous()

from interp.enttype import EntType, ModuleType, ConstructorType
