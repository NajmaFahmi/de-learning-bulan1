# DE Learning — Bulan 1: Fondasi Data Engineering

Repositori ini mendokumentasikan pembelajaran bulan pertama dalam roadmap **Data Engineering self-study**.

## Tujuan Bulan 1

Membangun fondasi yang solid, fokus pada SQL lanjut, Python pipeline, Linux/Bash, dan Git workflow profesional.

---

## Stack & Environment

| Komponen | Versi |
|----------|-------|
| Python | 3.13.4 (Homebrew) |
| PostgreSQL | 16.13 (Homebrew) |
| OS | macOS (Apple Silicon) |
| SQL Client | DBeaver 26.0.2 |
| Libraries | pandas, sqlalchemy, psycopg2-binary, pydantic, python-dotenv, pytest |

---

## Struktur Belajar

### Week 1 — SQL Fundamentals
Topik yang dikuasai:
- Basic SQL Query

Dataset: **dvdrental** (PostgreSQL sample database — 15 tabel, 1000 film)

### Week 2 — SQL Lanjut & Python Pipeline
Topik yang dikuasai:
- `EXPLAIN ANALYZE` — query optimization
- Idempotency dan UPSERT pattern (`ON CONFLICT DO UPDATE`)
- Python ETL pipeline dengan:
  - `SQLAlchemy` — database connection & ORM
  - `Pydantic` — data validation & schema enforcement
  - `python-dotenv` — secrets management
  - Structured logging dan error handling

### Week 3 — Linux, Bash & Git
Topik yang dikuasai:
- Linux filesystem, permissions (`chmod`, `chown`), process management
- Bash scripting: variables, loops, functions, conditionals
- Advanced Bash: `trap`, `cron`, structured logging, exit codes
- Git core: staging, commits, branching, merging
- Git professional workflow: PR process, tagging (`v0.1.0`, `v0.2.0`), `.gitignore`

### Week 4 — Mini Project ETL End-to-End
Tiga ETL pipeline dibangun dari nol:

| Project | Dataset | Highlights |
|---------|---------|------------|
| **ETL dvdrental** | dvdrental PostgreSQL | CSV → Pydantic validation → transform → UPSERT |
| **ETL Delayed Flights** | US Flight Delays (public) | Handling missing values, date parsing, aggregation |
| **ETL Olist** | Brazilian E-Commerce (Kaggle) | Multi-table join, incremental load pattern |

Setiap project memiliki:
- Logging terstruktur
- Error handling dengan retry logic
- Unit test dengan `pytest`
- README dokumentasi

---

## Deliverable Utama

```
bulan_1/
├── week1_sql/
│   ├── queries/          # SQL queries per topik
│   └── mini_quiz/        # Soal dan jawaban SQL
├── week2_pipeline/
│   ├── etl_pipeline.py   # Pipeline utama
│   ├── models.py         # Pydantic models
│   ├── database.py       # SQLAlchemy setup
│   └── tests/            # pytest unit tests
├── week3_linux_git/
│   ├── scripts/          # Bash scripts
│   └── weekly_report.sh  # Script laporan mingguan
└── week4_projects/
    ├── etl_dvdrental/
    ├── etl_delayed_flights/
    └── etl_olist/
```

---

## Konsep Kunci yang Dipelajari

**SQL**
- Window functions memungkinkan kalkulasi agregat tanpa menghilangkan row detail
- CTE membuat query kompleks lebih readable dan maintainable
- `EXPLAIN ANALYZE` adalah tools utama untuk debug query yang lambat

**Python Pipeline**
- Pydantic enforce schema di runtime — mencegah data kotor masuk ke database
- UPSERT pattern (`ON CONFLICT`) membuat pipeline idempoten — aman dijalankan berulang
- Separation of concerns: extract, validate, transform, load harus dipisah

**Linux & Bash**
- `trap` untuk handle script failure gracefully
- Cron untuk scheduling sederhana sebelum pakai Airflow
- Structured logging dengan timestamp membuat debugging jauh lebih mudah

**Git**
- Feature branch workflow: tidak pernah commit langsung ke `main`
- Semantic versioning dengan tags untuk mark milestone
- PR sebagai review gate sebelum merge

---

## Progres & Status

- [x] Week 1 — SQL Fundamentals
- [x] Week 2 — SQL Lanjut & Python Pipeline
- [x] Week 3 — Linux, Bash & Git
- [x] Week 4 — Mini Project ETL (3 projects)
- [x] Bulan 1 Complete ✓

**Next:** Bulan 2 — Apache Airflow, dbt, Data Modeling → [de-learning-bulan2](https://github.com/NajmaFahmi/de-learning-bulan2)

---

## Roadmap Keseluruhan

| Bulan | Fokus | Status |
|-------|-------|--------|
| 1 | SQL, Python Pipeline, Linux, Git | ✅ Selesai |
| 2 | Airflow, dbt, Data Modeling | 🔄 In Progress |
| 3 | Spark, Docker, Data Lakehouse | ⏳ Upcoming |
| 4 | Data Quality, Testing, Observability | ⏳ Upcoming |
| 5 | Kafka, CI/CD, GitHub Actions | ⏳ Upcoming |
| 6–8 | Portfolio, Interview Prep, Job Hunting | ⏳ Upcoming |

---

*Self-study roadmap — target: Remote Data Engineer position*
