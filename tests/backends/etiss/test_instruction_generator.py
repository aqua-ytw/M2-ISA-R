import pytest

import m2isar
from m2isar.backends.etiss.instruction_generator import generate_instructions, generate_fields, generate_instruction_callback
from m2isar.metamodel.utils import scalar_staticness, expr_simplifier


def _split_code(text):
    ret = []
    current = []
    for line in text.split("\n"):
        line = line.strip()
        if len(line) == 0:
            continue
        if "----" in line:
            ret.append("\n".join(current))
            current = []
        else:
            current.append(line)
    if len(current) > 0:
        ret.append("\n".join(current))
    splitted = ret
    assert len(splitted) == 7
    pre, misc, _, field, abc, code, post = splitted
    return pre, misc, _, field, abc, code, post


def _test_instruction(insn, memories, simplify=False, static_scalars=False):
    name = "TestCore"
    contributing_types = []
    template = None
    constants = {"XLEN": m2isar.metamodel.arch.Constant("XLEN", value=32, attributes={}, size=None, signed=False)}
    # memories = {'X': main_reg, 'PC': pc, 'MEM': main_mem, "CSR": csr_reg, "F": float_reg}
    memory_aliases = {}
    functions = {}
    instructions = {(insn.mask, insn.code): insn}
    instr_classes = set()
    core = m2isar.metamodel.arch.CoreDef(name, contributing_types, template, constants, memories, memory_aliases, functions, instructions, instr_classes)
    # static_scalars = True
    block_end_on = "none"

    instr_def = insn
    if simplify:
        m2isar.metamodel.patch_model(expr_simplifier)
        instr_def.operation.generate(None)
    if static_scalars:
        context = m2isar.metamodel.utils.ScalarStaticnessContext()
        m2isar.metamodel.patch_model(scalar_staticness)
        instr_def.operation.generate(context)
    # for instr_name, _, ext_name, templ_str in generate_instructions(core, static_scalars, block_end_on):
    #     # print("instr_name", instr_name)
    #     print("ext_name", ext_name)
    #     print("templ_str", templ_str)
    fields = generate_fields(core.constants['XLEN'].value, instr_def)
    callback_str = generate_instruction_callback(core, instr_def, fields, static_scalars, block_end_on)
    # print("callback_str", callback_str)
    return callback_str


@pytest.mark.parametrize("static_scalars", [False, True])
@pytest.mark.parametrize("simplify", [False, True])
def test_binop_int(tmp_path_factory, static_scalars, simplify):
    main_reg = m2isar.metamodel.arch.Memory("X", m2isar.metamodel.arch.RangeSpec(32), size=32, attributes={})
    memories = {"X": main_reg}
    op = m2isar.metamodel.behav.Operation(
        [
            m2isar.metamodel.behav.Assignment(
                m2isar.metamodel.behav.IndexedReference(
                    memories["X"],
                    m2isar.metamodel.behav.IntLiteral(0),
                ),
                m2isar.metamodel.behav.BinaryOperation(
                    m2isar.metamodel.behav.IntLiteral(42),
                    m2isar.metamodel.behav.Operator("+"),
                    m2isar.metamodel.behav.IntLiteral(24),
                ),
            )
        ]
    )
    insn = m2isar.metamodel.arch.Instruction("OP", attributes={}, encoding=[], disass="", operation=op)
    callback_str = _test_instruction(insn, memories, simplify=simplify, static_scalars=static_scalars)
    pre, misc, _, field, abc, code, post = _split_code(callback_str)
    lines = code.split("\n")
    temp = "\n".join(lines[-2:])
    assert temp == """cp.code() += "instr_exit_" + std::to_string(ic.current_address_) + ":\\n";
cp.code() += "cpu->instructionPointer = cpu->nextPc;\\n";"""
    code = "\n".join(lines[:-2])
    if simplify:
        assert code == """cp.code() += "((TestCore*)cpu)->X[0U] = 66U;\\n";"""
    else:
        assert code == """cp.code() += "((TestCore*)cpu)->X[0U] = " + std::to_string(42U + 24U) + "U;\\n";"""


def test_array(tmp_path_factory):
    pass


# @pytest.mark.parametrize("static_scalars", [False, True])
@pytest.mark.parametrize("static_scalars", [False])
# @pytest.mark.parametrize("simplify", [False, True])
@pytest.mark.parametrize("simplify", [False])
def test_lhs_slice_write(tmp_path_factory, static_scalars, simplify):
    main_reg = m2isar.metamodel.arch.Memory("X", m2isar.metamodel.arch.RangeSpec(32), size=32, attributes={})
    memories = {"X": main_reg}
    op = m2isar.metamodel.behav.Operation(
        [
            m2isar.metamodel.behav.Assignment(
                m2isar.metamodel.behav.SliceOperation(

                    # m2isar.metamodel.behav.IndexedReference(  # expr
                    #     memories["X"],
                    #     m2isar.metamodel.behav.IntLiteral(0),
                    # ),
                    m2isar.metamodel.behav.IntLiteral(17),  # left
                    m2isar.metamodel.behav.IntLiteral(11),  # right
                ),
                m2isar.metamodel.behav.IntLiteral(42),
            )
        ]
    )
    insn = m2isar.metamodel.arch.Instruction("OP", attributes={}, encoding=[], disass="", operation=op)
    callback_str = _test_instruction(insn, memories, simplify=simplify, static_scalars=static_scalars)
    pre, misc, _, field, abc, code, post = _split_code(callback_str)
    lines = code.split("\n")
    temp = "\n".join(lines[-2:])
    assert temp == """cp.code() += "instr_exit_" + std::to_string(ic.current_address_) + ":\\n";
cp.code() += "cpu->instructionPointer = cpu->nextPc;\\n";"""
    code = "\n".join(lines[:-2])
    print("code", code)
    if simplify:
        assert code == """cp.code() += "((TestCore*)cpu)->X[0U] = 66U;\\n";"""
    else:
        assert code == """cp.code() += "((TestCore*)cpu)->X[0U] = " + std::to_string(42U + 24U) + "U;\\n";"""
