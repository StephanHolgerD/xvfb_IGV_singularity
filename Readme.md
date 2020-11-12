# repository to explain headless automatic plotting with igv


## requirements

* working singularity installation
* python3
* .igv folder in the home directory of the current user

or

* full igv installation
* xfvb-run installation
* python3


## Docker & Singularity
[IGV_xfvb Image](https://hub.docker.com/repository/docker/stephanholgerdrukewitz/igvplots)

Image can be pulled and formated to singularity format using:

```
singularity pull docker://stephanholgerdrukewitz/igvplots:latest
```


### How it works

*call PlotVarSingularity or PlotVarIGVlocal funtion from the igvXfvb.py script
*both functions need an ID, chro, start, end, mapping, key
* chro, start, end, mapping, are informations about the alignment file and the position of interest
* ID and key are only uysed in the naming of the output, could be removed in future
* both functions write a 'plot.bat' file which is later read in by igvXfvb
* plot.bat based on the first line of data provided in vars.tsv, pseudocode in ploRegions.py to read out vars.tsv and call PlotVarSingularity or PlotVarIGVlocal
```
new
maxPanelHeight 5000
genome hg19
snapshotDirectory Snapshots
load /mnt/pat2.bam
group strand
goto chr2:41196281-41196341
sort base
collapse
snapshot Patient2_pat2_brcaBlaBlub_pat2_out_pad30_collapse.png
expand
snapshot Patient2_pat2_brcaBlaBlub_pat2_out_pad30_expand.png
goto chr2:41196236-41196386
sort base
collapse
snapshot Patient2_pat2_brcaBlaBlub_pat2_out_pad75_collapse.png
expand
snapshot Patient2_pat2_brcaBlaBlub_pat2_out_pad75_expand.png
goto chr2:41196161-41196461
sort base
collapse
snapshot Patient2_pat2_brcaBlaBlub_pat2_out_pad150_collapse.png
expand
snapshot Patient2_pat2_brcaBlaBlub_pat2_out_pad150_expand.png
exit
```

* PlotVarSingularity or PlotVarIGVlocal  both call igv headless using :

```
xvfb-run --auto-servernum --server-num=1 java -Xmx8000m jar /opt/conda/bin/igv.jar -b plot.bat

```
* /opt/conda/bin/igv.jar is the location of the igv.ja file in the docker iamge, night differ depnding on yout installation

* plots are saved in a directory with the name 'Snaphots' in yoyr current working directory
* every variant provided to PlotVarSingularity or PlotVarIGVlocal is plotted 3 times --> 30nt to both sides, 75nt to both sides, 150nt to both sides


# Author
Stephan drukewitz
--> stephan.drukewitz@nct-dresden.de
--> stephan.drukewitz@uniklinikum-dresden.de
