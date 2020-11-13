# Repository to explain headless automatic plotting with igv

This tool can be used to script the taking of screenshots with IGV.

It can be used either locally on your PC (as a background task, without sacrificing your monitor), or
even in completely headless environments such as compute clusters (for example, if your desktop isn't allowed
direct access to secured data).
It achieves this by using the "[X virtual frame buffer](https://www.x.org/releases/X11R7.7/doc/man/man1/Xvfb.1.xhtml)", `Xvfb`

In case you do not have a local IGV/Xvfb installation on the relevant machines, we also provide
an [IGV_xfvb](https://hub.docker.com/repository/docker/stephanholgerdrukewitz/igvplots) Docker/Singularity image
for easy containerisation.

## Requirements

For Singularity
* working singularity installation
* python3
* .igv folder in the home directory of the current user

or on your local computer
* full igv installation
* `xvfb-run` installed and in `$PATH`
* python3


## Docker & Singularity

The image [IGV_xfvb Image](https://hub.docker.com/repository/docker/stephanholgerdrukewitz/igvplots) can be pulled
and formated to singularity format using:

```sh
singularity pull docker://stephanholgerdrukewitz/igvplots:latest
```


## How it works

* Main entry point is the `plotRegions.py` script
* `plotRegions` processes a `vars.tsv` 'todo list'.
  * The actual work is done inside `PlotVarSingularity()` or `PlotVarIGVlocal()` funtions from the igvXfvb.py script
  * both functions need an ID, chro, start, end, mapping, key
* The `vars.tsv` file `chro`, `start`, `end`, `mapping`, are informations about the alignment file and the position of interest
  * `ID` and `key` are only uysed in the naming of the output, could be removed in future
* both `plotVar`-functions write a 'plot.bat' file which is later read in by igvXfvb
* plots are saved in a directory with the name `Snaphots` in your current working directory
* every variant provided to PlotVarSingularity or PlotVarIGVlocal is plotted 3 times --> 30nt to both sides, 75nt to both sides, 150nt to both sides
* PlotVarSingularity or PlotVarIGVlocal  both call igv headless using :
```sh
xvfb-run --auto-servernum --server-num=1 java -Xmx8000m jar /opt/conda/bin/igv.jar -b plot.bat
```
  * /opt/conda/bin/igv.jar is the location of the igv.jar file in the docker image, might differ depending on your installation


### Example generated `plot.bat`

This is an example `plot.bat`, created from the first line of the provided in vars.tsv.  
See also the pseudocode in `plotRegions.py`, which reads out `vars.tsv` and calls `PlotVarSingularity` or `PlotVarIGVlocal`

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


# Author
Stephan drukewitz
--> stephan.drukewitz@nct-dresden.de
--> stephan.drukewitz@uniklinikum-dresden.de
