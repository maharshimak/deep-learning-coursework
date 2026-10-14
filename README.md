# Deep learning coursework

Code-only educational notebook demonstrating a two-layer NumPy sigmoid network, binary cross-entropy, manual backpropagation, logistic regression comparison and Matplotlib/Plotly visualizations. This is coursework, not a trained model or production classifier. The original main.py is only a greeting placeholder.

The user confirmed source ownership/upload rights. Lecture prose, all 18 original markdown cells, notebook outputs/metadata, the original classification dataset, environments and historical results are excluded. No exclusive authorship claim is made for educational patterns; source rights remain reserved without inventing a license.

## Setup

Use a separate Python environment (Python3.10+). Review requirements.txt before choosing to install scientific/notebook dependencies. Dependency resolution and installation were not performed during preparation; no reproducible lock is claimed. Original uv.lock covered only Plotly and was excluded because it does not describe the actual scientific imports.

Generate clearly synthetic input first:

```powershell
python generate_synthetic_data.py --output data/synthetic_classification.csv --rows 128
```

The generator uses a local seeded standard-library RNG, refuses existing files, and permits at most1000rows. The schema is x1,x2,x3,y with binary labels. These generated values do not reproduce the withheld original dataset or any historical accuracy.

Review neural_network_basics.ipynb before execution. Its first code cell refuses by default; deliberately change ALLOW_COURSE_EXECUTION only after review. Training calls are bounded to100epochs instead of the original2000; no training was run during preparation. Loss/accuracy plots are training-set descriptions, not held-out performance. The teaching architecture has no separate output bias and is intentionally limited.

## Verification

`python -B -m unittest discover -s tests -v` runs four standard-library tests: source/metadata structure, default refusal, a reviewed isolated sigmoid function with scalar mock NumPy, and synthetic generator determinism/overwrite protection. It does not import scientific dependencies, execute the notebook, train a network or render plots. Full numerical gradient/integration validation remains unrun.
