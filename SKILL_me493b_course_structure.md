---
name: me493b-course-structure
description: >
  Reference for all structural, naming, and repository conventions for
  ME 493B "AI in Product Development" at UW Bothell (Spring 2026).
  Consult this file before creating any course file, notebook, folder,
  or spec document. Covers repo layout, file naming, notebook structure,
  spec document format, GitHub Classroom workflow, Canvas integration,
  and Copilot interaction patterns.
---

# ME 493B Course Structure Reference

## Course identity
- **Course:** ME 493B — AI in Product Development
- **Institution:** University of Washington Bothell
- **Term:** Spring 2026 (March 30 – June 5, 20 sessions, TTh 3:30–5:30 PM)
- **Instructor:** Scott Thielman, PhD (thielman@uw.edu)
- **Room:** UW1 041
- **Enrollment:** 24 students max
- **Credits:** 4

---

## Course architecture

### The Five Pillars (recurring vocabulary and rubric dimensions)

| Pillar | Short definition |
|--------|----------------|
| **Goal & Direction** | Specifying intent, writing requirements, directing AI toward outcomes |
| **Context Management** | RAG, memory, information architecture — what the model knows |
| **Tools & Integration** | MCP, APIs, function calling, connections to engineering systems |
| **Centaur Engineering** | Human-AI collaboration where the combination exceeds either alone |
| **Evaluation & Trust** | Verifying AI outputs at every scale, from response to full workflow |

### The Five Building Blocks (foundational concepts from "How AI Thinks" module)

These are the cognitive operations that underpin all AI systems. Taught in
MP1 Part A and referenced throughout the course:

| Building Block | What it means | Where it recurs |
|---|---|---|
| **Representation** | Turning real things into numbers | Embeddings in RAG (MP2), feature extraction (MP3), multimodal (MP4) |
| **Similarity** | Measuring how alike two things are | Document retrieval (MP2), design search (MP3), output evaluation (MP4) |
| **Prediction** | Estimating unknowns from patterns | Generative design (Wk 5), LLM generation is next-token prediction |
| **Classification** | Sorting things into categories | Quality evaluation, tool selection, trust calibration (Wk 8-9) |
| **Search & Retrieval** | Finding relevant items in a large space | RAG (MP2), semantic search, attention in Transformers |

### Product Development Spine

The course follows the engineering development lifecycle:
1. **Discover & Frame** (Weeks 3-4) → MP2
2. **Design & Explore** (Weeks 5-6) → MP3
3. **Build & Integrate** (Weeks 7-8) → MP3-MP4
4. **Test & Trust** (Weeks 8-9) → MP4
5. **Present & Reflect** (Week 10) → MP5

### Foundation Module: "How AI Thinks" (Weeks 1-2, Sessions 1-4)

Sessions 1-4 teach ML fundamentals as background for engineering decisions:
- Session 1: "Welcome to the Future" — course vision, AI timeline, five pillars
- Session 2: "From Data to Representations" — vectors, embeddings, training
- Session 3: "The Architecture of Intelligence" — tokens, Transformers, attention
- Session 4: "From Understanding to Generation" — LLM generation, diffusion, multimodal

---

## Assessment structure

| Assignment | Type | Points | Timeline | Pillar emphasis |
|-----------|------|--------|----------|----------------|
| hello_world | Setup (pass/fail) | 10 | Week 1 | Goal & Direction (intro) |
| MP1 | Individual, 2 weeks | 100 | Weeks 1-2 | Goal & Direction |
| MP2 | Individual, 2 weeks | 100 | Weeks 3-4 | Context Management |
| MP3 | Individual, 2 weeks | 100 | Weeks 5-7 | Tools & Integration |
| MP4 | Individual, 2 weeks | 100 | Weeks 7-9 | Centaur Engineering + Eval & Trust |
| Quiz 1 | In-class | 100 | Week 4 | Foundation + Pillars 1-2 |
| Quiz 2 | In-class | 100 | Week 9 | Pillars 3-5 |
| News Discussion | Rotating | 100 | All quarter | All pillars |
| MP5 / Final Presentation | Team (3-4), live | 300 | Week 10 | All pillars |
| **Total** | | **1,000** | | |

### Mini-project structure (MP1-MP4)

Each MP = **100 points**, **two-week timeline**, two parts:
- **Part A (50 pts):** Guided instructional exercise (Jupyter notebook) with
  learn→explore→solve pattern. Includes HOMEWORK cells with verifiable answers.
- **Part B (50 pts):** Applied engineering design problem evaluated across all
  five pillars with weighted emphasis. Constrained shared scenario for MP1-MP3;
  more open for MP4-MP5.

**Both Part A and Part B share a single due date** — 13 days after assignment,
due at 11:59 PM. There is no separate Part A checkpoint.

