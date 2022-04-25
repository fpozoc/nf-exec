# Install exact conda dependencies
conda-install:
	conda env create -f environment.yml
	echo "!!!RUN RIGHT NOW:\nconda activate nf-exec"

# Downloading GATK GRCh38 reference
download-gatk-grch37:
	aws s3 --no-sign-request --region eu-west-1 sync s3://ngi-igenomes/igenomes/Homo_sapiens/GATK/GRCh38/ data/references/Homo_sapiens/GATK/GRCh38/

# Downloading GATK GRCh37 reference
download-gatk-grch37:
	aws s3 --no-sign-request --region eu-west-1 sync s3://ngi-igenomes/igenomes/Homo_sapiens/GATK/GRCh38/ data/references/Homo_sapiens/GATK/GRCh38/

# Downloading NCBI GRCh38 reference
download-ncbi-grch38:
	aws s3 --no-sign-request --region eu-west-1 sync s3://ngi-igenomes/igenomes/Homo_sapiens/NCBI/GRCh38/Annotation/Genes/ ./references/Homo_sapiens/NCBI/GRCh38/Annotation/Genes/ --exclude "*" --include "genes.gtf"
	aws s3 --no-sign-request --region eu-west-1 sync s3://ngi-igenomes/igenomes/Homo_sapiens/NCBI/GRCh38/Annotation/Genes/ ./references/Homo_sapiens/NCBI/GRCh38/Annotation/Genes/ --exclude "*" --include "genes.bed"
	aws s3 --no-sign-request --region eu-west-1 sync s3://ngi-igenomes/igenomes/Homo_sapiens/NCBI/GRCh38/Sequence/WholeGenomeFasta/ ./references/Homo_sapiens/NCBI/GRCh38/Sequence/WholeGenomeFasta/
	aws s3 --no-sign-request --region eu-west-1 sync s3://ngi-igenomes/igenomes/Homo_sapiens/NCBI/GRCh38/Sequence/STARIndex/ ./references/Homo_sapiens/NCBI/GRCh38/Sequence/STARIndex/