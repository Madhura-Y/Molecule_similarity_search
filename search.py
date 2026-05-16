from rdkit import Chem
from rdkit.Chem import AllChem

import numpy as np
import h5py

# Database file
DB_FILE = "fingerprints.h5"

# Load database
with h5py.File(DB_FILE, "r") as hf:

    X = hf["fingerprints"][:]

    counts = hf["counts"][:]

    ids = hf["ids"][:].astype(str)

    smiles = [
        s.decode()
        for s in hf["smiles"][:]
    ]

    fp_size = int(
        hf.attrs.get(
            "fp_size",
            X.shape[1]
        )
    )

    radius = int(
        hf.attrs.get(
            "radius",
            2
        )
    )
print(f"Loaded {len(X)} molecules")

# Convert for fast computation
X = X.astype(np.float32)

counts = counts.astype(np.float32)

# Search function
def search(query_smiles, top_n=10):

    # Convert query SMILES to molecule
    mol = Chem.MolFromSmiles(query_smiles)

    if mol is None:
        raise ValueError("Invalid SMILES!")

    # Generate query fingerprint
    query_fp = AllChem.GetMorganFingerprintAsBitVect(
        mol,
        radius,
        nBits=fp_size
    )

    # Convert to numpy array
    q = np.array(
        list(map(int, query_fp.ToBitString())),
        dtype=np.float32
    )

    # Tanimoto similarity
    a = q.sum()

    b = counts

    c = X @ q

    tanimoto = c / (a + b - c)

    # Sort results
    order = np.argsort(
        tanimoto
    )[::-1][:top_n]

    results = []

    for i in order:

        results.append({

            "id": ids[i],

            "similarity": float(
                tanimoto[i]
            ),

            "smiles": smiles[i]
        })

    return results


# Terminal testing
if __name__ == "__main__":

    query = input("Enter SMILES: ")

    results = search(query)

    print("\nTop Matches:\n")

    for rank, item in enumerate(results, start=1):

        print(
            f"Rank {rank} | "
            f"ID: {item['id']} | "
            f"Similarity: {item['similarity']:.4f} | "
            f"SMILES: {item['smiles']}"
        )