MP1-MP3 use multi-part guided format. MP4-MP5 give students more freedom.
Mini-projects ARE the homework — there is no separate homework category.

### Mini-project schedule

| MP | Assigned | Due (11:59 PM) | Pillar emphasis |
|----|----------|----------------|-----------------|
| MP1 | Tue, March 31 (Session 1) | Mon, April 13, 11:59 PM | Goal & Direction |
| MP2 | Tue, April 14 (Session 5) | Mon, April 27, 11:59 PM | Context Management |
| MP3 | Tue, April 28 (Session 9) | Mon, May 11, 11:59 PM | Tools & Integration |
| MP4 | Tue, May 12 (Session 13) | Mon, May 25, 11:59 PM | Centaur + Eval & Trust |
| MP5 | Tue, May 19 (Session 17) | Finals week | All pillars (team) |

Note: Each MP is assigned on a Tuesday and due at 11:59 PM 13 days later
(Monday night). The next MP is assigned the following Tuesday.

### Part A notebook pattern: Learn → Explore → Solve

Every section in a Part A notebook follows this arc:
1. **TEACH:** Pre-written code with rich commentary. Student runs and observes.
   Start at lowest dimensionality (2D), use intuitive data first.
2. **EXPLORE:** `# ✏️ YOUR TURN` cells with guided experiments.
3. **SOLVE:** `# 🎯 HOMEWORK` cells where students write code to answer a
   specific question with a verifiable answer (a name, number, or ranking).

### Part A grading (50 points)

| Component | Points | Criteria |
|-----------|--------|----------|
| Completion & Experimentation | 30 | All cells run. YOUR TURN cells show experimentation. HOMEWORK cells have working code with correct answers. |
| Reflections | 20 | Thoughtful reflections demonstrating observation and connection to course concepts. |

### Part B grading (50 points)

Evaluated across all five pillars with weighted emphasis:

| Pillar | MP1 | MP2 | MP3 | MP4 |
|--------|-----|-----|-----|-----|
| Goal & Direction | ★★★ | ★★ | ★★ | ★★ |
| Context Mgmt | ★ | ★★★ | ★★ | ★★ |
| Tools & Integration | ★ | ★ | ★★★ | ★★ |
| Centaur Engineering | ★★ | ★ | ★★ | ★★★ |
| Evaluation & Trust | ★★ | ★★ | ★★ | ★★★ |

---

## MP1 specifics (current project)

### MP1 Part A: "Under the Hood — How AI Thinks"
- Jupyter notebook teaching five building blocks (representation, similarity,
  prediction, classification, search)
- Five HOMEWORK problems with verifiable answers, progressing in complexity
- Uses fruits/movies/snacks for concept teaching, engineering data for application
- Real embedding model: `sentence-transformers` with `all-MiniLM-L6-v2`
- Capstone homework integrates all five sections into a mini search engine
- Spec: `specs/SPEC_MP1_PartA.md`

### MP1 Part B: "MiniClaw Gear Train Design"
- Framed as a design brief from "Jordan Chen, Engineering Manager, ACME Robotics"
- Students design a scaled-down 3D-printable version of the Hiwonder BigClaw gripper
- Key constraints: ~20% scale-down, PLA/PETG, hand-driven input wheel, 5-8N grip
- Deliverables: goal statement, design iteration log, calculation script, trust assessment
- Reference: https://www.hiwonder.com/products/bigclaw-mechanical-gripper
- Separate design brief document provided alongside assignment document

---

## GitHub infrastructure

### Accounts and repos
- **Instructor GitHub:** dr-thielman
- **Classroom org:** me493b-spring2026
- **Template repo:** dr-thielman/ai-in-pd-spring2026 (must be public)
- **Student repos:** Private, auto-created in me493b-spring2026 org

### Critical GitHub Classroom lessons learned
- Template repo must live under **dr-thielman** (personal account),
  NOT under the classroom org (circular reference error)
- Do NOT set "Supported editor" when creating assignments (causes save error)
- Starter code can only be set during initial assignment creation —
  cannot be added or changed afterward; delete and recreate if needed
- Students do NOT need to be pre-added to the org — invitation link
  grants access automatically

---

## Repository folder structure

```
ai-in-pd-spring2026/                 ← lives under dr-thielman
├── hello_world.ipynb                ← setup lesson, repo root
├── README.md                        ← student-facing setup instructions
├── requirements.txt                 ← shared Python deps
├── .devcontainer/
│   └── devcontainer.json            ← Codespaces config
│
├── specs/                           ← visible to students (Goal & Direction examples)
│   ├── SPEC_hello_world.md
│   ├── SPEC_MP1_PartA.md
│   └── ...
│
├── MP1/
│   ├── Part A/
│   │   └── MP1_PartA_Under_the_Hood.ipynb
│   └── Part B/
│       └── (reference data, BigClaw specs, etc.)
│
├── MP2/
│   ├── Part A/
│   └── Part B/
│
├── MP3/
│   ├── Part A/
│   └── Part B/
│
├── MP4/
│   ├── Part A/
│   └── Part B/
│
└── MP5/
```

