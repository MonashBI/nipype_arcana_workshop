# from banana.entrypoint import DeriveCmd

# input_str = ("data/ds000114 mri.T1wAnalysis my_banana_analysis brain_mask "
#              "--subject_ids 01 --visit_ids test --scratch work "
#              "--processor single").split()

# args = DeriveCmd.parser().parse_args(input_str)

# DeriveCmd.run(args)


from banana.requirement import fsl_req
from banana.file_format import nifti_gz_format
from banana.citation import fsl_cite
from nipype.interfaces import fsl
import nibabel as nb
import numpy as np
import matplotlib.pyplot as plt
from nipype.interfaces import fsl
from nipype.interfaces.utility import Merge
from arcana import (Analysis, AnalysisMetaClass, ParamSpec, InputFilesetSpec,
                    FilesetSpec, FieldSpec, Dataset, OutputFieldSpec,
                    OutputFilesetSpec)
from banana.file_format import text_format, nifti_gz_format
from banana.citation import fsl_cite
from banana.requirement import fsl_req
from example.interfaces import Grep, Awk, ConcatFloats, ExtractMetrics
from arcana import Dataset, FilesetFilter, AnalysisMetaClass, OutputFilesetSpec


class ToyAnalysis(Analysis, metaclass=AnalysisMetaClass):
    """
    A Toy Analysis class that extracts metrics from text files and produces
    summary statistics from them.
    """

    add_data_specs = [
        InputFilesetSpec('body_metrics', text_format,
                         desc=("Text file containing a range of basic body "
                               "metrics on separate lines")),
        FilesetSpec('selected_metric', text_format,
                    'extract_metrics_pipeline',
                    desc="The line containing the metric of interest"),
        OutputFieldSpec('average', float, 'statistics_pipeline',
                        frequency='per_dataset',
                        desc=("The average of the selected metric across all "
                              "subjects")),
        OutputFieldSpec('std_dev', float, 'statistics_pipeline',
                        frequency='per_dataset',
                        desc=("The std. dev. of the selected metric across "
                              "all subjects"))]

    add_param_specs = [
        ParamSpec('metric_of_interest', 'height',
                  "The metric of interest to extract from the files")]

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
                'in1': ('selected_metric', text_format)},
            joinsource=self.VISIT_ID,
            joinfield=['in1'])

        merge_subjects = pipeline.add(
            'merge_subjects',
            Merge(
                numinputs=1,
                ravel_inputs=True),
            inputs={
                'in1': (merge_visits, 'out')},
            joinsource=self.SUBJECT_ID,
            joinfield=['in1'])

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
            name_maps=name_maps,
            citations=[fsl_cite])

        pipeline.add(
            'bet',
            fsl.BET(
                mask=True),
            inputs={
                'in_file': ('magnitude', nifti_gz_format)},
            outputs={
                'brain': ('out_file', nifti_gz_format),
                'brain_mask': ('mask_file', nifti_gz_format)},
            requirements=[
                fsl_req.v('5.0.10')])

        return pipeline

    def smooth_mask_pipeline(self, **name_maps):

        pipeline = self.new_pipeline(
            'smooth_mask',
            desc="Smooths and masks a brain image",
            name_maps=name_maps,
            citations=[fsl_cite])

        # Smoothing process
        smooth = pipeline.add(
            'smooth',
            fsl.IsotropicSmooth(
                fwhm=self.parameter('smoothing_fwhm')),
            inputs={
                'in_file': ('magnitude', nifti_gz_format)},
            outputs={
                'smooth': ('out_file', nifti_gz_format)},
            requirements=[
                fsl_req.v('5.0.10')])

        pipeline.add(
            'mask',
            fsl.ApplyMask(),
            inputs={
                'in_file': (smooth, 'out_file'),
                'mask_file': ('brain_mask', nifti_gz_format)},
            outputs={
                'smooth_masked': ('out_file', nifti_gz_format)},
            requirements=[
                fsl_req.v('5.0.10')])

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
        data = self.data(spec_name, derive=True).item(
            subject_id=subject_id, visit_id=visit_id).get_array()

        # Cut in the middle of the brain
        cut = int(data.shape[-1] / 2) + 10

        # Plot the data
        plt.imshow(np.rot90(data[..., cut]), cmap="gray")
        plt.gca().set_axis_off()


if __name__ == '__main__':

    from arcana import FilesetFilter
    import subprocess as sp

    # analysis = BasicBrainAnalysis(
    #     'toms_analysis',
    #     dataset=Dataset('output/sample-datasets/depth1', depth=1),
    #     processor='work/sample-test',
    #     inputs=[
    #         FilesetFilter('magnitude', '.*T1w$', is_regex=True)],
    #     parameters={
    #         'smoothing_fwhm': 5.0})

    # analysis.plot_comparision()

    weight_analysis = ToyAnalysis(
        'weight_analysis',  # The name needs to be the same as the previous version
        dataset=Dataset('output/sample-datasets/toy-datasets', depth=2),
        # If you just provide a work dir then SingleProc is assumed
        processor='work/toy-analysis',
        inputs={'body_metrics': 'metrics'},
        parameters={'metric_of_interest': 'weight'})

    weight_analysis.processor.reprocess = True

    print(weight_analysis.data('std_dev', derive=True).value())



class MyExtendedBasicBrainAnalysis(BasicBrainAnalysis, metaclass=AnalysisMetaClass):

    add_data_specs = [
        OutputFilesetSpec('smooth', nifti_gz_format, 'smooth_mask_pipeline',
                          desc="Smoothed magnitude image in Mrtrix format"),
        OutputFilesetSpec('image_std', nifti_gz_format,
                          'image_std_pipeline',
                          desc="Standard deviation of the smoothed masked image")]

    def image_std_pipeline(self, **name_maps):

        pipeline = self.new_pipeline(
            'image_std_pipeline',
            desc="Calculates the standard deviation of the smooth masked image",
            name_maps=name_maps,
            citations=[fsl_cite])

        pipeline.add(
            'mask',
            fsl.ImageStats(
                op_string='-s'),
            inputs={
                'in_file': ('smooth_masked', nifti_gz_format)},
            outputs={
                'image_std': ('out_file', nifti_gz_format)},
            requirements=[
                fsl_req.v('5.0.10')])

        return pipeline


print(MyExtendedBasicBrainAnalysis.static_menu(full=True))


my_analysis = MyExtendedBasicBrainAnalysis(
    'my_extended_analysis',  # The name needs to be the same as the previous version
    dataset=Dataset('output/sample-datasets/depth1', depth=1),
    processor='work',
    inputs=[
        FilesetFilter('magnitude', '.*T1w$', is_regex=True)])

for std in my_analysis.data('image_std', derive=True):
    print('Subject/visit ({}/{}): {} '.format(std.subject_id, std.visit_id, std.value()))
