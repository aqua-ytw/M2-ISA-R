import pytest

import m2isar
from m2isar.frontends.coredsl2.parser import parse

def check_pc_increment(stmt):
    assert isinstance(stmt, m2isar.metamodel.behav.Assignment)
    assert isinstance(stmt.target, m2isar.metamodel.behav.NamedReference)
    assert stmt.target.reference.name == "PC"
    assert isinstance(stmt.expr, m2isar.metamodel.behav.BinaryOperation)
    assert isinstance(stmt.expr.left, m2isar.metamodel.behav.NamedReference)
    assert stmt.expr.left.reference.name == "PC"
    assert isinstance(stmt.expr.op, m2isar.metamodel.behav.Operator)
    assert stmt.expr.op.value == "+"
    assert isinstance(stmt.expr.right, m2isar.metamodel.behav.IntLiteral)
    assert stmt.expr.right.value == 4  # ?
    assert not stmt.expr.right.signed  # ?

def _gen_core(name="TestCore", sets=["TestSet"], xlen=32):
    provides_str = ("provides " + ", ".join(sets)) if len(sets) > 0 else ""
    return f"""
Core {name} {provides_str} {{
    architectural_state {{
        XLEN={xlen};
    }}
}}
"""


def _gen_set(name="TestSet", content=""):
    return f"""
InstructionSet {name} {{
    {content}
}}
"""


def _gen_architectural_state(content=None):
    if content is None:
        content = """
        unsigned int XLEN;
        unsigned int RFS = 32;
        register unsigned<XLEN> X[RFS] [[is_main_reg]];
        register unsigned<XLEN> PC [[is_pc]];
        extern char MEM[1 << XLEN] [[is_main_mem]];
        """
    return f"""
    architectural_state {{
        {content}
    }}
    """


def _gen_functions(content=None):
    if content is None:
        content = ""
    return f"""
    functions {{
        {content}
    }}
    """


def _gen_instructions(content=None):
    if content is None:
        content = ""
    return f"""
    instructions {{
        {content}
    }}
    """


def _gen_instruction_context(content):
    out = "// Test\n"
    out += _gen_set(content=(
        # _gen_architectural_state() + _gen_functions() + _gen_instructions(content)
        _gen_architectural_state() + _gen_instructions(content)
    ))
    out += _gen_core()
    return out


def _gen_function_context(content):
    out = "// Test\n"
    out += _gen_set(content=(
        # _gen_architectural_state() + _gen_functions(content) + _gen_instructions()
        _gen_architectural_state() + _gen_functions(content)
    ))
    out += _gen_core()
    return out


def _gen_function_context(content):
    out = "// Test\n"
    out += _gen_set(content=(
        # _gen_architectural_state(content) + _gen_functions() + _gen_instructions()
        _gen_architectural_state(content)
    ))
    out += _gen_core()
    return out


def _test_instructions(factory, content):
    directory = factory.mktemp("desc")
    top = directory / "top.core_desc"
    text = _gen_instruction_context(content)
    # print("text", text)
    top.write_text(text)
    _, modules = parse(top)
    # print(modules)
    assert len(modules) == 1
    assert "TestCore" in modules
    core = modules["TestCore"]
    # print(core, dir(core))
    return list(core.instructions.values())


def _test_instruction(factory, content):
    insns = _test_instructions(factory, content)
    assert len(insns) == 1
    insn = insns[0]
    assert insn.actual_size == 32
    assert insn.size == 32
    assert insn.ext_name == "TestSet"
    # print("actual_size", insn.actual_size)
    # print("attributes", insn.attributes)
    # print("code", insn.code)
    # print("disass", insn.disass)
    # print("encoding", insn.encoding)
    # print("ext_name", insn.ext_name)
    # print("fields", insn.fields)
    # print("mask", insn.mask)
    # print("name", insn.name)
    # print("operation", insn.operation)
    # print("scalars", insn.scalars)
    # print("size", insn.size)
    # print("throws", insn.throws)

    return insn


def _test_behavior(factory, content):
    return _test_instruction(factory, """
        OP {
            encoding: 0b0000000 :: rs2[4:0] :: rs1[4:0] :: 0b101 :: rd[4:0] :: 0b1111111;
            assembly: "{name(rd)}, {name(rs1)}, {name(rs2)}";
            behavior: {""" + content + """
            }
        }
    """)


