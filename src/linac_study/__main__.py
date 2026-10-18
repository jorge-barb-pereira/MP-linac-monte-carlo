"""Run source characterization and archived mesh analysis without MCNP."""
import argparse
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from .mesh import read_mesh
from .source import bin_probabilities


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mesh', type=Path, default=Path('data/historical/meshtas'))
    parser.add_argument('--output', type=Path, default=Path('output'))
    args = parser.parse_args()
    args.output.mkdir(parents=True,exist_ok=True)
    histories, meshes = read_mesh(args.mesh.read_text(encoding='utf-8'))
    energy_edges=np.linspace(0,12,35)
    radius_edges=np.linspace(0,1,35)
    fig, axes=plt.subplots(1,2,figsize=(10,4),layout='constrained')
    for ax, edges, mu, gamma, xlabel in [(axes[0],energy_edges,6,.6,'Electron energy (MeV)'),
                                          (axes[1],radius_edges,0,.1,'Radius (cm)')]:
        probabilities=bin_probabilities(edges,mu,gamma)
        ax.stairs(probabilities/np.diff(edges),edges,fill=True,alpha=.65)
        ax.set(xlabel=xlabel,ylabel='Probability density',title='Normalized finite-interval Cauchy')
    fig.savefig(args.output/'source-distributions.png',dpi=160)
    plt.close(fig)
    fig,axes=plt.subplots(2,len(meshes),figsize=(13,7),squeeze=False,layout='constrained')
    summary=[]
    for col,mesh in enumerate(meshes):
        positive=mesh.values>0
        reliable=positive & (mesh.relative_errors<.1)
        summary.append(dict(tally=mesh.number,shape=list(mesh.values.shape),z_cm=mesh.z_edges.tolist(),
                            nonzero_bins=int(positive.sum()),total_bins=int(positive.size),
                            nonzero_bins_relative_error_below_0_1=int(reliable.sum()),
                            median_relative_error_nonzero=float(np.median(mesh.relative_errors[positive])) if positive.any() else None))
        for row,data,title in [(0,mesh.values,'Photon fluence'),(1,np.ma.masked_where(~positive,mesh.relative_errors),'Relative error (nonzero bins)')]:
            ax=axes[row,col]
            ax.set_facecolor('#dddddd')
            im=ax.pcolormesh(mesh.x_edges,mesh.y_edges,data,shading='flat')
            ax.set(xlabel='x (cm)',ylabel='y (cm)',title=f'Tally {mesh.number}: {title}',aspect='equal')
            fig.colorbar(im,ax=ax,label='cm⁻² / source electron' if row==0 else 'Relative standard error')
    fig.suptitle(f'Historical MCNP6 mesh: {histories:,} electron histories; not clinical validation')
    fig.savefig(args.output/'historical-fluence.png',dpi=160)
    plt.close(fig)
    result=dict(histories=histories,requested_histories=1000000000,
                interpretation='Descriptive postprocessing; relative error alone does not establish convergence or accuracy.',meshes=summary)
    (args.output/'summary.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
