from rdkit import Chem
from rdkit.Chem import AllChem

import numpy as np
import h5py

# Input and output files
SDF_FILE = "10mols.sdf"

OUTPUT_FILE = "fingerprints.h5"

# Fingerprint settings
FP_SIZE = 1024

RADIUS = 2

# Load molecules from SDF
supplier = Chem.SDMolSupplier(SDF_FILE)

molecules = [
    mol for mol in supplier
    if mol is not None
]

print(f"Loaded {len(molecules)} molecules")

# Lists for storage
fingerprints = []

counts = []

smiles_list = []

ids = []

# Generate fingerprints
for i, mol in enumerate(molecules):

    # Morgan fingerprint
    fp = AllChem.GetMorganFingerprintAsBitVect(
        mol,
        RADIUS,
        nBits=FP_SIZE
    )

    # Convert bit vector to numpy array
    bitstring = fp.ToBitString()

    arr = np.array(
        list(map(int, bitstring)),
        dtype=np.uint8
    )

    fingerprints.append(arr)

    counts.append(arr.sum())

    smiles_list.append(
        Chem.MolToSmiles(mol)
    )

    ids.append(f"MOL_{i+1}")

# Convert lists to numpy arrays
fingerprints = np.array(
    fingerprints,
    dtype=np.uint8
)

counts = np.array(
    counts,
    dtype=np.int32
)

ids = np.array(ids)

smiles_arr = np.array(
    smiles_list,
    dtype="S"
)

# Save database
with h5py.File(OUTPUT_FILE, "w") as hf:

    hf.create_dataset(
        "fingerprints",
        data=fingerprints,
        compression="gzip"
    )

    hf.create_dataset(
        "counts",
        data=counts
    )

    hf.create_dataset(
        "ids",
        data=ids.astype("S")
    )

    hf.create_dataset(
        "smiles",
        data=smiles_arr
    )

    # Metadata
    hf.attrs["fp_size"] = FP_SIZE

    hf.attrs["radius"] = RADIUS

print(f"\nDatabase saved to '{OUTPUT_FILE}'")

print(f"Shape: {fingerprints.shape}")