# def test_foo(tmp_path_factory):
#     _test_instruction(tmp_path_factory, """
#         SBOX {
#             encoding: 0b0000000 :: rs2[4:0] :: rs1[4:0] :: 0b000 :: rd[4:0] :: 0b1111011;
#             assembly: "{name(rd)}, {name(rs1)}, {name(rs2)}";
#             behavior: {
#                 unsigned int data_i;
#                 // contents of array omitted for for brevity
#                 const unsigned char sbox[256] = { 0x63, 0x7c, 0};
#                 data_i = (unsigned int) Xreg[rs1];
#                 Xreg[rd] = sbox[data_i[31:24]] :: sbox[data_i[23:16]] :: sbox[data_i[15:8]] :: sbox[data_i[7:0]];
#             }
#         }
#     """)


# def test_foo2(tmp_path_factory):
#     _test_instruction(tmp_path_factory, """
#         vectorL {
#             encoding: 0b0000000 :: rs2[4:0] :: rs1[4:0] :: 0b000 :: rd[4:0] :: 0b1111011 ;
#             assembly: "{name(rd)}, {name(rs1)}";
#             behavior: {
#                 float xc = F_Ext[rs1];
#                 float yc = F_Ext[rs1];
#                 float sqdist = xc*xc + yc*yc;
#                 //...SQRT(sqdist) computation
#             }
#         }
#     """)

def test_foo3(tmp_path_factory):
    insn = _test_instruction(tmp_path_factory, """
        FOO {
            encoding: 0b0000000 :: rs2[4:0] :: rs1[4:0] :: 0b000 :: rd[4:0] :: 0b1111011;
            assembly: "{name(rd)}, {name(rs1)}, {name(rs2)}";
            behavior: {
                switch(rs1) {
                    case 1: break;
                    case 2: break;
                }
            }
        }
    """)
    # print(insn, dir(insn))
    assert insn.name == "FOO"
    op = insn.operation
    # print(op, dir(op))
    stmts = op.statements
    # print(stmts, dir(stmts))

