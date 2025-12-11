
# Qdrant Neural Search - Quickstart

This project demonstrates how to run a neural search API using Qdrant and FastAPI. It is based on the official [Qdrant beginner neural search tutorial](https://qdrant.tech/documentation/beginner-tutorials/neural-search/), add was built using [uv](https://docs.astral.sh/uv/).

---

## Prerequisites

- [uv](https://docs.astral.sh/uv/) (for dependency management and running scripts)
- [Docker](https://www.docker.com/) (for running Qdrant)
- Python 3.14+ (should work on lower version but this is what I built it in)

---

## 1. Install Python dependencies

```bash
uv sync
```

---

## 2. Start Qdrant with Docker

Pull and run the official Qdrant image:

```bash
docker run -d \
    --name qdrant-learn \
    -p 6333:6333 \
    -v $(pwd)/qdrant_storage:/qdrant/storage \
    qdrant/qdrant
```

Visit [http://localhost:6333/](http://localhost:6333/) to verify Qdrant is running.

> All data uploaded to Qdrant is saved inside the `./qdrant_storage` directory and will be persisted even if you recreate the container.

---

## 3. Prepare your data

Your data should be in `startups_demo.json`, with one JSON object per line. Example:

```json
{
   "name": "SaferCodes",
   "images": "https://safer.codes/img/brand/logo-icon.png",
   "alt": "SaferCodes Logo",
   "description": "QR codes systems for COVID-19.\nSimple tools for bars, restaurants, offices, and other small proximity businesses.",
   "link": "https://safer.codes",
   "city": "Chicago"
}
```

---

## 4. Encode vectors
To conduct a neural search on startup descriptions, you must first encode the description data into vectors. To process text, I'm using the pre-trained model `all-MiniLM-L6-v2` from [Hugging Face](https://huggingface.co/models) using the [sentence transformers](https://sbert.net/) module.

```bash
uv run prepare_vectors.py
# This will create startup_vectors.npy
```

---

## 5. Upload vectors to Qdrant

At this point, you should have startup records in the `./startups_demo.json` file, encoded vectors in `./startup_vectors.npy` and Qdrant running on a local machine. Now you just need to upload all startup data and vectors into the search engine.

```bash
uv run upload_vectors.py
```

---

## 6. Run the FastAPI search service
Now that all the preparations are complete, let’s startup FastAPI framework and run the a neural search.
```bash
uv run service.py
```

The API will be available at [http://localhost:8000/api/search](http://localhost:8000/api/search).

**OR** Search via the command:

```bash
curl 'http://localhost:8000/api/search?q=rentals'
```

---

## Project Structure

- `startups_demo.json` — Input data
- `prepare_vectors.py` — Vector encoding
- `startup_vectors.npy` — Saved vectors
- `upload_vectors.py` — Upload to Qdrant
- `neural_searcher.py` — Search logic
- `service.py` — FastAPI service

---

## License

MIT
