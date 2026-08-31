# -*- coding: utf-8 -*-
from enum import IntEnum
from dataclasses import dataclass


class FrameType(IntEnum):
    NORMAL_INFORMATION_FRAME = 0
    EXTENDED_INFORMATION_FRAME = 1
    ACK_FRAME = 2
    NACK_FRAME = 3
    ERROR_FRAME = 4


@dataclass
class FrameDef:
    frame_type: FrameType
    definition: str
    constraints: tuple[str, ...]
    assignments: tuple[str, ...]
    mapping: tuple[str, ...]

    @property
    def type(self):
        return self.frame_type.name


NORMAL_INFORMATION_FRAME = FrameDef(
    FrameType.NORMAL_INFORMATION_FRAME,
    "B(0,0xff)BBBB{n}B(0)",
    ("(raw[3]+raw[4])&0xff==0", "sum(raw[5:-1])&0xff==0"),
    ("n=raw[3]-1",),
    ("preamble", "start_code", "len", "lcs", "tfi", "data", "dcs", "postamble")
)

EXTENDED_INFORMATION_FRAME = FrameDef(
    FrameType.EXTENDED_INFORMATION_FRAME,
    "B(0,0xff)(0xff)(0xff)BBBBB{n}B(0)",
    ("(raw[5]+raw[6]+raw[7])&0xff==0", "sum(raw[8:-1])&0xff==0"),
    ("n=raw[5]*256+raw[6]-1",),
    ("preamble", "start_code", "normal_length", "normal_length_checksum", "len_m", "len_l", "lcs", "tfi", "data", "dcs",
     "postamble")
)

ACK_FRAME = FrameDef(
    FrameType.ACK_FRAME,
    "(0)(0,0xff)(0,0xff)(0)",
    (),
    (),
    ("preamble", "start_code", "ack_code", "postamble")
)

NACK_FRAME = FrameDef(
    FrameType.ACK_FRAME,
    "(0)(0,0xff)(0xff,0)(0)",
    (),
    (),
    ("preamble", "start_code", "nack_code", "postamble")
)
