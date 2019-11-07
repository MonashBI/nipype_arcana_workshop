import os
import os.path as op
from nipype.interfaces.base import (
    TraitedSpec, traits, File, isdefined,
    CommandLineInputSpec, CommandLine, BaseInterface,
    InputMultiPath)


class GrepInputSpec(CommandLineInputSpec):
    match_str = traits.Str(argstr='-e %s', position=0,
                           desc="The string to search for")
    in_file = File(argstr='%s', position=1,
                   desc="The file to search")
    out_file = File(genfile=True, argstr='> %s', position=2,
                    desc=("The file to contain the search results"))


class GrepOutputSpec(TraitedSpec):
    out_file = File(exists=True, desc="The search results")


class Grep(CommandLine):
    """
    Wraps the common Unix utility 'grep' used for searching through plain
    text files
    """

    _cmd = 'grep'
    input_spec = GrepInputSpec
    output_spec = GrepOutputSpec

    def _list_outputs(self):
        outputs = self._outputs().get()
        outputs['out_file'] = self._gen_filename('out_file')
        return outputs

    def _gen_filename(self, name):
        if name == 'out_file':
            if isdefined(self.inputs.out_file):
                fname = self.inputs.out_file
            else:
                fname = op.join(os.getcwd(), 'search_results.txt')
        else:
            assert False
        return fname


class AwkInputSpec(CommandLineInputSpec):
    format_str = traits.Str(argstr="'%s'", position=0,
                            desc="The string to search for")
    in_file = File(argstr='%s', position=1,
                   desc="The file to parse")
    out_file = File(genfile=True, argstr='> %s', position=2,
                    desc=("The file to contain the parsed results"))


class AwkOutputSpec(TraitedSpec):
    out_file = File(exists=True, desc="The parsed results")


class Awk(CommandLine):
    """
    Wraps the common Unix utility 'awk' for text processing
    """

    _cmd = 'awk'
    input_spec = AwkInputSpec
    output_spec = AwkOutputSpec

    def _list_outputs(self):
        outputs = self._outputs().get()
        outputs['out_file'] = self._gen_filename('out_file')
        return outputs

    def _gen_filename(self, name):
        if name == 'out_file':
            if isdefined(self.inputs.out_file):
                fname = self.inputs.out_file
            else:
                fname = os.path.join(os.getcwd(), 'awk_results.txt')
        else:
            assert False
        return fname


class ConcatFloatsInputSpec(TraitedSpec):
    in_files = InputMultiPath(desc='file name')


class ConcatFloatsOutputSpec(TraitedSpec):
    out_list = traits.List(traits.Float, desc='input floats')


class ConcatFloats(BaseInterface):
    """Joins values from a list of files into a single list"""

    input_spec = ConcatFloatsInputSpec
    output_spec = ConcatFloatsOutputSpec

    def _list_outputs(self):
        out_list = []
        for path in self.inputs.in_files:
            with open(path) as f:
                val = float(f.read())
                out_list.append(val)
        outputs = self._outputs().get()
        outputs['out_list'] = out_list
        return outputs

    def _run_interface(self, runtime):
        # Do nothing
        return runtime


class ExtractMetricsInputSpec(TraitedSpec):
    in_list = traits.List(traits.Float, desc='input floats')


class ExtractMetricsOutputSpec(TraitedSpec):
    std = traits.Float(desc="The standard deviation")
    avg = traits.Float(desc="The average")


class ExtractMetrics(BaseInterface):
    """Joins values from a list of files into a single list"""

    input_spec = ExtractMetricsInputSpec
    output_spec = ExtractMetricsOutputSpec

    def _list_outputs(self):
        values = self.inputs.in_list
        outputs = self._outputs().get()
        outputs['std'] = numpy.std(values)
        outputs['avg'] = numpy.average(values)
        return outputs

    def _run_interface(self, runtime):
        # Do nothing
        return runtime
