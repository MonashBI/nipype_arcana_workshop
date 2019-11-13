from banana.entrypoint import DeriveCmd

input_str = ("data/ds000114 mri.T1wAnalysis my_banana_analysis brain_mask "
             "--subject_ids 01 --visit_ids test --scratch work "
             "--processor single").split()

args = DeriveCmd.parser().parse_args(input_str)

DeriveCmd.run(args)
