# Mixed-Use Skies: Dynamic Risk Cells and Performance-Contracted Integration of Spacecraft into Global Air Traffic

Reproducible scripts and assets to generate the four figures used in the paper:

`closure_example.png` — static closure polygon + (optional) reroutes overlay  
`blockdiag.png` — system block diagram  
`reliability_plot.png` — calibration (reliability) diagram with ECE  
`containment_demo.png` — inward offset + simplification containment demo

The repository also includes the LaTeX source (`main.tex`) and a Makefile for one-command builds.

---

## Contents

drc_figs/
blockdiag/
blockdiag.dot
make_blockdiag.py
closure_example/
hazard.csv # YOUR official polygon (lon,lat,order)
tracks_example.geojson # optional (demo)
make_closure_example.py
containment_demo/
make_containment_demo.py
reliability_plot/
make_preds.py # makes a synthetic preds.csv (optional)
make_reliability_plot.py
preds.csv # YOUR held-out predictions (y_true,y_prob)
Makefile
requirements.txt
environment.yml
main.tex
new-aiaa.cls, new-aiaa.bst
LICENSE
CITATION.cff

---

## Quick start

### Prerequisites

- Python 3.10+ (tested on 3.13)  
- [Graphviz](https://graphviz.org/download/) binary (`dot`) for the block diagram  
  - macOS: `brew install graphviz`  
  - Ubuntu/Debian: `sudo apt-get install graphviz`
- (Optional) `cartopy` will download Natural Earth coastline/land data at first run

### Setup

```bash
cd drc_figs
python3 -m venv .venv
source .venv/bin/activate  
pip install -r requirements.txt
```

### Build everything

```bash
cd drc_figs
make all

# or individually:
make closure
make blockdiag
make reliability
make containment
```

The outputs land in their respective subfolders (and copies at repo root if you want).

---

## Data & reproducibility

Archive/DOI: A versioned snapshot of this repo (code, figure scripts, configs, and example bundles) is archived at: DOI: 10.5281/zenodo.16881670.

GitHub mirror: https://github.com/mathewlewallen/Mixed-Use_Skies (tag v1.0.0 or commit a6d8b60).

---

## Troubleshooting

ModuleNotFoundError: geopandas: Geopandas is optional and only needed if you load GeoJSON tracks with attribute ops. The map script works without it. If you want it: pip install geopandas (may require geos, proj on Linux).

dot: command not found: Install Graphviz (see Prerequisites).

cartopy downloads Natural Earth layers on first run; if behind a proxy, set HTTP_PROXY/HTTPS_PROXY.

---

## Citation

If you use this software or reproduce the figures, please cite:

@software{Lewallen_DRC_2025,
  author  = {Mathew J. Lewallen},
  title   = {Mixed-Use Skies: Dynamic Risk Cells and Performance-Contracted Integration of Spacecraft into Global Air Traffic},
  year    = {2025},
  url     = {https://github.com/mathewlewallen/Mixed-Use_Skies},
  version = {v1.0.0},
  doi     = {10.5281/zenodo.16881670}
}

A CITATION.cff is included so GitHub can generate the correct citation.

---

## License

Code in this repository is licensed under the Apache License 2.0 (see LICENSE).

Example maps may render U.S. Government data (NOTAM/LNM/Federal Register) and Natural Earth basemaps — both are public domain.

If you overlay OpenSky Network ADS-B data, follow OpenSky’s license/attribution (ODbL) for the data you fetch. The provided tracks_example.geojson is illustrative only.