---

## File naming conventions

### Notebooks
| Convention | Example |
|-----------|---------|
| `MP{N}_Part{X}_Descriptive_Name.ipynb` | `MP1_PartA_Under_the_Hood.ipynb` |
| `hello_world.ipynb` | Setup lesson at repo root |

### Spec documents
| Convention | Example |
|-----------|---------|
| `SPEC_MP{N}_Part{X}.md` | `SPEC_MP1_PartA.md` |

- All specs live in `specs/` folder
- UPPERCASE prefix `SPEC_` makes them visually distinct

### Assignment documents (Word)
- `MP{N}_The_First_Build.docx` — student-facing assignment document
- `MP{N}_PartB_Design_Brief.docx` — in-world scenario document

These are distributed via Canvas, NOT committed to the GitHub repo.

---

## Spec document format

Every notebook must have a corresponding spec in `specs/`. Specs serve
two purposes: (1) build instructions for Claude Code to generate the
notebook, and (2) visible to students as Goal & Direction examples.

### Required spec sections (see SPEC_hello_world.md for a complete example)

1. **Header:** Notebook filename, course, author, file locations
2. **Purpose:** What this notebook teaches (1-3 sentences)
3. **Primary pillar emphasis**
4. **Student prerequisites**
5. **Tone**
6. **Session alignment:** Which lecture sessions this connects to
7. **Notebook structure:** Section-by-section breakdown with:
   - The question the section answers
   - Data to use (self-contained, no external files)
   - Concepts to teach (start low-dimensional, intuitive data first)
   - YOUR TURN experiments (specific things to try)
   - HOMEWORK problems (definite verifiable answers)
   - Dig Deeper keywords and AI prompts
   - Forward connections to later course content
8. **Grading alignment**
9. **Technical requirements**
10. **Build notes for Claude Code**

---

## Notebook authoring rules

### Code cells
- Pre-written TEACH cells: full working code with rich inline comments
- YOUR TURN cells: clear instructions with specific things to try
- HOMEWORK cells: starter scaffolding with `# YOUR CODE HERE` placeholders
  and `print()` statements so cells run without errors but produce
  placeholder output students must replace
- Variable names and data that carry forward must be noted in the spec

### Markdown cells
- Cells students must edit: prefix with **✏️ YOUR TURN** or **🎯 HOMEWORK**
- Every formula shown alongside a concrete numerical example
- No jargon without inline definition on first use
- Forward connection callouts: "You'll see this again when..."
- Include Codespace save warning in submission section

### Copilot interaction — platform agility
Students explore inline completion, Copilot Chat, and Copilot CLI.
Do NOT prescribe a single mode. The ability to find effective AI
interaction patterns is itself a learning objective.

### Cell ordering
- All notebooks must run top-to-bottom without errors in a fresh Codespace
- No hidden state dependencies
- sentence-transformers install uses try/except with --break-system-packages

---

## Devcontainer configuration

```json
{
  "name": "ME 493B — AI in Product Development",
  "image": "mcr.microsoft.com/devcontainers/python:3.11",
  "customizations": {
    "vscode": {
      "extensions": [
        "GitHub.copilot",
        "GitHub.copilot-chat",
        "ms-python.python",
        "ms-toolsai.jupyter"
      ],
      "settings": {
        "python.defaultInterpreterPath": "/usr/local/bin/python",
        "editor.inlineSuggest.enabled": true,
        "github.copilot.enable": { "*": true, "jupyter": true }
      }
    }
  },
  "postCreateCommand": "pip install -r requirements.txt"
}
```

## Standard requirements.txt

```
numpy
pandas
matplotlib
scikit-learn
sentence-transformers
jupyter
```

---

## Student submission workflow

```
1. Canvas: read assignment instructions
2. Canvas: click GitHub Classroom invitation link
3. GitHub: auto-creates private repo
4. GitHub: open repo → Code → Codespaces → New codespace
5. Codespaces: complete notebook
6. Codespaces: commit and push via Source Control GUI
7. Canvas: paste GitHub repo URL as Website URL submission
8. Instructor: review on GitHub, enter grade in Canvas
```

---

## What NOT to do

- Do not put solution code in student-facing notebooks
- Do not commit executed notebooks to the template repo
- Do not use Google Colab — course uses GitHub Codespaces exclusively
- Do not reference Claude Code in student materials — students use Copilot
- Do not use hyphens in notebook filenames (use underscores)
- Do not set a Supported editor in Classroom assignments
- Do not host the template repo in the classroom org
- Do not use ML where physics or known equations suffice — ML should
  add genuine value, not replace straightforward calculations
- Do not train models on problems where lookup tables give the answer
