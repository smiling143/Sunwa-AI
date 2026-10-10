# Sunwa-AI (सुनवाई-AI)
**Public Grievance Root-Cause & Action Prioritizer**  
*Civic Technology, NLP, Geospatial Clustering & Administrative Action Queues*  
*Hackathon Problem Statement 7 — Complete Project Rebuild*

---

## 1. Project Overview & Problem Statement
Municipal administrations in rapidly expanding urban centers receive thousands of unstructured citizen complaints weekly across multiple languages, dialects, and scripts (English, Hindi, Marathi, and Romanized forms). Traditional civic grievance management portals suffer from fundamental bottlenecks:
1. **Isolated Grievance Silos**: Complaints are treated as independent tickets, obscuring localized surges and systemic failures.
2. **False Generalization**: Categorizing all reports under generic buckets (e.g., "Roads" or "Water") lumps unrelated physical issues together.
3. **Subjective Prioritization**: Decisions often rely on manual sorting or loud-voice bias, lacking transparent, explainable criteria.
4. **Lack of Follow-up Accountability**: Administrations lack systematic tracking to observe whether interventions correlate with a reduction in citizen complaints.

**Sunwa-AI (सुनवाई-AI)**, pronounced *"Sunwaai"*, transforms high-volume, multilingual citizen grievances into explainable, geographically constrained, and actionable intelligence for municipal decision-makers in Navi Mumbai (Nerul, Panvel, Vashi, Kharghar, and Belapur).

---

## 2. Core Architecture & Capabilities

```
+---------------------------------------------------------------------------------------+
|                                    PRESENTATION LAYER                                 |
|   +---------------------------------------+   +-----------------------------------+   |
|   |    Administrative Response Portal     |   |     Citizen Grievance Portal      |   |
|   |  - Executive Overview                 |   |  - Multilingual Form (EN/HI/MR)   |   |
|   |  - Interactive Incident Map (Folium)  |   |  - Reference ID Receipt           |   |
|   |  - Explainable Priority Queue         |   |  - Zero Image-Upload Footprint    |   |
|   |  - Evidence Dossier Panel             |   |  - Shared DB Immediate Ingestion  |   |
|   |  - Action Command Center              |   +-----------------------------------+   |
|   |  - Simulated Municipal Alert Queue    |                                           |
|   |  - Intervention Impact Tracker        |                                           |
|   +---------------------------------------+                                           |
+---------------------------------------------------------------------------------------+
                                           |
+---------------------------------------------------------------------------------------+
|                                  INTELLIGENCE ENGINE                                  |
|                                                                                       |
|   [1. Text Normalization]  Unicode NFKC, Devanagari preservation, lowercase Latin     |
|              |                                                                        |
|   [2. Deterministic Resolver] Exact Alias Match -> Multilingual/Fuzzy -> Region Check  |
|              | (If Unresolved/Ambiguous)                                              |
|   [3. Constrained Groq Fallback] -> Model: openai/gpt-oss-20b (Validated vs Catalogue)|
|              |                                                                        |
|   [4. Multilingual Embeddings] paraphrase-multilingual-MiniLM-L12-v2 (or TF-IDF)       |
|              |                                                                        |
|   [5. Incident Clustering] Semantic Cosine Sim + Distance (<=1.5km) + Category Match  |
|              |                                                                        |
|   [6. Pattern Analyzer] Localized Incident vs Surge vs Recurring vs Distributed vs Haz|
|              |                                                                        |
|   [7. Priority Engine] P = 0.25S + 0.20A + 0.15D + 0.25R + 0.15T (Safety Escalation)  |
|              |                                                                        |
|   [8. Department Recommender] Prescriptive Action & Municipal Department Mapping      |
+---------------------------------------------------------------------------------------+
                                           |
+---------------------------------------------------------------------------------------+
|                                    PERSISTENCE LAYER                                  |
|   - CSV Complaint Data Store (data/complaints.csv)                                    |
|   - Curated Verified Landmark Catalogue (data/landmarks.json)                         |
|   - SQLite State Store (data/sunwa_state.db: actions, alerts, interventions)          |
+---------------------------------------------------------------------------------------+
```

---

## 3. Key Methodological Innovations

### Requirement A — Multilingual Semantic Grouping
Citizen grievances describing the identical physical defect in diverse linguistic forms are recognized as related:
- *"There is a massive pothole near the college."*
- *"Road has a very deep khadda."*
- *"कॉलेजच्या समोर रस्त्यावर खूप मोठा खड्डा पडला आहे."*
- *"SIES College ke samne bada gaddha hai."*

Complaints are encoded into 384-dimensional dense vectors using `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` (with a character n-gram TF-IDF offline fallback). Vector cosine similarity handles cross-lingual code-switching without calling external translation APIs.

