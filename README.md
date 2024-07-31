# Assemblyinfo: Interact with assembly metadata in Python

![CI](https://github.com/open2c/assemblyinfo/actions/workflows/ci.yml/badge.svg)
[![Docs status](https://readthedocs.org/projects/genomeinfo/badge/)](https://genomeinfo.readthedocs.io/en/latest/)
[![Slack](https://img.shields.io/badge/chat-slack-%233F0F3F?logo=slack)](https://bit.ly/open2c-slack)

Assemblyinfo simplifies the management and analysis of genome assembly metadata in Python.

This package provides:

* Efficient tools for querying and manipulating assembly information datasets.
* Streamlined methods for importing, exporting, and converting between common chromosome formats.
* Utilities for retrieving assembly statistics across different versions or species.

Read the [documentation](https://genomeinfo.readthedocs.io/en/latest/) for more information.


## Installation

Bioframe is available on [PyPI](https://pypi.org/project/bioframe/):

```sh
pip install assemblyinfo
```

## Basic operations on chromosome data

Assemblyinfo offers a flexible and straigthforward interface to interact and perform basic queries.

```python
import assemblyinfo

db = assemblyinfo.connect()
hg38 = db.assembly_info("hg38", roles=["assembled"])
```

Easily allows getting chromosome sizes:

```python
hg38.chromsizes

> name
> chr1     248956422
> chr2     242193529
> ...
```

chromosome equivalences:

```python
hg38.chromeq

>      ncbi     genbank        refseq
> chr1     1  CM000663.2  NC_000001.11
> chr2     2  CM000664.2  NC_000002.12
> chr3     3  CM000665.2  NC_000003.12
> ...
```

or assembly metadata:

```python
hg38.metadata

> {'assembly_level': 'Chromosome',
 'assembly_type': 'haploid-with-alt-loci',
 'bioproject': 'PRJNA168',
 'submitter': 'Genome Reference Consortium',
 'synonyms': ['GRCh38', 'hg38'],
 'taxid': '9606',
 'species': 'homo_sapiens',
 'common_name': 'human',
 ... }
```

and more!

# Request an assembly

Feel free to open an issue and request a non-reference assembly! Current supported species are:

```plaintext
['caenorhabditis_elegans',
 'homo_sapiens',
 'mus_musculus',
 'drosophila_melanogaster',
 'danio_rerio',
 'bos_taurus',
 'gallus_gallus',
 'canis_lupus_familiaris']
```

You also can easily see which specific assemblies are supported by:

```python
db = assemblyinfo.connect()
db.available_assemblies()
```

## Citing

If you use ***assemblyinfo*** in your work, please refer to:

```bibtex
@software{assemblyinfo_2024,
  author       = {Open2C},
  title        = {assemblyinfo},
  year         = {2024},
  publisher    = {Github},
  version      = {v0.0.1},
  url          = {https://github.com/open2c/assemblyinfo}
}
```
