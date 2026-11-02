from flask import Flask, request, jsonify
from Bio.PDB import PDBParser
import urllib.request, os

app = Flask(__name__)
parser = PDBParser(QUIET=True)

@app.route("/analyze")
def analyze():
    pdb_id = request.args.get("pdb_id", "1CRN")
    path = f"/tmp/{pdb_id}.pdb"
    urllib.request.urlretrieve(f"https://files.rcsb.org/download/{pdb_id}.pdb", path)
    structure = parser.get_structure(pdb_id, path)
    chains = list(structure.get_chains())
    atoms = list(structure.get_atoms())
    residues = list(structure.get_residues())
    return jsonify({
        "pdb_id": pdb_id,
        "chains": len(chains),
        "residues": len(residues),
        "atoms": len(atoms),
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