### Requirement B — Localized Incidents vs. Systemic Patterns
Sunwa-AI strictly prevents merging complaints across distinct geographic coordinates or dissimilar categories:
- **Localized Incident**: Standard civic defect at a single landmark with corroborated reports.
- **Complaint Surge**: $\ge 3$ complaints at the same landmark within $\le 3.5$ days.
- **Recurring Infrastructure Issue**: Chronic defect spanning $> 14$ days or $\ge 4$ recurrences at the same landmark.
- **Distributed Systemic Issue**: Same category (e.g. streetlights or potholes) appearing concurrently across multiple distinct sites in a region.
- **Potential Acute Hazard**: High-voltage electrical wire, sparking, or open trench requiring immediate escalation.
- **Insufficient Evidence**: Isolated complaint with unresolved location coordinates.

### Requirement C & D — Deterministic Priority Engine & Explainability
Priority is computed deterministically using the standardized formula:
$$P = 0.25\,S + 0.20\,A + 0.15\,D + 0.25\,R + 0.15\,T$$

Where factors (normalized to 0–100 scale) represent:
- **$S$ (Severity)**: Physical defect severity from observed citizen reports or category baseline.
- **$A$ (Affected Population / Density)**: Transit hub, college gate, market, or public park density.
- **$D$ (Duration / Persistence)**: Days elapsed since earliest report.
- **$R$ (Safety Risk Assessment)**: Hazard keyword scan and risk indicators.
- **$T$ (Recurrence / Frequency)**: Grievance repetition count.

#### Safety Escalation Rule:
If acute safety risk $R \ge 85.0$ (e.g. live sparking electrical cable or open manhole), the incident is **immediately escalated to Critical priority** ($P \ge 80.0$) with explicit audit justification recorded in the Evidence Dossier.

### Requirement E — Intervention Tracking & Observational Impact
Interventions record pre- and post-intervention complaint counts over identical measurement windows (e.g. 14 days before vs 14 days after).
- **Zero-Baseline Handling**: Safe calculation prevents division-by-zero or misleading percentages when baseline counts are zero.
- **Non-Causality Disclaimer**: Prominently warns decision-makers that complaint reductions are observational correlations and do not constitute proof of physical engineering resolution or municipal causation.

---

## 4. Strict Groq LLM Configuration & Fallback Discipline

Sunwa-AI enforces strict architectural rules regarding LLM usage:
1. **Deterministic Resolver Runs First**: Unicode NFKC normalization, exact multilingual alias matching, and controlled fuzzy matching (`rapidfuzz`) are executed first.
2. **Groq is ONLY a Location Fallback**: The LLM is never invoked for confident deterministic matches, never calculates priority scores, and never invents complaints.
3. **Provider**: GROQ
4. **Environment Variable**: `GROQ_API` (loaded strictly via `python-dotenv`). Never printed, logged, or exposed.
5. **Configured Model**: `openai/gpt-oss-20b`
6. **Constrained Validation**: Suggested landmarks from Groq are strictly validated against `data/landmarks.json`. Any invented or hallucinated landmark is automatically rejected.
7. **Offline Capability**: The application functions seamlessly in pure deterministic mode if `GROQ_API` is not set or network is offline.

---

## 5. Administrative Lifecycle & Alert Simulation

### Administrative Action State Machine:
Actions follow a validated state machine persisted in SQLite:
$$\text{pending\_review} \longrightarrow \text{ready\_to\_dispatch} \longrightarrow \text{alert\_queued} \longrightarrow \text{acknowledged} \longrightarrow \text{assigned} \longrightarrow \text{in\_progress} \longrightarrow \text{resolved} \longrightarrow \text{closed}$$

Arbitrary skips are strictly rejected by the lifecycle validator.

### Municipal Alert Queue:
- Explicitly labelled: `DEMO MODE — SIMULATED MUNICIPAL ALERT`.
- Generates structured dispatch payloads (`ALT-2026-XXXX.json`) available for download.
- Simulated acknowledgments are recorded explicitly; no fictitious government APIs are called.

---

## 6. Directory Structure

