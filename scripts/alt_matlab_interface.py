import re  # Regular-expressions module
import os.path as op
from nipype.interfaces.base import (CommandLine, traits, TraitedSpec,
                                    BaseInterface, BaseInterfaceInputSpec,
                                    File)
from nipype.interfaces.matlab import MatlabCommand, MatlabInputSpec


class AltBrainVolumeMATLABInputSpec(MatlabInputSpec):
    in_file = File(exists=True, mandatory=True)


class AltBrainVolumeMATLABOutputSpec(TraitedSpec):
    volume = traits.Int(desc='brain volume')
    raw_output = traits.Str()


class AltBrainVolumeMATLAB(MatlabCommand):
    input_spec = AltBrainVolumeMATLABInputSpec
    output_spec = AltBrainVolumeMATLABOutputSpec

    def _generate_script(self):
        """This is where you implement your script"""
        return """
            data = niftiread('{in_file}');
            total = sum(data(:) > 0)
        """.format(in_file=self.inputs.in_file)

    def run(self, *args, **kwargs):
        # Inject our script into the Matlab input interface
        self.inputs.script = self._generate_script()
        return super().run(*args, **kwargs)

    def _run_interface(self, runtime):
        runtime = super()._run_interface(runtime)
        # Save the stdout output to use in _list_outputs
        self._raw_output = runtime.stdout

        return runtime

    def _list_outputs(self):
        # Get outputs dictionary
        outputs = self._outputs().get()
        # Save the raw output to the outputs dictionary
        outputs['raw_output'] = self._raw_output
        # Use a regular expression to extract out the volume from the matlab
        # output
        match = re.search(r'total =\s+([0-9]+)', self._raw_output)
        if match:
            outputs['volume'] = int(match.group(1))
        else:
            raise Exception(("Did not find match for 'total =\\s+([0-9]+)' in "
                             "raw output:\n\n{}").format(self._raw_output))

        return outputs


matlab = AltBrainVolumeMATLAB(in_file=op.abspath(
    'notebooks/data/ds000114/sub-01/ses-test/anat/sub-01_ses-test_T1w.nii.gz'))
result = matlab.run()
print(result.outputs)
