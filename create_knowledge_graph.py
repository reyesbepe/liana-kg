import biocypher
from adapters.uniprot_liana import (
    Uniprot,
    UniprotNodeType,
    UniprotNodeField,
)

# Instantiate the BioCypher driver
# You can use `config/biocypher_config.yaml` to configure the driver or supply
# settings via parameters below
driver = biocypher.Driver(
    user_schema_config_path="config/biocypher_config.yaml",
    skip_bad_relationships=True,  # Neo4j admin import option
    skip_duplicate_nodes=True,  # Neo4j admin import option
)

# Take a look at the ontology structure of the KG according to the schema
driver.show_ontology_structure()

# Choose node types to include in the knowledge graph.
# These are defined in the adapter (`adapter.py`).
uniprot_node_types = [
    UniprotNodeType.PROTEIN,
    UniprotNodeType.GENE,
    UniprotNodeType.ORGANISM,
    UniprotNodeType.CELLULAR_COMPARTMENT,
]

uniprot_node_fields = [
    UniprotNodeField.PROTEIN_SECONDARY_IDS,
    UniprotNodeField.PROTEIN_LENGTH,
    UniprotNodeField.PROTEIN_MASS,
    UniprotNodeField.PROTEIN_ORGANISM,
    UniprotNodeField.PROTEIN_ORGANISM_ID,
    UniprotNodeField.PROTEIN_NAMES,
    UniprotNodeField.PROTEIN_PROTEOME,
    UniprotNodeField.PROTEIN_EC,
    UniprotNodeField.PROTEIN_GENE_NAMES,
    UniprotNodeField.PROTEIN_ENSEMBL_TRANSCRIPT_IDS,
    UniprotNodeField.PROTEIN_ENSEMBL_GENE_IDS,
    UniprotNodeField.PROTEIN_ENTREZ_GENE_IDS,
    UniprotNodeField.PROTEIN_VIRUS_HOSTS,
    UniprotNodeField.PROTEIN_KEGG_IDS,
    UniprotNodeField.PROTEIN_SUBCELLULAR_LOCATION
]

# Create a protein adapter instance
uniprot_adapter = Uniprot(
        organism="9606",
        node_types=uniprot_node_types,
        node_fields=uniprot_node_fields,
        test_mode=True,
        ligand_file="data/ligands_curated.csv",
        receptor_file="data/receptors_curated.csv",
    )

uniprot_adapter.download_uniprot_data(cache = True)

# Create a knowledge graph from the adapter
driver.write_nodes(uniprot_adapter.get_nodes())
driver.write_edges(uniprot_adapter.get_edges())

# Write admin import statement
driver.write_import_call()

# Check output
driver.log_duplicates()
driver.log_missing_bl_types()