```
ipl/
├── app.py                      # Main application entry point & portal router
├── pytest.ini                  # Pytest configuration
├── requirements.txt            # Python dependencies
├── .env.example                # Template for environment configuration
├── .gitignore                  # Protection for credentials and caches
│
├── models/
│   └── schemas.py              # Pydantic schemas for complaints, clusters, actions
│
├── engine/
│   ├── data_loader.py          # CSV & SQLite persistence layer
│   ├── complaint_normalizer.py # Unicode NFKC and multilingual text normalizer
│   ├── location_resolver.py    # Deterministic multi-stage location resolver
│   ├── llm_client.py           # Constrained Groq fallback (openai/gpt-oss-20b)
│   ├── semantic_engine.py      # Multilingual sentence embeddings & category engine
│   ├── clustering_engine.py    # Geospatial, semantic, and temporal clustering
│   ├── pattern_analyzer.py     # Root-cause pattern classifier
│   ├── priority_engine.py      # Numerical scoring engine & safety escalation
│   ├── recommendation_engine.py# Departmental & action mapping
│   ├── action_manager.py       # Validated state machine & action tasks
│   ├── alert_manager.py        # Simulated municipal alert dispatcher
│   ├── intervention_manager.py # Before/after observational impact analyzer
│   └── pipeline.py             # End-to-end processing pipeline orchestrator
│
├── components/
│   ├── admin_dashboard.py      # Administrative portal views router
│   ├── overview.py             # Executive overview & operational metrics
│   ├── priority_queue.py       # Prioritized grievance queue & manual overrides
│   ├── evidence_panel.py       # Deep-dive explainable evidence dossier
│   ├── incident_map.py         # Folium map & quarantined unresolved queue
│   ├── action_center.py        # Action Command Center & lifecycle controls
│   ├── alert_queue.py          # Simulated alert queue & payload downloader
│   ├── intervention_tracking.py# Remediation intervention impact tracker
│   ├── citizen_portal.py       # Citizen grievance submission & receipt generator
│   └── shared_ui.py            # WCAG-compliant styles & localization helpers
│
├── locales/
│   ├── en.json                 # English localization dictionary
│   ├── hi.json                 # Hindi localization dictionary (Devanagari)
│   └── mr.json                 # Marathi localization dictionary (Devanagari)
│
├── data/
│   ├── complaints.csv          # Canonical complaint store (preserves original text)
│   ├── landmarks.json          # Curated landmark catalogue (Nerul, Panvel, Vashi, etc.)
│   ├── interventions.json      # Initial remediation records
│   └── sunwa_state.db          # SQLite persistent state database
│
└── tests/
    ├── conftest.py
    ├── test_data_loader.py
    ├── test_location_resolver.py
    ├── test_groq_fallback.py
    ├── test_semantic_clustering.py
    ├── test_priority_engine.py
    ├── test_action_manager.py
    ├── test_alert_manager.py
    ├── test_intervention_manager.py
    ├── test_localization.py
    └── test_integration.py
```

---

## 7. Setup & Execution Instructions

### 1. Prerequisites
- Python 3.10 – 3.12 (Tested on Python 3.12 64-bit Windows)
- CPU execution supported (No GPU or CUDA required)

### 2. Installation
```bash
pip install -r requirements.txt
```

### 3. Environment Configuration
Create a `.env` file in the project root:
```ini
GROQ_API=your_groq_api_key_here
```
*(Sunwa-AI loads `GROQ_API` directly with `python-dotenv`. The application remains fully functional in deterministic mode if the key is absent.)*

### 4. Running the Application
```bash
streamlit run app.py
```

### 5. Accessing the Portals
- **Administrative Response Portal**: Open `http://localhost:8501`. Use the sidebar to switch between Overview, Incident Map, Priority Queue, Action Center, Alert Queue, and Evidence Dossier.
- **Citizen Grievance Portal**: Select **"🗣️ Citizen Grievance Portal"** in the sidebar portal switcher, or navigate directly via `http://localhost:8501/?portal=citizen`.
- **Language Switching**: Select English, हिंदी, or मराठी in the sidebar selector.

### 6. Running the Automated Test Suite
```bash
pytest -v
```

---

## 8. End-to-End Demonstration Checklist
1. **Language Switching**: Switch the administrative interface to **हिंदी** or **मराठी**; verify all navigational headings, metrics, and labels update in Devanagari while original complaint texts remain unaltered.
2. **Citizen Grievance Submission**: Switch to the **Citizen Portal**, submit a grievance in Marathi or Hindi (e.g. *"कॉलेजच्या समोर रस्त्यावर खूप मोठा खड्डा पडला आहे"* in Nerul), and receive a verified reference receipt (`CMP-2026-XXXX`).
3. **Administrative Ingestion**: Switch to the **Administrative Portal**; verify the complaint immediately appears in the dataset, is clustered with existing SIES Nerul pothole grievances, and updates the priority score.
4. **Location Resolution**: Verify deterministic resolution matches the landmark; inspect the Evidence Dossier to observe the exact match confidence.
5. **Acute Safety Escalation**: Inspect the Vashi electrical sparking cluster; verify it triggers the safety override ($R=95$) and escalates directly to Critical.
6. **Action & Alert Lifecycle**: Create an action task from the Priority Queue, advance its state from `pending_review` $\rightarrow$ `ready_to_dispatch` $\rightarrow$ `alert_queued`, download the simulated JSON payload, and record acknowledgment.
7. **Intervention Impact Tracking**: Review before-and-after grievance counts for the SIES asphalt patching intervention; verify that non-causality disclaimers are prominently displayed.
