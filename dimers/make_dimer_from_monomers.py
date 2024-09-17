from ase import Atoms
from ase.io import read, write
from ase.build import add_adsorbate
import os

"""
This script generates all possible combinations of molecular complexes from 
monomers and atomic clusters, adjusting distances and orientations.
The script reads XYZ files from directories named:
  - 'molecules': containing ligand molecules
  - 'clusters': containing atomic clusters (e.g., dimers, trimers, tetramers)
Directories should be available at ../  in the same root directory.

For each pair of molecule and cluster, the script:
  1. Aligns the center of mass of each component.
  2. Rotates the cluster by a specified angle about a user-defined axis.
  3. Combines the molecule and cluster into a dimer at a specified distance.
  4. Saves the resulting dimer in an XYZ file with descriptive naming.
  

Code written by Piotr Zuchowski / improved for clarity by LLM (Claude)  
"""

def make_dimer_xyz(molecule_file, cluster_file, distance, angle, axis):
    """
    Combines a molecule and an atomic cluster into a dimer and saves the result as an XYZ file.

    Parameters:
        molecule_file (str): Filename of the molecule in 'molecules' directory.
        cluster_file (str): Filename of the atomic cluster in 'clusters' directory.
        distance (float): Distance between the centers of mass of the molecule and cluster.
        angle (float): Rotation angle (in degrees) to apply to the cluster.
        axis (list): Unit vector defining the axis of rotation.
    
    Returns:
        None
    """
    # Load molecule and cluster from files
    molecule = read(f'../molecules/{molecule_file}')
    cluster = read(f'../clusters/{cluster_file}')

    # Center both molecule and cluster
    molecule.translate(-molecule.get_center_of_mass())
    cluster.translate(-cluster.get_center_of_mass())

    # Apply rotation to the cluster
    cluster.rotate(axis, angle, rotate_cell=False)

    # Translate the cluster to the specified distance along the z-axis
    cluster.translate([0, 0, distance])

    # Combine molecule and cluster into a dimer
    dimer = molecule + cluster

    # Construct a descriptive filename and text comment
    base_name_a = os.path.splitext(molecule_file)[0]
    base_name_b = os.path.splitext(cluster_file)[0]
    output_filename = f'{base_name_a}_{base_name_b}_D{distance}_A{angle}.xyz'
    comment = f'{base_name_a} + {base_name_b}: Distance = {distance}, Angle = {angle}, Axis = {axis}'

    # Save the dimer as an XYZ file with the comment
    write(output_filename, dimer, comment=comment)
    print(f'Saved: {output_filename}')

# Directory paths
molecules_dir = "molecules"
clusters_dir = "clusters"

# Generate dimers for each combination of molecule and cluster files
for molecule_file in os.listdir(molecules_dir):
    if molecule_file.endswith(".xyz"):
        for cluster_file in os.listdir(clusters_dir):
            if cluster_file.endswith(".xyz"):
                # Create dimers at different orientations
                make_dimer_xyz(molecule_file, cluster_file, distance=4.0, angle=0.0, axis=[1, 0, 0])
                make_dimer_xyz(molecule_file, cluster_file, distance=4.0, angle=90.0, axis=[0, 0, 1])

