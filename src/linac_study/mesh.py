"""Strict reader for the archived MCNP6 OUT=IJ single-plane photon meshes.

Other output layouts, multiple energy groups and multiple planes are rejected.
Arrays have shape (y, x). Relative errors are supplied by MCNP, not re-estimated.
"""
from dataclasses import dataclass
import re
import numpy as np


@dataclass(frozen=True)
class Mesh:
    number: int
    x_edges: np.ndarray
    y_edges: np.ndarray
    z_edges: np.ndarray
    values: np.ndarray
    relative_errors: np.ndarray


def read_mesh(text):
    match = re.search(r"Number of histories used for normalizing tallies\s*=\s*([0-9.Ee+\-]+)", text)
    if not match:
        raise ValueError("Missing history count")
    histories = float(match[1])
    if not np.isfinite(histories) or histories <= 0 or not histories.is_integer():
        raise ValueError("Invalid history count")
    meshes = []
    chunks = re.split(r"Mesh Tally Number\s+(\d+)", text)
    for pos in range(1, len(chunks), 2):
        number, chunk = int(chunks[pos]), chunks[pos+1]
        if 'photon   mesh tally.' not in chunk:
            raise ValueError("Only photon meshes supported")
        axes = []
        for axis in 'XYZ':
            found = re.search(axis+r" direction:\s*([^\n]+)", chunk)
            if not found:
                raise ValueError("Missing axis boundaries")
            edges = np.array([float(v) for v in found[1].split()])
            if len(edges)<2 or not np.all(np.isfinite(edges)) or np.any(np.diff(edges)<=0):
                raise ValueError("Invalid axis boundaries")
            axes.append(edges)
        x, y, z = axes
        if len(z)!=2 or chunk.count('Energy Bin:')!=1 or chunk.count('Z bin:')!=1:
            raise ValueError("Only one energy group and one z plane supported")
        arrays = []
        for label in ['Tally Results:  X (across) by Y (down)', 'Relative Errors']:
            if chunk.count(label)!=1:
                raise ValueError("Missing or repeated matrix label")
            lines = chunk.split(label, 1)[1].strip().splitlines()
            expected_x = (x[:-1]+x[1:])/2
            header = np.array([float(v) for v in lines[0].split()])
            if header.shape != expected_x.shape or not np.allclose(header, expected_x, atol=0.0051, rtol=0):
                raise ValueError("Matrix x coordinates disagree with boundaries")
            rows = [[float(v) for v in line.split()] for line in lines[1:len(y)]]
            matrix = np.array(rows)
            if matrix.shape != (len(y)-1, len(x)) or not np.all(np.isfinite(matrix)):
                raise ValueError("Invalid or truncated matrix")
            if not np.allclose(matrix[:,0], (y[:-1]+y[1:])/2, atol=0.0051, rtol=0):
                raise ValueError("Matrix y coordinates disagree with boundaries")
            arrays.append(matrix[:,1:])
        values, errors = arrays
        if np.any(values<0) or np.any(errors<0) or np.any(errors>1):
            raise ValueError("Invalid tally values or relative errors")
        meshes.append(Mesh(number,x,y,z,values,errors))
    if not meshes or len({m.number for m in meshes})!=len(meshes):
        raise ValueError("Missing or duplicate mesh tallies")
    return int(histories), meshes
