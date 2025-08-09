from typing import Callable, Dict, Any
import logging
import copy

Transform = Callable[[Any, Any], Any] #(df, args) -> df
GLOBAL_REGISTRY: Dict[str, Transform] = {}

def register_transform(name: str, *, registry: Dict[str, Transform] = GLOBAL_REGISTRY):
    def wrapper(func: Transform) -> Transform:
        if name in registry:
            logging.warning(f"Transform: {name} already registered; overriding.")
        registry[name] = func
        return func
    return wrapper

def build_registry(
        *,
        base: Dict[str, Transform] = GLOBAL_REGISTRY,
        include: list[str] | None = None,
        exclude: list[str] | None = None,
        overrides: Dict[str, Transform] | None = None,
) -> Dict[str, Transform]:
    '''Create a project-specific registry by filtering/overriding the global one.'''
    reg = copy.copy(base)
    if include is not None:
        reg = {k: v for k, v in reg.items() if k in include}
    if exclude:
        for k in exclude:
            reg.pop(k, None)
    if overrides:
        reg.update(overrides)
    return reg