
import nibabel as nb
import numpy as np
import matplotlib.pyplot as plt
from nipype.interfaces import fsl
from nipype.interfaces.utility import Merge
from arcana import (Analysis, AnalysisMetaClass, ParamSpec, InputFilesetSpec,
                    FilesetSpec, FieldSpec, Dataset, OutputFieldSpec,
                    OutputFilesetSpec)
from banana.file_format import text_format, nifti_gz_format
from example.interfaces import Grep, Awk, ConcatFloats, ExtractMetrics


class ExampleAnalysis(Analysis, metaclass=AnalysisMetaClass):

    add_data_specs = [
        InputFilesetSpec('body_metrics', text_format),
        FilesetSpec('selected_metric', text_format,
                    'extract_metrics_pipeline'),
        FieldSpec('average', float, 'statistics_pipeline',
                  frequency='per_dataset'),
        FieldSpec('std_dev', float, 'statistics_pipeline',
                  frequency='per_dataset')]

    add_param_specs = [
        ParamSpec('metric_of_interest', 'height')]

    def extract_metrics_pipeline(self, **name_maps):
        pipeline = self.new_pipeline(
            name='extract_metrics',
            name_maps=name_maps,
            desc="Extract metrics from file")

        grep = pipeline.add(
            'grep',
            Grep(
                match_str=self.parameter('metric_of_interest')),
            inputs={
                'in_file': ('body_metrics', text_format)})

        pipeline.add(
            'awk',
            Awk(
                format_str='{print $2}'),
            inputs={
                'in_file': (grep, 'out_file')},
            outputs={
                'selected_metric': ('out_file', text_format)})

        return pipeline

    def statistics_pipeline(self, **name_maps):
        pipeline = self.new_pipeline(
            name='statistics',
            name_maps=name_maps,
            desc="Calculate statistics")

        merge_visits = pipeline.add(
            'merge_visits',
            Merge(
                numinputs=1),
            inputs={
                'in1': ('selected_metric', text_format)})

        merge_subjects = pipeline.add(
            'merge_subjects',
            Merge(
                numinputs=1,
                ravel_inputs=True),
            inputs={
                'in1': (merge_visits, 'out')})

        concat = pipeline.add(
            'concat',
            ConcatFloats(),
            inputs={
                'in_files': (merge_subjects, 'out')})

        pipeline.add(
            'extract_metrics',
            ExtractMetrics(),
            inputs={
                'in_list': (concat, 'out_list')},
            outputs={
                'average': ('avg', float),
                'std_dev': ('std', float)})

        return pipeline


class BasicBrainAnalysis(Analysis, metaclass=AnalysisMetaClass):
    """
    A baisc analysis class that demonstrates how Analysis classes work.
    """

    add_data_specs = [
        InputFilesetSpec('magnitude', nifti_gz_format,
                         desc="A magnitude image (e.g. T1w, T2w, etc..)"),
        OutputFilesetSpec('brain', nifti_gz_format,
                          'brain_extraction_pipeline',
                          desc="Skull-stripped magnitude image"),
        FilesetSpec('brain_mask', nifti_gz_format,
                    'brain_extraction_pipeline',
                    desc="Brain mask used for skull-stripping"),
        OutputFilesetSpec('smooth', nifti_gz_format, 'smooth_mask_pipeline',
                          desc="Smoothed magnitude image"),
        OutputFilesetSpec('smooth_masked', nifti_gz_format,
                          'smooth_mask_pipeline',
                          desc="Smoothed and masked magnitude image")]

    add_param_specs = [
        ParamSpec('smoothing_fwhm', 4.0,
                  desc=("The full-width-half-maxium radius of the smoothing "
                        "kernel"))]

    def brain_extraction_pipeline(self, **name_maps):

        pipeline = self.new_pipeline(
            'brain_extraction',
            desc="Extracts brain from full-head image",
            name_maps=name_maps)

        pipeline.add(
            'bet',
            fsl.BET(
                mask=True),
            inputs={
                'in_file': ('magnitude', nifti_gz_format)},
            outputs={
                'brain': ('out_file', nifti_gz_format),
                'brain_mask': ('mask_file', nifti_gz_format)})

        return pipeline

    def smooth_mask_pipeline(self, **name_maps):

        pipeline = self.new_pipeline(
            'smooth_mask',
            desc="Smooths and masks a brain image",
            name_maps=name_maps)

        # Smoothing process
        smooth = pipeline.add(
            'smooth',
            fsl.IsotropicSmooth(
                fwhm=self.parameter('smoothing_fwhm')),
            inputs={
                'in_file': ('magnitude', nifti_gz_format)},
            outputs={
                'smooth': ('out_file', nifti_gz_format)})

        pipeline.add(
            'mask',
            fsl.ApplyMask(),
            inputs={
                'in_file': (smooth, 'out_file'),
                'mask_file': ('brain_mask', nifti_gz_format)},
            outputs={
                'smooth_masked': ('out_file', nifti_gz_format)})

        return pipeline

    def plot_comparision(self, figsize=(12, 4)):

        for subj_i in self.subject_ids:
            for visit_i in self.visit_ids:
                f = plt.figure(figsize=figsize)
                f.suptitle('Subject "{}" - Visit "{}"'.format(subj_i, visit_i))
                for i, spec_name in enumerate(['magnitude', 'smooth',
                                               'brain_mask', 'smooth_masked']):
                    f.add_subplot(1, 4, i + 1)
                    self._plot_slice(spec_name, subj_i, visit_i)
                    plt.title(spec_name)
        plt.show()

    def _plot_slice(self, spec_name, subject_id=None, visit_id=None):
        # Load the image
        data = self.derive(spec_name).item(subject_id=subject_id,
                                           visit_id=visit_id).get_array()

        # Cut in the middle of the brain
        cut = int(data.shape[-1] / 2) + 10

        # Plot the data
        plt.imshow(np.rot90(data[..., cut]), cmap="gray")
        plt.gca().set_axis_off()


if __name__ == '__main__':

    from arcana import LocalFileSystemRepo, SingleProc
    import subprocess as sp

# sp.check_call(
#     'mkdir -p output/basic_brain/sub-01/ses-test;'
#     'ln -s $(pwd)/data/ds000114/sub-01/ses-test/anat/sub-01_ses-test_T1w.nii.gz '
#     'output/basic_brain/sub-01/ses-test/', shell=True)

    analysis = BasicBrainAnalysis(
        'test',
        dataset=Dataset('output/basic_brain'),
        processor=SingleProc('output/work-dir'),
        inputs={
            'magnitude': 'sub-01_ses-test_T1w'})

    analysis.plot_comparision()
