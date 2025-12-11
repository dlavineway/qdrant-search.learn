
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

## Practical use cases

1. **Internal document search for operations & compliance**

    You likely have manuals, SOPs, safety rules, customs forms and training docs.
    - Build a semantic search over policies so any dispatcher/manager can ask plain English and get the right section back.
    - This beats keyword search when terms vary (e.g., “hazardous goods rules vs dangerous goods regs”).

    This saves time and cuts mistakes.

2. **Driver support knowledge base**

    Drivers ask the same questions over and over (routes, pay, equipment issues, hours of service).

    - Index past tickets, Slack/Teams chats, driver handbook Q&As.
    - Provide a search API for support staff or an internal bot.

    Improves support speed and accuracy for drivers.

3. **Customer service & freight status queries**

    Your customer service people handle queries like:

    - “Where’s my refrigerated load from Winnipeg?”
    - “Any delays on the Ontario corridor?”

    Build a semantic retriever across:

    - Shipment updates
    - GPS tracking notes
    - Delay logs
    - Then feed results into a simple response app or assistant.

    Better than filtering by exact keywords.

4. **Load-to-carrier matching / loadboard enhancement**

    You already have a load board and partner network. Instead of keyword filters:

    - Embed load descriptions and carrier profiles.
    - When a broker enters a free-text request (“temperature controlled from Calgary to Chicago tomorrow”), return the best candidate carriers.

    That makes matching smarter for contracts and spot loads.

5. **Knowledge extraction from driver logs/claims**

    There’s a ton of unstructured text in:
    - Driver log notes
    - Incident reports
    - Claims descriptions

    Vector search can help you:
    - Find similar past incidents
    - Identify patterns (e.g., recurring trailer issues)
    - Speed claims investigation

    This cuts investigation time.

6. **Hiring & training support**

    For HR and training teams:
    - Index job descriptions, training materials, and onboarding docs.
    - Provide a tool where a recruiter or new employee can ask for specifics (“What’s the finishing program detail?”) and get exact text snippets.

    It’s faster than manual searches through PDFs and folders.

---

## License

MIT
