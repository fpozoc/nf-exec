#!/bin/bash
nextflow \
	run nf-core/sarek -r 2.7.1 \
	-params-file "params.json" \
	-work-dir "work" \
	-profile "docker"
