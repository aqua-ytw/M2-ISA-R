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

from m2isar.metamodel.arch import CoreDef, DataType, BitField, BitVal
from m2isar.metamodel.behav import FunctionCall

from . import BlockEndType, instruction_transform, instruction_utils
from ...metamodel import patch_model


def get_type_str(dtype, size):
    type_str = ""
    if dtype == DataType.S:
        type_str += "signed"
    elif dtype == DataType.U:
        type_str += "unsigned"
    elif dtype == DataType.NONE:
        type_str += "void"
    else:
        print("type", dtype)
        raise NotImplementedError
    if dtype in [DataType.S, DataType.U]:
        type_str += f"<{size}>"
    return type_str


def setup():
    """Setup a M2-ISA-R metamodel consumer. Create an argument parser, unpickle the model
    and generate output file structure.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('top_level', help="A .m2isarmodel file containing the models to generate.")
    parser.add_argument('-s', '--separate', action='store_true', help="Generate separate .cpp files for each instruction set.")
    parser.add_argument("--static-scalars", action="store_true", help="Enable crude static detection for scalars. WARNING: known to break!")
    parser.add_argument("--block-end-on", default="none", choices=[x.name.lower() for x in BlockEndType], help="Force end translation blocks on no instructions, uncoditional jumps or all jumps.")
    parser.add_argument("--log", default="info", choices=["critical", "error", "warning", "info", "debug"])
    args = parser.parse_args()

    logging.basicConfig(level=getattr(logging, args.log.upper()))
    logger = logging.getLogger("etiss_writer")

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
    output_base_path = search_path.joinpath('gen_output')
    output_base_path.mkdir(exist_ok=True)

    logger.info("loading models")

    with open(model_fname, 'rb') as f:
        models: "dict[str, CoreDef]" = pickle.load(f)

    start_time = time.strftime("%a, %d %b %Y %H:%M:%S %z", time.localtime())

    return (models, logger, output_base_path, spec_name, start_time, args)

def main():
    models, logger, output_base_path, spec_name, start_time, args = setup()

    print("AAA")
    for core_name, core in models.items():
        logger.info("preprocessing model %s", core_name)
        patch_model(instruction_transform)
        # print("core_name, core", core_name, core)
        # print("dir(core)", dir(core))
        # print("core.constants", core.constants)
        print(f"InstructionSet ISA {{")
        print("    architectural_state {")

        print("    }")
        print("    functions {")
        for func_name, func in core.functions.items():
            # print("f", func_name, func, dir(func))
            # print("f.operation", func.operation, dir(func.operation))
            # print("f.operation.generate", func.operation.generate())
            core_default_width = core.constants['XLEN'].value
            # print("f.operation.statements", func.operation.statements)
            # print("f.ext_name", func.ext_name)
            # TODO: put them in respective ISA
            if len(func.scalars) > 0:
                print("f.scalars", func.scalars)
                # for scalar in func.scalars:
                raise NotImplementedError
            # bprint("f.static", func.static)
            # TODO: static?
            if func.throws:
                print("f.throws", func.throws)
                raise NotImplementedError
            # input(">")
            # f raise <Function object>: name=raise, size=32, actual_size=32, data_type=DataType.S ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_size', 'actual_size', 'args', 'attributes', 'data_type', 'ext_name', 'extern', 'name', 'operation', 'scalars', 'size', 'static', 'throws']
            # print("func.args", func.args)
            args_str = ""
            for name, arg in func.args.items():
                # print("arg", arg, dir(arg))
                type_str = get_type_str(arg.data_type, arg.size)
                if len(args_str) > 0:
                    args_str += ", "
                args_str += type_str
                if arg.name:
                    args_str += arg.name
            # print("func.attributes", func.attributes)
            attrs_str = ""
            if len(func.attributes) > 0:
                attrs_str += " [["
                for attr, value in func.attributes.items():
                    # print("attr", attr, dir(attr), attr.name, attr.value)
                    if len(attrs_str) > 3:
                        attrs_str += ","
                    attrs_str += attr.name.lower()
                    if len(value) > 0:
                        assert len(value) == 1
                        value = value[0]
                        # print("value", value, dir(value))
                        attrs_str += f"={value.value}"
                attrs_str += "]]"
            prefix = ""
            if func.extern:
                prefix += "extern "
            type_str = get_type_str(func.data_type, func.size)
            prefix += type_str
            print("        " + f"{prefix} {func_name} ({args_str}){attrs_str}", end="")
            if not func.operation or func.extern:
                print(";")
            else:
                print(" {")
                context = instruction_utils.TransformerContext(core.constants, core.memories, core.memory_aliases, func.args, func.attributes, core.functions, 0, core_default_width, core_name, False, True)
                out_code = func.operation.generate(context)
                # print("out_code", out_code)
                print("\n".join(["            " + line for line in out_code.split("\n")]))
                print("        }")

        print("    }")
        print()
        print("}")
        print(f"Core {core_name} provides ISA {{")
        print("    architectural_state {")
        for name, const in core.constants.items():
            print("        " + f"{name} = {const.value}")
        print("    }")
        print("}")
        # print("core.contributing_types", core.contributing_types)
        # print("core.instr_classes", core.instr_classes)
        # print("core.instructions", core.instructions)
        for key, instr in core.instructions.items():
            out = ""
            out += instr.name
            if len(instr.attributes) > 0:
                attrs_str = " [["
                for attr, value in instr.attributes.items():
                    # print("attr", attr, dir(attr), attr.name, attr.value)
                    if len(attrs_str) > 3:
                        attrs_str += ","
                    attrs_str += attr.name.lower()
                    if len(value) > 0:
                        assert len(value) == 1
                        value = value[0]
                        print("value", value, dir(value))
                        if isinstance(value, FunctionCall):
                            print("args", value.args)
                            print("ref_or_name", value.ref_or_name)
                            raise NotImplementedError
                        else:
                            attrs_str += f"={value.value}"
                attrs_str += "]]"
                out += attrs_str
            out += " {\n"
            if instr.encoding:
                # print("enc", instr.encoding,  dir(instr.encoding))
                # print("fields", instr.fields, dir(instr.fields))
                enc_str = ""
                for e in instr.encoding:
                    print("e", e, type(e), dir(e))
                    if len(enc_str) > 0:
                        enc_str += " :: "
                    if isinstance(e, BitField):
                        enc_str += f"{e.name}[{e.range.upper}:{e.range.lower}]"
                    elif isinstance(e, BitVal):
                        enc_str += f"{e.length}'b{bin(e.value)}"
                    else:
                        raise RuntimeError("Unexpected field in ecoding")
                out += f"    encoding: {enc_str}\n"
            if instr.disass:
                out += f"    assembly: {instr.disass}\n"
            if instr.operation:
                out += "    behavior: {\n"
                if instr.scalars:
                    assert instr.operation
                    # print("instr.scalars", instr.scalars)
                    for scalar_name, scalar in instr.scalars.items():
                        # print("scalar_name", scalar_name)
                        # print("scalar", scalar, dir(scalar))
                        type_str = get_type_str(scalar.data_type, scalar.size)
                        out += f"{type_str} {scalar.name}"
                        if scalar.value:
                            out += " = {scalar.value}"
                        if scalar.static:
                            raise NotImplementedError("static scalar")
                        out += ";\n"
                context = instruction_utils.TransformerContext(core.constants, core.memories, core.memory_aliases, instr.fields, instr.attributes, core.functions, "?", core_default_width, core_name, False)
                out_code = instr.operation.generate(context)
                out += "\n".join(["        " + line for line in out_code.split("\n")])
                out += "\n"
                out += "    }\n"
            print("\n".join(["        " + line for line in out.split("\n")]))

            # input("<>")
        break  # TODO: remove

    print("BBB")
    for core_name, core in models.items():
        print("core_name, core", core_name, core)
        logger.info("processing model %s", core_name)
        output_path = output_base_path / spec_name / core_name
        try:
            output_path.mkdir(parents=True)
        except FileExistsError:
            shutil.rmtree(output_path)
            output_path.mkdir(parents=True)


if __name__ == "__main__":
    main()
