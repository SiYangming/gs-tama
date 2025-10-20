import argparse
import sys

# This script uses the TAMA read levels support file for sampling curves

ap = argparse.ArgumentParser(
    description=("This script uses the TAMA read support levels file "
                 "to create a saturation curve"))

ap.add_argument("-r", type=str, nargs=1, help="Read support file")

ap.add_argument("-b", type=str, nargs=1, help="Read bin size")

ap.add_argument("-o", type=str, nargs=1, help="Output file name")

opts = ap.parse_args()

# check for missing args
missing_arg_flag = 0

if not opts.r:
    print("Read support file missing")
    missing_arg_flag = 1

if not opts.b:
    print("Read bin size missing")
    missing_arg_flag = 1

if not opts.o:
    print("Output file name missing")
    missing_arg_flag = 1

if missing_arg_flag == 1:
    print("Please try again with complete arguments")

report_file = opts.r[0]

read_bin = int(opts.b[0])

outfile_name = opts.o[0]

print("opening report file")

report_file_contents = open(report_file).read().rstrip("\n").split("\n")
# continue here! 2019/06/22

outfile = open(outfile_name, "w")

read_gene_dict = {}
# read_gene_dict[read_id] = gene_id

all_gene_dict = {}
# all_gene_dict[gene_id] = 1

for line in report_file_contents:

    # test_files/Read_support_file.txt

    if line.startswith("gene_id"):
        continue

    line_split = line.split("\t")

    merge_gene_id = line_split[0]
    num_reads = line_split[2]
    support_line = line_split[5]

    support_list = support_line.split(";")

    if merge_gene_id not in all_gene_dict:
        all_gene_dict[merge_gene_id] = 1

    for source_line in support_list:
        source_split = source_line.split(":")

        source_name = source_split[0]

        source_split.pop(0)

        read_line = ":".join(source_split)

        read_list = read_line.split(",")

        for read_id in read_list:

            if read_id not in read_gene_dict:
                read_gene_dict[read_id] = merge_gene_id
            elif merge_gene_id != read_gene_dict[read_id]:
                print("Error with read support multiple genes!")
                print(read_id + "\t" + read_gene_dict[read_id] + "\t" +
                      merge_gene_id)
                sys.exit()

all_read_list = list(read_gene_dict.keys())

read_count = 0
gene_count = 0

check_gene_dict = {}  # check_gene_dict[gene_id] = 1

outline = "read_count" + "\t" + "gene_count"

outfile.write(outline)
outfile.write("\n")

for read_id in all_read_list:
    read_count += 1

    if read_count % read_bin == 0:
        outline = "\t".join([str(read_count), str(gene_count)])

        outfile.write(outline)
        outfile.write("\n")

    this_gene_id = read_gene_dict[read_id]

    if this_gene_id not in check_gene_dict:
        gene_count += 1
        check_gene_dict[this_gene_id] = 1
