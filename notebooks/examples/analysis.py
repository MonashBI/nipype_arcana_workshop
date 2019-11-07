
from nipype.interfaces import fsl
from nipype.interfaces.utility import Merge
from arcana import (Study, StudyMetaClass, ParamSpec, InputFilesetSpec,
                    FilesetSpec, FieldSpec)
from arcana.data.file_format import text_format, FileFormat
from .interfaces import Grep, Awk, ConcatFloats, ExtractMetrics


class ExampleStudy(Study, metaclass=StudyMetaClass):

    add_data_specs = [
        InputFilesetSpec('body_metrics', text_format),
        FilesetSpec('selected_metric', text_format,
                    'extract_metrics_pipeline'),
        FieldSpec('average', float, 'statistics_pipeline',
                  frequency='per_study'),
        FieldSpec('std_dev', float, 'statistics_pipeline',
                  frequency='per_study')]

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



nifti_gz_format = FileFormat(name='nifti_gz', extension='.nii.gz',
                             resource_names={'xnat': ['NiFTI_GZ',
                                                      'NIFTI_GZ']})


class SkullStripSmoothMaskAnalysis(Study):

    add_data_specs = [
        InputFilesetSpec('magnitude', nifti_gz_format),
        FilesetSpec('brain', nifti_gz_format, 'brain_extraction_pipeline'),
        FilesetSpec('smooth_masked', nifti_gz_format, 'smooth_mask_pipeline')]

    add_param_specs = [
        ParamSpec('fwhm', 4.0)]

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
                'brain': ('out_file', nifti_gz_format)})

        return pipeline
    
    def 
        # Skullstrip process
        skullstrip = fsl.BET(
            in_file="data/ds000114/sub-01/ses-test/anat/sub-01_ses-test_T1w.nii.gz",
            out_file="output/sub-01_T1w_brain.nii.gz",
            mask=True)
        skullstrip.run()

# Smoothing process
smooth = fsl.IsotropicSmooth(
    in_file="data/ds000114/sub-01/ses-test/anat/sub-01_ses-test_T1w.nii.gz",
    out_file="output/sub-01_T1w_smooth.nii.gz",
    fwhm=4)
smooth.run()

# Masking process
mask = fsl.ApplyMask(
    in_file="output/sub-01_T1w_smooth.nii.gz",
    out_file="output/sub-01_T1w_smooth_mask.nii.gz",
    mask_file="output/sub-01_T1w_brain_mask.nii.gz")
mask.run()

f = plt.figure(figsize=(12, 4))
for i, img in enumerate(["T1w", "T1w_smooth",
                         "T1w_brain_mask", "T1w_smooth_mask"]):
    f.add_subplot(1, 4, i + 1)
    if i == 0:
        plot_slice(
            "data/ds000114/sub-01/ses-test/anat/sub-01_ses-test_%s.nii.gz" % img)
    else:
        plot_slice("output/sub-01_%s.nii.gz" % img)
    plt.title(img)
