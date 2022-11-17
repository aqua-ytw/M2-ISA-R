# SPDX-License-Identifier: Apache-2.0
#
# This file is part of the M2-ISA-R project: https://github.com/tum-ei-eda/M2-ISA-R
#
# Copyright (C) 2022
# Chair of Electrical Design Automation
# Technical University of Munich

import argparse
import logging
import pathlib
import pickle
import shutil
import time
import re

from m2isar.metamodel.arch import CoreDef, BitVal, BitField

from ...metamodel.utils.expr_preprocessor import (process_functions,
                                                  process_instructions)
# from . import BlockEndType
# from .architecture_writer import (write_arch_cmake, write_arch_cpp,
#                                   write_arch_gdbcore, write_arch_header,
#                                   write_arch_lib, write_arch_specific_cpp,
#                                   write_arch_specific_header,
#                                   write_arch_struct)
# from .instruction_writer import write_functions, write_instructions

REPLACE = {
    "val_?_12_3": "funct3",
    "val_?_25_7": "funct7",
    "val_?_20_12": "funct12",
    "val_?_20_5": "subf5",
    # "val_?_20_5": "funct5",
    "val_?_0_7": "opcode",
}


def process_instructions2(core):
    print("core", core, type(core), dir(core))
    instructions = core.instructions
    # print("instructions", instructions, type(instructions), dir(instructions))
    masks = []
    matches = []
    field_names = []
    all_disass = {}
    # encs = []
    encs = {}
    for key in instructions:
    # while False:
        # key = ""
        # print("instruction", instruction, type(instruction), dir(instruction))
        code, mask = key
        instruction = instructions[key]
        name = instruction.name
        # if name != "CLZ":
        #     continue
        print("instruction", instruction, type(instruction), dir(instruction))
        encoding = instruction.encoding
        fields = instruction.fields
        disass = instruction.disass
        if disass:
            disass = re.sub(r"name\(([^)]*)\)", r"\g<1>", re.sub(r"{(([^}:]*)(:.*)?)}", r"$\g<2>", disass))
        if disass in all_disass:
            all_disass[disass].append(name)
        else:
            all_disass[disass] = [name]
        # print("name", name)
        # print("code", code)
        # print("mask", mask)
        print("encoding", encoding, type(encoding), dir(encoding))
        t = []
        # start = -1
        start = 0
        for enc in encoding[::-1]:
            if isinstance(enc, BitVal):
                print("BitVal")
                n = None
                # if start == 0:
                #     if enc.value == 0b0011011:
                #         n = "OP-IMM-32"
                #     elif enc.value == 0b0111011:
                #         n = "OP-32"
                #     elif enc.value == 0b1011011:
                #         n = "custom-2"
                #     elif enc.value == 0b1111011:
                #         n = "custom-3"
                #     elif enc.value == 0b0010111:
                #         n = "AUIPC"
                #     elif enc.value == 0b0110111:
                #         n = "LUI"
                #     elif enc.value == 0b1010111:
                #         n = "OP-V"
                #     elif enc.value == 0b1110111:
                #         n = "OP-P"
                #     elif enc.value == 0b0010011:
                #         n = "OP-IMM"
                #     elif enc.value == 0b0110011:
                #         n = "OP"
                #     elif enc.value == 0b1010011:
                #         n = "OP-FP"
                #     elif enc.value == 0b1110011:
                #         n = "SYSTEM"
                #     elif enc.value == 0b0001111:
                #         n = "MISC-MEM"
                #     elif enc.value == 0b0101111:
                #         n = "AMO"
                #     elif enc.value == 0b1001111:
                #         n = "NMADD"
                #     elif enc.value == 0b1101111:
                #         n = "JAL"
                #     elif enc.value == 0b0001011:
                #         n = "custom-0"
                #     elif enc.value == 0b0001011:
                #         n = "custom-1"
                #     elif enc.value == 0b0001011:
                #         n = "NMSUB"
                #     elif enc.value == 0b0001011:
                #         n = "reserved"
                #     elif enc.value == 0b0000111:
                #         n = "LOAD-FP"
                #     elif enc.value == 0b0100111:
                #         n = "STORE-FP"
                #     elif enc.value == 0b1000111:
                #         n = "MSUB"
                #     elif enc.value == 0b1100111:
                #         n = "JALR"
                #     elif enc.value == 0b0000011:
                #         n = "LOAD"
                #     elif enc.value == 0b0100011:
                #         n = "STORE"
                #     elif enc.value == 0b1000011:
                #         n = "MADD"
                #     elif enc.value == 0b1100011:
                #         n = "BRANCH"
                if not n:
                    n = f"val_?_{start}_{enc.length}"
                if n in REPLACE:
                    n = REPLACE[n]
                start += enc.length
                t.insert(0, n)
            elif isinstance(enc, BitField):
                print("BitField")
                assert enc.name in fields
                n = f"{enc.name}_{fields[enc.name].data_type.name}_{start}_{enc.range.length}"
                field_names.append(n)
                start += enc.range.length
                t.insert(0, n)
            else:
                assert False
        t_str = "|".join(t)
        if t_str in encs:
            encs[t_str].append(name)
        else:
            encs[t_str] = [name]
        # encs.append(tuple(t))

        # print("fields", fields, type(fields), dir(fields))
        # print("disass", disass)
        # for field in fields:
        #     print("field", field)
        #     print("fields[field]", fields[field], type(fields[field]), dir(fields[field]))
        #     print("fields[field].data_type", fields[field].data_type, dir(fields[field].data_type))
        #     # input(">")
        #     if field not in field_names:
        #         start = -1
        #         # end = -1
        #         for enc in encoding[::-1]:
        #             if isinstance(enc, BitVal):
        #                 print("BitVal")
        #                 start += enc.length
        #             elif isinstance(enc, BitField):
        #                 print("BitField")
        #                 if enc.name == field:
        #                     field_names.append(f"{field}_{fields[field].data_type.name}_{start}_{enc.range.length}")
        #                     break
        #                 start += enc.range.length
        #             else:
        #                 assert False


        # print(f"#define MASK_{name} {hex(mask)}")
        # print(f"#define MATCH_{name} {hex(code)}")
        masks.append(f"#define MASK_{name} {hex(mask)}")
        matches.append(f"#define MATCH_{name} {hex(code)}")
        print()
    return masks, matches, field_names, all_disass, encs



