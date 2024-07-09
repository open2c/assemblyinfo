from genomeinfo.interface import GenomeInfo


def test_method_attachment():
    db = GenomeInfo.connect()
    assert hasattr(db, "info"), "Method info is not attached"


def test_method_execution():
    genome_info = GenomeInfo.connect()

    try:
        genome_info.info()
    except Exception as e:
        AssertionError(f"Method execution failed: {e!s}")


def test_get_species_info():
    genome_info = GenomeInfo.connect()

    assert hasattr(
        genome_info, "get_species_info"
    ), "Method get_species_info is not attached"

    try:
        genome_info.get_species_info("homo_sapiens")
    except Exception as e:
        AssertionError(f"Method execution failed: {e!s}")


def test_get_assembly_metadata_ncbi():
    genome_info = GenomeInfo.connect()

    assert hasattr(
        genome_info, "get_assembly_metadata"
    ), "Method get_assembly_metadata is not attached"

    try:
        genome_info.get_assembly_metadata("GRCh38")
    except Exception as e:
        AssertionError(f"Method execution failed: {e!s}")


def test_get_assembly_metadata_ucsc():
    genome_info = GenomeInfo.connect()

    try:
        rs = genome_info.get_assembly_metadata("hg38")
    except Exception as e:
        AssertionError(f"Method execution failed: {e!s}")


    assert rs is not None, "The result is None"
    assert len(rs) > 0, "The result if empty"


def test_get_assembly_metadata_t2t():
    genome_info = GenomeInfo.connect()

    try:
        rs = genome_info.get_assembly_metadata("T2T-CHM13")
    except Exception as e:
        AssertionError(f"Method execution failed: {e!s}")

    assert rs is not None, "The result is None"
    assert len(rs) > 0, "The result if empty"


def test_available_assemblies():
    genome_info = GenomeInfo.connect()

    try:
        rs = genome_info.available_assemblies()
    except Exception as e:
        AssertionError(f"Method execution failed: {e!s}")

    assert rs is not None, "The result is None"
    assert len(rs) > 0, "The result is empty"


def test_get_organism_info():
    genome_info = GenomeInfo.connect()

    try:
        rs = genome_info.get_organism_info("human")
    except Exception as e:
        AssertionError(f"Method execution failed: {e!s}")

    assert rs is not None, "The result is None"
    assert len(rs) > 0, "The result is empty"


def test_available_patches():
    genome_info = GenomeInfo.connect()

    try:
        rs = genome_info.available_patches()
    except Exception as e:
        AssertionError(f"Method execution failed: {e!s}")

    assert rs is not None, "The result is None"
    assert len(rs) > 0, "The result is empty"


def test_available_accessions():
    genome_info = GenomeInfo.connect()

    try:
        rs = genome_info.available_accessions("GRCh38")
    except Exception as e:
        AssertionError(f"Method execution failed: {e!s}")

    assert rs is not None, "The result is None"
    assert len(rs) > 0, "The result is empty"

    try:
        rs = genome_info.available_accessions("hg38")
    except Exception as e:
        AssertionError(f"Method execution failed: {e!s}")

    assert rs is not None, "The result is None"
    assert len(rs) > 0, "The result is empty"
