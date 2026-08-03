# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agentic Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

I asked the agent to help me make the recommender more realistic and more transparent. I wanted it to suggest bonus features, add a diversity fix, and make the output easier to read.

**Prompts used:**

"How can I get bonus points?"

"Please add an artist diversity penalty, a second ranking mode, and a readable table output. Keep the changes small and make sure the explanations match the score."

"Update the model card and write down what the agent changed and what I checked manually."

**What did the agent generate or change?**

The agent updated `src/recommender.py` to support a diversity penalty and multiple ranking modes. It updated `src/main.py` to print an ASCII table. It also updated `model_card.md` and this file so the stretch work is documented.

**What did you verify or fix manually?**

I ran the app after each change to make sure the CSV still loaded and the recommendation list still printed. I checked the output to confirm that the artist penalty reduced repetition and that the table was readable.

---

## Design Pattern (SF10)

> Document how AI helped you choose or implement a design pattern.

**Which design pattern did you use?**

Strategy.

**How did AI help you brainstorm or implement it?**

AI helped me compare a few bonus ideas and pick the smallest one that would still matter. It suggested a clean way to separate ranking behavior so I could switch modes without rewriting the whole recommender.

**How does the pattern appear in your final code?**

The pattern appears in `recommend_songs`, which now supports `balanced`, `genre_first`, and `energy_first` ranking modes. `main.py` selects one mode and passes it into the recommender.

---

## Retrieval-Augmented Generation (RAG)

> Document how AI helped you design and implement RAG in your project.

**What task did you give the agent?**

I asked for help adding a RAG feature to the recommender, since the assignment required at least one advanced AI capability. I wanted the system to generate natural-language explanations for recommendations, grounded in real data rather than free-form LLM output, and fully integrated into the main app rather than a standalone script.

**Prompts used:**

"How can I add RAG to my existing recommender in a way that's realistic for a 2-day timeline and adds real portfolio value?"

"Help me design a retrieval layer and generation layer that plug into my existing recommend_songs function without changing it."

"Add error handling, logging, and a fallback so the app never crashes if the API key is missing or the call fails."

**What did the agent generate or change?**

The agent created three new files: `src/knowledge_base.py` (a small local reference dataset on genres/moods), `src/retriever.py` (gathers song attributes, score data, and knowledge base notes into a single context object), and `src/rag_explainer.py` (sends that context to the Claude API with a prompt that restricts it to only the provided facts, with a deterministic fallback if the API is unavailable). It also updated `src/main.py` to call this pipeline for each recommendation and print the results, and added logging to `logs/app.log`.

**What did you verify or fix manually?**

I ran the app after each change to confirm the recommendation table still printed correctly and that the AI-generated explanations section appeared without errors. I found and fixed a bug where the log file was created before its folder existed, causing a crash on a fresh clone — I added `os.makedirs("logs", exist_ok=True)` before the logging setup to fix it. I also checked `retriever.py`'s type hints, since an invalid `List[str] or str` annotation needed to be corrected to `Union[List[str], str]`. I confirmed the fallback path works correctly by running the app without an API key set and checking that `logs/app.log` recorded the fallback warnings as expected.

---

## Agentic Workflow Enhancement (Stretch Feature)

> Documenting the multi-step reasoning added to the RAG explanation pipeline.

**What was added:**

The explanation pipeline now runs two steps instead of one: (1) generate an explanation grounded in retrieved context, then (2) a second, separate AI call verifies whether that explanation only used facts present in the context, flagging it if not. This is implemented in `verify_explanation()` in `src/rag_explainer.py`, and wired into `main.py`'s `print_ai_explanations()` function so every recommendation goes through both steps.

**Reasoning trace (per recommendation):**

1. **Retrieve** — gather song attributes, score breakdown, and genre/mood/artist notes (`retriever.py`)
2. **Generate** — produce a natural-language explanation using only the retrieved context (`generate_explanation()`)
3. **Verify** — a second AI call checks the explanation against the same context and returns `VALID` or `INVALID: <reason>` (`verify_explanation()`)
4. **Report** — the explanation is printed alongside its verification status (`verified`, `flagged: <reason>`, or `unverified` if the API is unavailable)

**What I verified manually:**

I ran the full pipeline without an API key configured and confirmed every recommendation correctly reported `[Self-check: unverified (API unavailable)]` instead of crashing or silently skipping the verification step. This confirmed the agentic step degrades gracefully in the same way the generation step does, using the same fallback pattern.