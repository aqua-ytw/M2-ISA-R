import pytest

from m2isar.frontends.coredsl2.parser import parse

def _gen_core(name="TestCore", sets=["TestSet"], xlen=32):
    provides_str = ("provides " + ", ".join(sets)) if len(sets) > 0 else ""
    return f"""
Core {name} {provides_str}{{
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
    print("text", text)
    top.write_text(text)
    _, modules = parse(top)
    print(modules)
    assert len(modules) == 1
    assert "TestCore" in modules
    core = modules["TestCore"]
    print(core, dir(core))
    return list(core.instructions.values())


def _test_instruction(factory, content):
    a = _test_instructions(factory, content)
    assert len(a) == 1
    return a[0]




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
    print(insn, dir(insn))
    assert insn.name == "FOO"
    op = insn.operation
    print(op, dir(op))
    stmts = op.statements
    print(stmts, dir(stmts))

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
