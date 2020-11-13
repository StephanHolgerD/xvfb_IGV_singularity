from glob import glob
import pandas as pd
import subprocess

IGV_jar='path/to/.jar' ##need to provide path to igv.ja file on your system, is needed for the subprocess call
snapshot_dir='Snapshots'

#definition to run igv using a bat file
#defintion needs:
# the ID of the patient --> only for naming the output
# chromosome
# start position
# end position
# location of the bam file
# key string of chro pos alt and ref --> only for naming output



# plot.bat template fragment to load a file
bat_template_header = """\
new
maxPanelHeight 5000
genome hg19
snapshotDirectory {snap_dir}
load {filename}
group strand
"""

# plot.bat template fragment to take a pair of {collapsed,expanded} snapshots, with a given padding.
bat_template_padded_snapshot = """\
goto chr{chro}:{padded_start}-{padded_end}
sort base
collapse
snapshot {ID}_{key}_{mappingName}_out_pad{pad}_collapse.png
expand
snapshot {ID}_{key}_{mappingName}_out_pad{pad}_expand.png
"""

def WritePlotBat(ID, chro, start, end, mapping, key):
    mappingName=mapping.split('/')[-1].split('.')[0]
    with open('plot.bat','w') as s:
        s.write(bat_template_header.format(
           filename=mapping,
           snap_dir=snapshot_dir
        ))

        for pad in (30, 75, 150):
            s.write(bat_template_padded_snapshot.format(
                chro=chro,
                pad=pad,
                padded_start=int(start)-pad,
                padded_end=int(end)+pad,
                ID=ID,
                key=key,
                mappingName=mappingName
            ))

        s.write('exit\n')


def PlotVarSingularity(ID, chro, start, end, mapping, key):
    WritePlotBat(ID, chro, start, end, mapping, key)

    subprocess.call(['singularity', 'run', '-B',
                    '/icgc/dkfzlsdf/project/hipo/hipo_021:/icgc/dkfzlsdf/project/hipo/hipo_021','igvplots_latest.sif',
                    'xvfb-run', '--auto-servernum', '--server-num=1', 'java',
                    '-Xmx8000m', '-jar',
                    '/opt/conda/bin/igv.jar', '-b' ,'plot.bat'])


def PlotVarIGVlocal(ID, chro, start, end, mapping, key):
    WritePlotBat(ID, chro, start, end, mapping, key)

    subprocess.call(['xvfb-run', '--auto-servernum', '--server-num=1', 'java',
                    '-Xmx8000m', '-jar',
                    IGV_jar, '-b' ,'plot.bat'])
