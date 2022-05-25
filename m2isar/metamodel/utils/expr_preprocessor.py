import logging

from ... import M2ValueError
from .. import arch, patch_model
from . import (expr_simplifier, function_staticness, function_throws,
               scalar_staticness)

logger = logging.getLogger("preprocessor")

def process_functions(core: arch.CoreDef):
	for fn_name, fn_def in core.functions.items():
		patch_model(expr_simplifier)
		logger.debug("simplifying expressions for fn %s", fn_name)
		fn_def.operation.generate(None)

		patch_model(function_throws)
		logger.debug("checking throws for fn %s", fn_name)
		throws = fn_def.operation.generate(None)
		fn_def.throws = throws or arch.FunctionAttribute.ETISS_EXC_ENTRY in fn_def.attributes

		patch_model(scalar_staticness)
		logger.debug("examining scalar staticness for fn %s", fn_name)
		fn_def.operation.generate(None)

		patch_model(function_staticness)
		logger.debug("examining function staticness for fn %s", fn_name)

		if arch.FunctionAttribute.ETISS_NEEDS_ARCH in fn_def.attributes and arch.FunctionAttribute.ETISS_STATICFN in fn_def.attributes:
			raise M2ValueError("etiss_needs_arch and etiss_staticfn not allowed together, in function %s", fn_name)

		if not fn_def.extern and (arch.FunctionAttribute.ETISS_NEEDS_ARCH in fn_def.attributes or arch.FunctionAttribute.ETISS_STATICFN in fn_def.attributes):
			raise M2ValueError("etiss_needs_arch and etiss_staticfn only allowed for extern functions, in function %s", fn_name)

		if fn_def.extern:
			if arch.FunctionAttribute.ETISS_STATICFN in fn_def.attributes:
				fn_def.static = True

		else:
			ret = fn_def.operation.generate(None)
			fn_def.static = ret

def process_instructions(core: arch.CoreDef):
	for (code, mask), instr_def in core.instructions.items():
		patch_model(expr_simplifier)
		logger.debug("simplifying expressions for instr %s", instr_def.name)
		instr_def.operation.generate(None)

		patch_model(function_throws)
		logger.debug("checking throws for instr %s", instr_def.name)
		throws = instr_def.operation.generate(None)
		instr_def.throws = throws

		patch_model(scalar_staticness)
		logger.debug("examining staticness for instr %s", instr_def.name)
		instr_def.operation.generate(None)