@pytest.mark.parametrize("binop", ["+", "-", "*", "/", "%", ">>", "<<", "&", "|", "^"])
def test_binop_int(tmp_path_factory, binop):
    # TODO: use verlilog int literals
    insn = _test_instruction(tmp_path_factory, """
        OP {
            encoding: 0b0000000 :: rs2[4:0] :: rs1[4:0] :: 0b101 :: rd[4:0] :: 0b1111111;
            assembly: "{name(rd)}, {name(rs1)}, {name(rs2)}";
            behavior: {
                X[rd] = X[rs1] """ + binop + """ X[rs2];
            }
        }
    """)
    # print(insn, dir(insn))
    assert insn.name == "OP"

    # Check encoding
    assert "rd" in insn.fields.keys()
    assert "rs1" in insn.fields.keys()
    assert "rs2" in insn.fields.keys()
    assert len(insn.encoding) == 6

    assert isinstance(insn.encoding[0], m2isar.metamodel.arch.BitVal)
    assert insn.encoding[0].length == 7
    assert insn.encoding[0].value == 0

    assert isinstance(insn.encoding[1], m2isar.metamodel.arch.BitField)
    assert isinstance(insn.encoding[1].data_type, m2isar.metamodel.arch.DataType)
    assert insn.encoding[1].data_type == m2isar.metamodel.arch.DataType.U
    assert insn.encoding[1].name == "rs2"
    assert isinstance(insn.encoding[1].range, m2isar.metamodel.arch.RangeSpec)
    assert insn.encoding[1].range.lower == 0
    assert insn.encoding[1].range.upper == 4
    assert insn.encoding[1].range.length == 5

    assert isinstance(insn.encoding[2], m2isar.metamodel.arch.BitField)
    assert isinstance(insn.encoding[2].data_type, m2isar.metamodel.arch.DataType)
    assert insn.encoding[2].data_type == m2isar.metamodel.arch.DataType.U
    assert insn.encoding[2].name == "rs1"
    assert isinstance(insn.encoding[1].range, m2isar.metamodel.arch.RangeSpec)
    assert insn.encoding[2].range.lower == 0
    assert insn.encoding[2].range.upper == 4
    assert insn.encoding[2].range.length == 5

    assert isinstance(insn.encoding[3], m2isar.metamodel.arch.BitVal)
    assert insn.encoding[3].length == 3
    assert insn.encoding[3].value == 5

    assert isinstance(insn.encoding[4], m2isar.metamodel.arch.BitField)
    assert isinstance(insn.encoding[4].data_type, m2isar.metamodel.arch.DataType)
    assert insn.encoding[4].data_type == m2isar.metamodel.arch.DataType.U
    assert insn.encoding[4].name == "rd"
    assert isinstance(insn.encoding[1].range, m2isar.metamodel.arch.RangeSpec)
    assert insn.encoding[4].range.lower == 0
    assert insn.encoding[4].range.upper == 4
    assert insn.encoding[4].range.length == 5

    assert isinstance(insn.encoding[5], m2isar.metamodel.arch.BitVal)
    assert insn.encoding[5].length == 7
    assert insn.encoding[5].value == 127

    # Check assembly
    assert insn.disass == '"{name(rd)}, {name(rs1)}, {name(rs2)}"'  # TODO: deal with outer quotes?

    # Check behavior
    op = insn.operation
    # print(op, dir(op))
    stmts = op.statements
    # print(stmts, dir(stmts))
    first = stmts[0]
    check_pc_increment(stmts[0])
    stmt = stmts[1]

    assert isinstance(stmt, m2isar.metamodel.behav.Assignment)
    assert isinstance(stmt.target, m2isar.metamodel.behav.IndexedReference)
    assert stmt.target.reference.name == "X"
    assert isinstance(stmt.target.index, m2isar.metamodel.behav.NamedReference)
    assert stmt.target.index.reference.name == "rd"
    assert isinstance(stmt.expr, m2isar.metamodel.behav.BinaryOperation)
    assert isinstance(stmt.expr.left, m2isar.metamodel.behav.IndexedReference)
    assert stmt.expr.left.reference.name == "X"
    assert isinstance(stmt.expr.left.index, m2isar.metamodel.behav.NamedReference)
    assert stmt.expr.left.index.reference.name == "rs1"
    assert isinstance(stmt.expr.op, m2isar.metamodel.behav.Operator)
    assert isinstance(stmt.expr.right, m2isar.metamodel.behav.IndexedReference)
    assert stmt.expr.right.reference.name == "X"
    assert isinstance(stmt.expr.right.index, m2isar.metamodel.behav.NamedReference)
    assert stmt.expr.right.index.reference.name == "rs2"
    assert isinstance(stmt.expr.op, m2isar.metamodel.behav.Operator)
    assert stmt.expr.op.value == binop


    # stmts = stmts[1:]
    # for i, stmt in enumerate(stmts):
    #     print(i, "stmt", stmt)
    #     print("dir", dir(stmt))
    #     print("target", stmt.target, dir(stmt.target))
    #     if isinstance(stmt.target, m2isar.metamodel.behav.NamedReference):
    #         # print("ref", stmt.target.reference)
    #         print("ref.name", stmt.target.reference.name)
    #     elif isinstance(stmt.target, m2isar.metamodel.behav.IndexedReference):
    #         print("index", stmt.target.index)
    #         print("ref", stmt.target.reference)
    #         print("ref.name", stmt.target.reference.name)
    #         print("right", stmt.target.right)
    #     else:
    #         assert False
    #     print("expr", stmt.expr, dir(stmt.expr))
    #     if isinstance(stmt.expr, m2isar.metamodel.behav.BinaryOperation):
    #         print("left", stmt.expr.left, dir(stmt.expr.left))
    #         print("op", stmt.expr.op, dir(stmt.expr.op))
    #         print("op.value", stmt.expr.op.value)
    #         print("right", stmt.expr.right, dir(stmt.expr.right))
    #     print("")

# TODO
# encoding
# assembly
# duplicate?
# empty
# pc inc
# switch case
# float
# attrs
# spawn
# ++ --
# ...
# scoping

def test_array(tmp_path_factory):
    # TODO: use verlilog int literals
    insn = _test_behavior(tmp_path_factory, """
                unsigned<8> arr1[4];
                unsigned<8> arr2[2][4];
                unsigned<8> arr3[4] = {1, 2, 3, 4};
                unsigned<8> arr4[2][4] = {{1, 2, 3, 4}, {5, 6, 7, 8}};
                unsigned<8> arr5[4] = {42};
                unsigned<8> x;
                x = arr1[3];
                x = arr2[2][3];
                x = arr3[3];
                x = arr4[2][3];
    """)
    # print(insn, dir(insn))
    assert insn.name == "OP"


