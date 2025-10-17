# tama
Transcriptome Annotation by Modular Algorithms

This software was designed for processing Iso-Seq data and other long read transcriptome data. 

See wiki for manual:
https://github.com/GenomeRIK/tama/wiki

If you have any questions on how to run TAMA please post them in the Github issues for this repo and I will respond as soon as possible. It is also worth checking the closed issues to see if your question has already been answered. 

In case I am not responsive on the issues page you can email me directly at (sometimes I don't get the notifications): 
GenomeRIK at gmail dot com

To cite TAMA please use our paper in BMC Genomics:
https://bmcgenomics.biomedcentral.com/articles/10.1186/s12864-020-07123-7

版本与修复记录（Python2→Python3，本地 1.0.4）:

- 软件版本：将 TAMA Collapse 的 `tc_version` 更新为 `1.0.4`（见 `tama_collapse.py` L26-27），用于标识本地兼容修复。

- 已完成的 Python3 兼容修复项：
  - `pyflow/gs-tama-1.0.4/tama_collapse.py`：加固版本导入（`__version__` 导入回退）；使用 `from io import StringIO`；正则 `\d` → `r'\d'`。
  - `pyflow/gs-tama-1.0.4/tama_merge.py`：加固版本导入（`__version__` 导入回退）；使用 `from io import StringIO`。
  - `pyflow/gs-tama-1.0.4/tama_go/call_variants/tama_variant_caller.py`：正则 `\d` → `r'\d'`。
 - `pyflow/gs-tama-1.0.4/tmp.py`：加固版本导入（`__version__` 导入回退）；正则 `\d` → `r'\d'`。

- Python3 排序修复：
  - 修复 `dict_keys` 在 Python3 下无 `sort()` 方法的问题。
  - 替换模式：
    - 旧：`start_gene_list = start_gene_dict.keys(); start_gene_list.sort()`
    - 新：`start_gene_list = sorted(start_gene_dict.keys())`
  - 在 `tama_collapse.py` 的合并起始位点汇总处，修复为：`all_start_list = sorted(all_start_gene_dict.keys())`，并统一使用 `all_start_list` 进行遍历，避免变量不一致导致的异常。

- 正则修复说明：避免 "SyntaxWarning: invalid escape sequence '\d'"，确保正则表达式按数字匹配而非字符 `d`。

- 全目录 Python3 统一替换：已将所有 Python 文件中的 `xrange(` 统一替换为 `range(`，并将 `from StringIO import StringIO` 替换为 `from io import StringIO`，与上述正则修复一并完成。

- 版本导入回退说明：为避免直接运行脚本时出现 `ModuleNotFoundError: No module named '__init__'`，在相关脚本中增加了 `__version__` 的回退逻辑：优先从同目录 `__init__.py` 解析版本；若不可用，则使用默认版本 `1.0.4`。

示例用法（Python3 环境）：

- 直接调用 Collapse：
  - `python3 pyflow/gs-tama-1.0.4/tama_collapse.py -s input.sorted.sam -f genome.fa -p output_prefix -x capped -e common_ends -a 10 -m 10 -z 10`
  - 读取 BAM：`python3 pyflow/gs-tama-1.0.4/tama_collapse.py -s input.bam -f genome.fa[.gz] -p output_prefix -b BAM`

- 直接调用 Merge：
  - `python3 pyflow/gs-tama-1.0.4/tama_merge.py -f filelist.tsv -p output_prefix -e common_ends -a 10 -m 10 -z 10`

- 通过封装主流程（推荐）：
  - `python3 pyflow/gs_tama.py collapse --bam input.bam --fasta genome.fa --outdir outdir --prefix output_prefix --args "-x capped -e common_ends"`
  - `python3 pyflow/gs_tama.py merge --filelist filelist.tsv --prefix output_prefix --order common_ends`
  - 指定 samtools 路径：`python3 pyflow/gs_tama.py collapse --bam input.bam --fasta genome.fa[.gz] --outdir outdir --prefix output_prefix --args "-b BAM" --samtools-bin "~/miniconda3/envs/pacbio_iso_seq/bin/samtools"`

注意事项：
- BAM 读取与 samtools：脚本优先使用 `samtools view`；若系统未安装或命令失败，封装会自动回退到 `pysam.view('-h', bam, catch_stdout=True)`，并在 Python3 下对字节流进行安全解码，避免 `TypeError: a bytes-like object is required, not 'str'`。
- 指定 samtools 路径（封装）：`gs_tama.py collapse` 支持 `--samtools-bin`；批处理脚本 `run_gs_tama.sh` 支持 `SAMTOOLS_BIN` 环境变量统一注入。封装会将该路径所在目录优先加入 `PATH`，确保内部调用使用指定版本。