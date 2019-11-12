#!/usr/bin/env bash

for sub in '01' '02' '03'; do
    for vis in 'test' 'retest'; do
        for f in $(find data/ds000114/sub-$sub/ses-$vis -name '*.nii.gz'); do
            scan=$(basename $f)
            scan=${scan#sub-${sub}_ses-${vis}_}
            xnat-put -s xnat.monash.edu -c MISC0002_sub${sub}_$vis ${scan%%.nii.gz} $f 
        done
    done
done