def test_union_basic_aligned(tmp_path_factory):
    # TODO: use verlilog int literals
    insn = _test_behavior(tmp_path_factory, """
                // basic, aligned
                union foo {
                    unsigned<8> AA;
                    signed<8> BB;
                };  // expected size: max(8, 8)=8
                // union foo myfoo;
                // union foo myfoo_init = {12};
                // union foo myfoo_init2 = {.BB=12};
    """)
    # print(insn, dir(insn))
    assert insn.name == "OP"


def test_union_basic_unaligned(tmp_path_factory):
    # TODO: use verlilog int literals
    insn = _test_behavior(tmp_path_factory, """
                union bar {
                    unsigned<12> AA;
                    unsigned<24> BB;
                };  // expected size: max(12, 24)=24
    """)
    # print(insn, dir(insn))
    assert insn.name == "OP"


def test_union_arrays_aligned(tmp_path_factory):
    # TODO: use verlilog int literals
    insn = _test_behavior(tmp_path_factory, """
                union baz {
                    unsigned<8> AA[4];
                    unsigned<4> BB[8];
                };  // expected size: max(4*8, 8*4)=32
    """)
    # print(insn, dir(insn))
    assert insn.name == "OP"


def test_union_arrays_unaligned(tmp_path_factory):
    # TODO: use verlilog int literals
    insn = _test_behavior(tmp_path_factory, """
                union foobar {
                    unsigned<12> AA[5];
                    unsigned<16> BB[3];
                };  // expected size: max(5*12, 4*16)=60
    """)
    # print(insn, dir(insn))
    assert insn.name == "OP"


def test_union_multi_arrays_unaligned(tmp_path_factory):
    # TODO: use verlilog int literals
    insn = _test_behavior(tmp_path_factory, """
                union foobaz {
                    unsigned<12> AA[5][4];
                    unsigned<16> BB[3][4];
                };  // expected size: undefined
    """)
    # print(insn, dir(insn))
    assert insn.name == "OP"


def test_union_mixed_aligned(tmp_path_factory):
    # TODO: use verlilog int literals
    insn = _test_behavior(tmp_path_factory, """
                union barfoo {
                    unsigned<32> AA;
                    unsigned<4> BB[8];
                };  // expected size: max(32, 8*4)=32
    """)
    # print(insn, dir(insn))
    assert insn.name == "OP"


def test_union_mixed_unaligned(tmp_path_factory):
    # TODO: use verlilog int literals
    insn = _test_behavior(tmp_path_factory, """
                union bazfoo {
                    unsigned<12> AA[5];
                    unsigned<48> BB;
                };  // expected size: max(5*12, 48)=60
    """)
    # print(insn, dir(insn))
    assert insn.name == "OP"


def test_struct(tmp_path_factory):
    # TODO: use verlilog int literals
    insn = _test_behavior(tmp_path_factory, """
    """)
    # print(insn, dir(insn))
    assert insn.name == "OP"


def test_lhs_indexed_write_slice(tmp_path_factory):
    # TODO: use verlilog int literals
    # TODO: try combination with arrays?
    insn = _test_behavior(tmp_path_factory, """
                unsigned<32> x = 32'b00001111000000001111111111110000;
                x[31:28] = 4'b1111;
                x[27:24] = 4'b0000;
                x[23:16] = 8'b11111111;
                x[16:4] = 12'b000000000000;
                x[3:0] = 4'b1111;
    """)
    # print(insn, dir(insn))
    assert insn.name == "OP"


@pytest.mark.xfail
@pytest.mark.parametrize("post", [False, True])
def test_pre_post_inc(tmp_path_factory, post):
    # TODO: use verlilog int literals
    op = "++" if post else "--"
    insn = _test_behavior(tmp_path_factory, """
                unsigned<8> i = 0;
                i""" + op + """;
    """)
    # print(insn, dir(insn))
    assert insn.name == "OP"


@pytest.mark.parametrize("binop", ["+", "-", "*", "/", "%", ">>", "<<", "&", "|", "^"])
def test_assignment_binop_int(tmp_path_factory, binop):
    # TODO: use verlilog int literals
    insn = _test_instruction(tmp_path_factory, """
        OP {
            encoding: 0b0000000 :: rs2[4:0] :: rs1[4:0] :: 0b101 :: rd[4:0] :: 0b1111111;
            assembly: "{name(rd)}, {name(rs1)}, {name(rs2)}";
            behavior: {
                X[rd] """ + binop + """= X[rs1];
            }
        }
    """)
    # print(insn, dir(insn))
    assert insn.name == "OP"
