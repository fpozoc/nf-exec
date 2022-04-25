# nf-exec

# Table of contents
- [nf-exec](#nf-exec)
- [Table of contents](#table-of-contents)
- [Introduction](#introduction)
- [Installation](#installation)
  - [Conda](#conda)
  - [Docker](#docker)
- [Pipelines](#pipelines)
  - [Running Sarek (nf-core)](#running-sarek-nf-core)
    - [Reference genomes](#reference-genomes)
    - [Usage](#usage)
    - [Sample directory structure:](#sample-directory-structure)
  - [Running a different pipeline (from nf-core)](#running-a-different-pipeline-from-nf-core)
- [Directory structure](#directory-structure)
- [Author information and license](#author-information-and-license)

# Introduction
Tools to reproduce the steps to run nf-core pipelines for bioinformatics analysis within Linux environments.

# Installation

## Conda
Run the silent installation of [Miniconda](https://docs.conda.io/en/latest/miniconda.html)/[Anaconda](https://anaconda.org/) in case you don't have this software in your environment.

```sh
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh -b -p $HOME/miniconda3
```

## Docker
Run the installation of [Docker](https://docs.docker.com/engine/install/ubuntu/) in case you don't have this software in your environment.

```sh
 sudo apt-get update

 sudo apt-get install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io

sudo docker run hello-world
```

# Pipelines

## Running Sarek (nf-core)
[Sarek](https://nf-co.re/sarek) is a workflow designed to detect variants on whole genome or targeted sequencing data. Initially designed for Human, and Mouse, it can work on any species with a reference genome. 

### Reference genomes

Creating the data structure:
```sh
mkdir -p data/reference data/out data/samples
```

Downloading commonly used bioinformatics reference genomes. In this case, GATK files for GRCh38 and GRCh37:

```sh
make gatk-grch38
make gatk-grch37
```

### Usage
1. Modify <my_sample_id> and <data_dir> by the actual variables and setting environment variables:
```sh
$SAMPLE_ID=<my_sample_id>
$DATA_DIR=<data_dir>

$REFERENCE_DIR=$DATA_DIR/reference
$SAMPLE_DIR=$DATA_DIR/out/$SAMPLE_ID
$WORK_DIR=$DATA_DIR/out/$SAMPLE_ID/work
$RESULTS_DIR=$DATA_DIR/out/$SAMPLE_ID/results
```

2. Creating the directory structure with symbolic links (check this guide [here](https://www.digitalocean.com/community/tutorials/workflow-symbolic-links) in case you don't know how to deal with symbolic links):
```sh
mkdir -p $SAMPLE_ID # creating the new directory for the new upcoming sample

ln -s $SAMPLE_DIR"/"$SAMPLE_ID_1".fastq.gz" $SAMPLE_ID"/samples/sample1_1.fastq.gz" # sample1_1.fastq.gz
ln -s $SAMPLE_DIR"/"$SAMPLE_ID"_2.fastq.gz" $SAMPLE_ID"/samples/sample1_2.fastq.gz" # sample1_2.fastq.gz
ln -s $REFERENCE_DIR $SAMPLE_ID/reference # genome reference directory
ln -s $WORK_DIR $SAMPLE_ID/work # work directory
ln -s $RESULTS_DIR $SAMPLE_ID/results # results directory
```

3. Run the pipeline:
```sh
bash run.sh
```

The run.sh script is a bash script that runs the pipeline and has the following content:
```
#!/bin/bash
nextflow \
	run nf-core/sarek -r 2.7.1 \
	-params-file "params.json" \
	-work-dir "work" \
	-profile "docker"
```

### Sample directory structure:
```sh
$ nf-exec/sample_template/: tree -L 3
.
├── params.json # parameters for the pipeline
├── references -> data/references # reference genome directory
├── resources.json # resources for the pipeline (Slurm)
├── results -> data/out/SAMPLE_ID/results # results directory
├── run.sh # script to run the pipeline
├── run.slurm # script to run the pipeline (Slurm)
├── samples # directory with the fastq.gz files
│   ├── sample1.fastq.gz -> data/samples/SAMPLE_ID_1.fastq.gz # 5'->3' paired-end reads
│   └──sample2.fastq.gz -> data/samples/SAMPLE_ID_2.fastq.gz # 3'->5' paired-end reads
├── samples.tsv # table with the metadata for the fastq.gz files
└── work -> data/out/SAMPLE_ID/work # work directory

1 directory, 10 files
```

## Running a different pipeline (from nf-core)

If you want to perform a different analysis, below is an example of how to run a RNA-seq pipeline:

1. Downloading genome references. In this case, NCBI Reference Genome for GRCh38:
```sh
make download-ncbi-grch38
```
2. Reproduce the same 2 and 3 steps as before changing the ids for control and case.
3. Create a new `samples.csv` instead of the original one.

```
$SAMPLE_ID=<my_sample_id>
mkdir -p $SAMPLE_ID # creating the new directory for the new upcoming sample
touch $SAMPLE_ID/samples.csv
```

4. Edit this `samples.csv` file following this [reference](https://nf-co.re/rnaseq/usage#full-samplesheet):
```
sample,fastq_1,fastq_2,strandedness
CONTROL,samples/<SAMPLE_ID_control>_1.fastq.gz,samples/<SAMPLE_ID_control>_1.fastq.gz,reverse
TREATMENT,samples/<SAMPLE_ID_treatment>_1.fastq.gz,samples/<SAMPLE_ID_treatment>_1.fastq.gz,reverse
```

1. Modify the `<SAMPLE_ID>/run.sh` file to run the RNA-seq pipeline:
```sh
#!/bin/bash
nextflow \
	run nf-core/rnaseq -r 3.6 \
	-params-file "params.json" \
	-work-dir "work" \
	-profile "docker"
```

# Directory structure
```sh
$ nf-exec/: tree -L 3
.
├── data # data directory to store all the input and output files
    .
    ├── out # output directory to store all the output files (results and work)
    ├── references # directory to store the reference genomes
    └── samples # directory to store the samples raw data 
├── environment.yml # environment variables for reproducing the pipeline within a conda environment
├── LICENSE # license file
├── Makefile # makefile to facilite the pipeline management
├── README.md # readme file
├── sample_template # sample template directory
└── scripts # scripts directory
    .
    └── utils.py # utility functions written in Python to post-process the output files

3 directories, 4 files
```

# Author information and license

Fernando Pozo ([@fpozoca](https://twitter.com/fpozoca) – fpozoc@gmx.com)

Distributed under the GNU General Public License. See ``LICENSE`` for more information.