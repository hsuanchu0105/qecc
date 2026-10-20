# Copyright (c) 2023 - 2026 Chair for Design Automation, TUM
# All rights reserved.
#
# SPDX-License-Identifier: MIT
#
# Licensed under the MIT License

"""Type definitions."""

from typing import TypeAlias, TypedDict, Literal
from dataclasses import dataclass


pos: TypeAlias = tuple[int, int]          
Gate: TypeAlias = pos | tuple[pos, pos]
FirstPart = Literal["control", "target"]
Layout = dict[str | int, pos | list[pos]]
VdpDict = dict[str | Gate, list[pos]]


class HistoryTemp(TypedDict, total=False):  # pragma: no cover
    """Type for history dictionaries."""

    scores: list[int]
    layout_init: dict[str | int, pos | list[pos]]
    layout_final: dict[str | int, pos | list[pos]]

@dataclass
class RouteInfo:
    gate: Gate
    path: tuple[pos, ...]
    ancilla_idx: int
    first_part: FirstPart = "control"
    # Allowed steiner T-junction index range [junction_lo, junction_hi] on `path`:
    junction_lo: int | None = None
    junction_hi: int | None = None

    @property
    def ancilla(self) -> pos:
        return self.path[self.ancilla_idx]

    @property
    def control(self) -> tuple[pos, ...]:
        return self.path[: self.ancilla_idx + 1]

    @property
    def target(self) -> tuple[pos, ...]:
        return self.path[self.ancilla_idx :]

    @property
    def subpath1(self) -> tuple[pos, ...]:
        """The part routed first."""
        if self.first_part == "control":
            return self.control
        return self.target

    @property
    def subpath2(self) -> tuple[pos, ...]:
        """The part routed second."""
        if self.first_part == "control":
            return self.target
        return self.control
