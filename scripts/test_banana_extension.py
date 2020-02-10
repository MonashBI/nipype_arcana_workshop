from nipype import config
import os.path as op
from traits.trait_base import Undefined
from nilearn import plotting, image
config.enable_debug_mode()  # This is necessary due to a bug in one of the interfaces
import nipype
import matplotlib.pyplot as plt
from nipype.interfaces import fsl
from arcana import (
    Analysis, AnalysisMetaClass, ParamSpec, SwitchSpec, Dataset, FilesetFilter,
    SingleProc)
from arcana import OutputFilesetSpec
from banana.file_format import nifti_gz_format
from example.analysis import BasicBrainAnalysis  # qa pylint: disable=unrecognised-import



class MyExtendedBasicBrainAnalysis(BasicBrainAnalysis, metaclass=AnalysisMetaClass):
    
    add_param_specs = [
        BasicBrainAnalysis.param_spec('smoothing_fwhm').with_new_default(2.0)
    ]
    
    add_data_specs = [
        OutputFilesetSpec('skull_mask', nifti_gz_format,
                          'brain_extraction_pipeline',
                          desc="Skull mask extracted from magnitude image"),
    ]
    
    def brain_extraction_pipeline(self, **name_maps):
        pipeline = super().brain_extraction_pipeline(**name_maps)

        bet = pipeline.node('bet')

        # Set the input of the BET node so that it outputs a Skull mask
        bet.inputs.surfaces = True

        pipeline.connect_output(
            'skull_mask', bet, 'skull_mask_file', nifti_gz_format)

        return pipeline

    def smooth_mask_pipeline(self, **name_maps):
        pipeline = super().smooth_mask_pipeline(**name_maps)

        smooth = pipeline.node('smooth')

        # Set the input of the BET node so that it outputs a Skull mask
        smooth.inputs.fwhm = Undefined
        smooth.inputs.sigma = 2.0

        return pipeline

    def plot_slices(self, spec_name, title, subject_id='sub1', visit_id='VISIT'):
        plotting.plot_anat(
            image.load_img(self.data(spec_name).item(
                subject_id=subject_id, visit_id=visit_id).path),
            title=title, display_mode='z', dim=-1,
            cut_coords=[-20, -10, 0, 10, 20, 30])
    

def create_analysis():
    my_analysis = MyExtendedBasicBrainAnalysis(
        'my_extended_analysis',  # The name needs to be the same as the previous version
        dataset=Dataset('output/sample-datasets/depth1', depth=1),
        processor=SingleProc('work', reprocess=True),
        inputs=[
            FilesetFilter('magnitude', '.*T1w$', is_regex=True)])
    return my_analysis


analysis = create_analysis()
analysis.derive('smooth_masked')
analysis.plot_slices('smooth_masked', 'Skull Mask')
plt.show()