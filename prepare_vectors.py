from sentence_transformers import SentenceTransformer
import torch
import numpy as np
import json
import pandas as pd
from tqdm.notebook import tqdm

if torch.backends.mps.is_available():
    execDevice = "mps"
    print("Using Apple Silicon GPU for vector encoding")
else:
    execDevice = "cpu"
    print("Using CPU for vector encoding")

model = SentenceTransformer(
    "all-MiniLM-L6-v2", device=execDevice
)

df = pd.read_json("./startups_demo.json", lines=True)

vectors = model.encode(
    [row.alt + ". " + row.description for row in df.itertuples()],
    show_progress_bar=True,
)

print(vectors.shape)

np.save("startup_vectors.npy", vectors, allow_pickle=False)
