from glob import glob
import pandas as pd
import subprocess


#definition to run igv using a bat file
#defintion needs:
# the ID of the patient --> only for naming the output
# chromosome
# start position
# end position
# location of the bam file
# key string of chro pos alt and ref --> only for naming output

def WritePlotBat(ID, chro, start, end, mapping, key):
    mappingName=mapping.split('/')[-1].split('.')[0]
    with open('plot.bat','w')as s:
        s.write('new\n')
        s.write('maxPanelHeight 5000\n')
        s.write('genome hg19\n')
        s.write('snapshotDirectory Snapshots\n')
        s.write('load {}\n'.format(mapping))
        s.write('group strand\n')
        s.write('goto chr{}:{}-{}\n'.format(chro,str(int(start)-30),str(int(end)+30)))
        s.write('sort base\n')
        s.write('collapse\n')
        s.write('snapshot {}_{}_{}_out_pad30_collapse.png\n'.format(ID,key,mappingName))
        s.write('expand\n')
        s.write('snapshot {}_{}_{}_out_pad30_expand.png\n'.format(ID,key,mappingName))

        s.write('goto chr{}:{}-{}\n'.format(chro,str(int(start)-75),str(int(end)+75)))
        s.write('sort base\n')
        s.write('collapse\n')
        s.write('snapshot {}_{}_{}_out_pad75_collapse.png\n'.format(ID,key,mappingName))
        s.write('expand\n')
        s.write('snapshot {}_{}_{}_out_pad75_expand.png\n'.format(ID,key,mappingName))

        s.write('goto chr{}:{}-{}\n'.format(chro,str(int(start)-150),str(int(end)+150)))
        s.write('sort base\n')
        s.write('collapse\n')
        s.write('snapshot {}_{}_{}_out_pad150_collapse.png\n'.format(ID,key,mappingName))
        s.write('expand\n')
        s.write('snapshot {}_{}_{}_out_pad150_expand.png\n'.format(ID,key,mappingName))
        s.write('exit')


def PlotVarSingularity(ID, chro, start, end, mapping, key):
    WritePlotBat(ID, chro, start, end, mapping, key)

    subprocess.call(['singularity', 'run', '-B',
                    '/icgc/dkfzlsdf/project/hipo/hipo_021:/icgc/dkfzlsdf/project/hipo/hipo_021','igvplots_latest.sif',
                    'xvfb-run', '--auto-servernum', '--server-num=1', 'java',
                    '-Xmx8000m', '-jar',
                    '/opt/conda/bin/igv.jar', '-b' ,'plot.bat'])



IGV_jar='path/to/.jar' ##need to provide path to igv.ja file on your system, is needed for the subprocess call

def PlotVarIGVlocal(ID, chro, start, end, mapping, key):
    WritePlotBat(ID, chro, start, end, mapping, key)

    subprocess.call(['xvfb-run', '--auto-servernum', '--server-num=1', 'java',
                    '-Xmx8000m', '-jar',
                    IGV_jar, '-b' ,'plot.bat'])
