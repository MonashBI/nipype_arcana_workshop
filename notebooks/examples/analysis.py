
from nipype.interfaces.utility import Merge
from arcana import (Study, StudyMetaClass, ParamSpec, InputFilesetSpec,
                    FilesetSpec, FieldSpec)
from arcana.data.file_format import text_format
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
