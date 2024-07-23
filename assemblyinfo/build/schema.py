import numpy as np

NCBI = "https://ftp.ncbi.nlm.nih.gov/genomes/all"

ASSEMBLY_BLACKLIST = [
    "T2T-CHM13v0.7",
    "NCBI33",
    "NCBI34",
    "MGSCv3",
    "canfam4",
    "Release_6_plus_MT",
]
REFSEQ_BLACKLIST = [
    "GCF_000001215.2",
    "GCF_000001215.2",
    "GCF_000002285.2",
    "GCF_000002315.2",
    "GCF_000002315.6",
    "GCF_000002035.3",
]

MAP_SPECIES_NAME = {
    "homo_sapiens": "human",
    "mus_musculus": "mouse",
    "canis_lupus_familiaris": "dog",
    "caenorhabditis_elegans": "celegans",
    "drosophila_melanogaster": "fruitfly",
    "danio_rerio": "zebrafish",
    "gallus_gallus": "chicken",
    "bos_taurus": "cow",
}

HUMAN_ASSEMBLY_MAP = {
    "GRCh37": "hg19",
    "GRCh38": "hg38",
    "T2T-CHM13": "hs1",
    "NCBI34": "hg16",
    "NCBI35": "hg17",
    "NCBI36": "hg18",
}
MOUSE_ASSEMBLY_MAP = {
    "GRCm38": "mm10",
    "GRCm39": "mm39",
    "MGSCv37": "mm9",
    "MGSCv36": "mm8",
    "MGSCv35": "mm7",
    "MGSCv34": "mm6",
}
DOG_ASSEMBLY_MAP = {
    "UU_Cfam_GSD_1.0": "canFam4",
    "CanFam2.0": "canFam2",
    "CanFam3.1": "canFam3",
    "Dog10K_Boxer_Tasha": "canFam6",
    "ROS_Cfam_1.0": "ROS_Cfam_1.0",
    "UMICH_Zoey_3.1": "canFam5",
}
CELEGANS_ASSEMBLY_MAP = {
    "WS144": np.NaN,
    "WBcel215": np.NaN,
    "WBcel235": "ce11",
    "WS190": "ce6",
    "WS195": np.NaN,
    "ASM2820141v1": np.NaN,
}
DROSOPHILA_ASSEMBLY_MAP = {
    "Release_5": "dm3",
    "Release_6": "dm6",
    "Release_6_plus_ISO1_MT": "dm6",
    "Release_6_plus_MT": "dm6",
}
DANIO_ASSEMBLY_MAP = {
    "Zv8": "danRer6",
    "Zv9": "danRer7",
    "GRCz10": "danRer10",
    "GRCz11": "danRer11",
    "Zv7": "danRer5",
    "ASM3317019v1": np.NaN,
    "ASM3317019v2": np.NaN,
}
CHICKEN_ASSEMBLY_MAP = {
    "bGalGal1.mat.broiler.GRCg7b": "galGal7",
    "Gallus_gallus-2.1": "galGal3",
    "Gallus_gallus-4.0": "galGal4",
    "Gallus_gallus-5.0": "galGal5",
    "GRCg6": np.NaN,
    "GRCg6a": "galGal6",
}
COW_ASSEMBLY_MAP = {
    "ARS-UCD1.1": np.NaN,
    "ARS-UCD1.2": "bosTau9",
    "ARS-UCD1.3": np.NaN,
    "ARS-UCD2.0": np.NaN,
}
ASSEMBLY_MAP = (
    HUMAN_ASSEMBLY_MAP
    | MOUSE_ASSEMBLY_MAP
    | DOG_ASSEMBLY_MAP
    | CELEGANS_ASSEMBLY_MAP
    | DROSOPHILA_ASSEMBLY_MAP
    | DANIO_ASSEMBLY_MAP
    | CHICKEN_ASSEMBLY_MAP
    | COW_ASSEMBLY_MAP
)