def setup():
    """Setup a M2-ISA-R metamodel consumer. Create an argument parser, unpickle the model
    and generate output file structure.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('top_level', help="A .m2isarmodel file containing the models to generate.")
    # parser.add_argument('-s', '--separate', action='store_true', help="Generate separate .cpp files for each instruction set.")
    # parser.add_argument("--static-scalars", action="store_true", help="Enable crude static detection for scalars. WARNING: known to break!")
    # parser.add_argument("--block-end-on", default="none", choices=[x.name.lower() for x in BlockEndType], help="Force end translation blocks on no instructions, uncoditional jumps or all jumps.")
    # parser.add_argument("--log", default="info", choices=["critical", "error", "warning", "info", "debug"])
    args = parser.parse_args()

    # logging.basicConfig(level=getattr(logging, args.log.upper()))
    logger = logging.getLogger("dummy")

    top_level = pathlib.Path(args.top_level)
    abs_top_level = top_level.resolve()
    search_path = abs_top_level.parent.parent
    model_fname = abs_top_level

    if abs_top_level.suffix == ".core_desc":
        logger.warning(".core_desc file passed as input. This is deprecated behavior, please change your scripts!")
        search_path = abs_top_level.parent
        model_path = search_path.joinpath('gen_model')

        if not model_path.exists():
            raise FileNotFoundError('Models not generated!')
        model_fname = model_path / (abs_top_level.stem + '.m2isarmodel')

    spec_name = abs_top_level.stem
    # output_base_path = search_path.joinpath('gen_output')
    # output_base_path.mkdir(exist_ok=True)

    logger.info("loading models")

    with open(model_fname, 'rb') as f:
        models: "dict[str, CoreDef]" = pickle.load(f)

    # start_time = time.strftime("%a, %d %b %Y %H:%M:%S %z", time.localtime())

    # return (models, logger, output_base_path, spec_name, start_time, args)
    return (models, logger, spec_name, args)


def main():
    # models, logger, output_base_path, spec_name, start_time, args = setup()
    models, logger, spec_name, args = setup()

    all_masks = []
    all_matches = []
    all_field_names = []
    all_disass = {}
    all_encs = {}
    for core_name, core in models.items():
        logger.info("preprocessing model %s", core_name)
        # process_functions(core)
        # process_instructions(core)
        masks, matches, field_names, disass, encs = process_instructions2(core)
        all_masks.extend(masks)
        all_matches.extend(matches)
        all_field_names.extend(field_names)
        for key, value  in disass.items():
            if key in all_disass:
                all_disass[key].extend(value)
                all_disass[key] = list(set(all_disass[key]))
            else:
                all_disass[key] = value
        for key, value  in encs.items():
            if key in all_encs:
                all_encs[key].extend(value)
                all_encs[key] = list(set(all_encs[key]))
            else:
                all_encs[key] = value

    print()
    print(f"// MASKS len={len(all_masks)}")
    for mask in all_masks:
        print(mask)

    print()
    print(f"// MASKS len={len(all_matches)}")
    for match in all_matches:
        print(match)

    print()
    all_field_names = list(set(all_field_names))
    print(f"// FIELDS len={len(all_field_names)}")
    for field in all_field_names:
        print(field)

    print()
    print(f"// DISASS len={len(all_disass)}")
    for disass, used in all_disass.items():
        print(disass, used)

    print()
    # all_encs = list(set(all_encs))
    print(f"// ENCS len={len(all_encs)}")
    for enc, used in all_encs.items():
        print(enc, used)


    # for core_name, core in models.items():
    #     logger.info("processing model %s", core_name)
    #     # output_path = output_base_path / spec_name / core_name
    #     # try:
    #     #     output_path.mkdir(parents=True)
    #     # except FileExistsError:
    #     #     shutil.rmtree(output_path)
    #     #     output_path.mkdir(parents=True)

    #     # write_arch_struct(core, start_time, output_path)
    #     # write_arch_header(core, start_time, output_path)
    #     # write_arch_cpp(core, start_time, output_path, False)
    #     # write_arch_specific_header(core, start_time, output_path)
    #     # write_arch_specific_cpp(core, start_time, output_path)
    #     # write_arch_lib(core, start_time, output_path)
    #     # write_arch_cmake(core, start_time, output_path, args.separate)
    #     # write_arch_gdbcore(core, start_time, output_path)
    #     # write_functions(core, start_time, output_path, args.static_scalars)
    #     # write_instructions(core, start_time, output_path, args.separate, args.static_scalars, BlockEndType[args.block_end_on.upper()])

if __name__ == "__main__":
    main()
