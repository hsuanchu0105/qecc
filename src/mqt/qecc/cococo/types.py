# Copyright (c) 2023 - 2026 Chair for Design Automation, TUM
# All rights reserved.
#
# SPDX-License-Identifier: MIT
#
# Licensed under the MIT License

"""Type definitions."""

from typing import TypedDict, Literal
from dataclasses import dataclass
from dataclasses import replace

pos = tuple[int, int]
Gate = tuple[pos, pos]
FirstPart = Literal["control", "target"]
Layout = dict[str | int, pos | list[pos]]
VdpDict = dict[str | pos | Gate, list[pos]]


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