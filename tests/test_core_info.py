from assemblyinfo.interface import AssemblyInfo


def test_method_attachment():
    db = AssemblyInfo.connect()
    assert hasattr(db, "info"), "Method info is not attached"


def test_method_execution():
    genome_info = AssemblyInfo.connect()

    genome_info.info()


def test_get_species_info():
    genome_info = AssemblyInfo.connect()

    assert hasattr(
        genome_info, "get_species_info"
    ), "Method get_species_info is not attached"

    rs = genome_info.get_species_info("homo_sapiens")

    assert rs is not None, "The result is None"


def test_get_assembly_metadata_ncbi():
    genome_info = AssemblyInfo.connect()

    assert hasattr(
        genome_info, "get_assembly_metadata"
    ), "Method get_assembly_metadata is not attached"

    rs = genome_info.get_assembly_metadata("GRCh38")

    assert rs is not None, "The result is None"


def test_get_assembly_metadata_ucsc():
    genome_info = AssemblyInfo.connect()

    rs = genome_info.get_assembly_metadata("hg38")

    assert rs is not None, "The result is None"
    assert len(rs) > 0, "The result if empty"


def test_get_assembly_metadata_t2t():
    genome_info = AssemblyInfo.connect()

    rs = genome_info.get_assembly_metadata("T2T-CHM13")

    assert rs is not None, "The result is None"
    assert len(rs) > 0, "The result if empty"


def test_available_assemblies():
    genome_info = AssemblyInfo.connect()

    rs = genome_info.available_assemblies()

    assert rs is not None, "The result is None"
    assert len(rs) > 0, "The result is empty"


def test_get_organism_info():
    genome_info = AssemblyInfo.connect()

    rs = genome_info.get_organism_info("human")

    assert rs is not None, "The result is None"
    assert len(rs) > 0, "The result is empty"


def test_available_patches():
    genome_info = AssemblyInfo.connect()

    rs = genome_info.available_patches()

    assert rs is not None, "The result is None"
    assert len(rs) > 0, "The result is empty"


def test_available_accessions():
    genome_info = AssemblyInfo.connect()

    rs = genome_info.available_accessions("GRCh38")

    assert rs is not None, "The result is None"
    assert len(rs) > 0, "The result is empty"

    rs = genome_info.available_accessions("hg38")

    assert rs is not None, "The result is None"
    assert len(rs) > 0, "The result is empty"
