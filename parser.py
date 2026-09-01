# -*- coding: utf-8 -*-


def dsl_parser(raw: bytes, definition: str, constraints: tuple[str, ...], assignments: tuple[str, ...],
               mapping: tuple[str, ...],
               endian: bool = True) -> (dict, int):
    mapping_table: dict = {}
    assignments_table: dict = {}
    raw_p: int = 0
    ele_p: int = 0
    def_p: int = 0
    raw_sz: int = len(raw)
    def_sz: int = len(definition)
    s: str = ""

    for assignment in assignments:
        sp: list = assignment.split('=')
        name: str = sp[0]
        val: int = int(eval(sp[1], {"raw": raw, "sum": sum}))
        assignments_table[name] = val

    for constraint in constraints:
        if not eval(constraint, {"raw": raw, "sum": sum}):
            return None

    while def_p < def_sz:
        s = ""
        if definition[def_p] == '(':
            while definition[def_p] != ')':
                s += definition[def_p]
                def_p += 1
            s += ')'
            def_p += 1
            constants_list: list = list(eval(s, {"raw": raw, "sum": sum})) if ',' in s else [
                eval(s, {"raw": raw, "sum": sum})]
            size = len(constants_list)
            if raw[raw_p:raw_p + size] != bytes(constants_list):
                return None
            mapping_table[mapping[ele_p]] = constants_list if size > 1 else constants_list[0]
            raw_p += size
            ele_p += 1

        elif definition[def_p].isalpha():
            c: str = definition[def_p].lower()
            if not c in "bwdq":
                raise TypeError(f"Unknown type {c}")
            length_mapping = {'b': 1, 'w': 2, 'd': 4, 'q': 8}
            length = length_mapping[c]
            times: int = 1
            def_p += 1
            if def_p < def_sz:
                if definition[def_p] == '{':
                    def_p += 1
                    while definition[def_p] != '}':
                        s += definition[def_p]
                        def_p += 1
                    def_p += 1
                    if s.isdigit():
                        times = int(s)
                    else:
                        if s[0].isdigit():
                            raise ValueError(f"{s} cannot as a variable name")
                        for ch in s[1:]:
                            if not (ch.isalnum() or ch == '_'):
                                raise ValueError(f"{s} cannot as a variable name")
                        times = assignments_table[s]
                else:
                    times: int = 1
            else:
                times: int = 1

            if times == 0:
                mapping_table[mapping[ele_p]] = []
            elif times == 1:
                end = raw_p + length
                if end > raw_sz:
                    return None
                val = int.from_bytes(raw[raw_p:end], "big" if endian else "little")
                mapping_table[mapping[ele_p]] = val
                raw_p = end

            elif times > 1:
                arr = []
                for i in range(times):
                    end = raw_p + length
                    if end > raw_sz:
                        return None
                    arr.append(int.from_bytes(raw[raw_p:end], "big" if endian else "little"))
                    raw_p = end
                mapping_table[mapping[ele_p]] = arr
            else:
                raise ValueError("The number in {} cannot below 0!")
            ele_p += 1

        elif definition[def_p].isspace():
            def_p += 1

        else:
            raise ValueError(f"Unknown character '{definition[def_p]}'")

    # if raw_p != raw_sz:
    #    return None

    if mapping_table:
        for key in mapping_table.keys():
            if isinstance(mapping_table[key], bytes):
                if len(mapping_table[key]) == 1:
                    mapping_table[key] = int.from_bytes(mapping_table[key])
                else:
                    mapping_table[key] = list(mapping_table[key])

    return mapping_table, raw_p
