import sys

#
# This script comverts nanopore fastq to fasta
#

print("opening fastq")
fastq_file = sys.argv[1]
fastq_file_contents = open(fastq_file).read().rstrip("\n").split("\n")

outfile_name = sys.argv[2]
outfile = open(outfile_name, "w")

# test_files/test.fastq
count_lines = 0

for line in fastq_file_contents:

    count_lines += 1

    # grab fasta header
    if line.startswith("@") and count_lines == 1:
        fasta_header = ">" + line[1:]

    elif count_lines == 2:
        fasta_seq = line

    if count_lines == 4:
        count_lines = 0

        outfile.write(fasta_header)
        outfile.write("\n")
        outfile.write(fasta_seq)
        outfile.write("\n")

        fasta_header = "na"
        fasta_seq = "na"
