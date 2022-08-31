#!/usr/bin/env python3

import io
from typing import Any, Iterable, TypeVar


TVar = TypeVar("TVar")

class tqdm:
    def __init__(
        self,
        iterable: None | Iterable[TVar] = ...,
        desc: None | str = ...,
        total: None | int | float = ...,
        leave: None | bool = ...,
        file: None | io.TextIOWrapper | io.StringIO = ...,
        ncols: None | int = ...,
        mininterval: None | float = ...,
        maxinterval: None | float = ...,
        miniters: None | int | float = ...,
        ascii: None | bool | str = ...,
        disable: None | bool = ...,
        unit: None | str = ...,
        unit_scale: None | bool | int | float = ...,
        dynamic_ncols: None | bool = ...,
        smoothing: None | float = ...,
        bar_format: None | str = ...,
        initial: None | int | float = ...,
        position: None | int = ...,
        postfix: None | dict[Any, Any] = ...,
        unit_divisor: None | float = ...,
        write_bytes: None | bool = ...,
        lock_args: None | tuple[Any] = ...,
        nrows: None | int = ...,
        colour: None | str = ...,
        delay: None | float = ...,
        gui: None | bool = ...,
        **kwargs: Any) -> None: ...
