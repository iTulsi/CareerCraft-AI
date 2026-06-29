# CareerCraft AI Dataset Design

This milestone defines the labelled dataset foundation for supervised
resume-to-job matching. It does not add model training code, LangChain, a
vector database, or deployment infrastructure.

CareerCraft will compare three matching approaches:

1. Deterministic skill baseline
2. Pretrained embedding model
3. Fine-tuned embedding model

## Label Schema

Each resume/job pair receives one overall label and three dimension labels.

Overall labels:

- `0`: unsuitable
- `1`: weak match
- `2`: reasonable match
- `3`: strong match

Dimension labels use the same `0` to `3` scale:

- `skills_label`
- `experience_label`
- `education_label`

## Overall Annotation Rules

Use the overall label to answer: "How suitable is this candidate for this job?"

- `0` unsuitable: The resume is clearly outside the role. Core skills,
  experience, or required background are missing.
- `1` weak match: The resume has limited overlap. The candidate may have some
  adjacent skills, but important requirements are missing or too shallow.
- `2` reasonable match: The resume covers several important requirements and
  could be considered, but has notable gaps in depth, domain, seniority, or
  credentials.
- `3` strong match: The resume closely matches the job's core skills,
  experience level, and required background, with only minor gaps.

Dimension labels should be assigned independently. For example, a candidate may
have strong skills but weak education alignment if the role explicitly requires
a specific degree or certification.

## Synthetic Examples

These examples are synthetic and contain no personal data.

- `0` unsuitable: Resume describes retail cashier experience and basic office
  tools. Job asks for a senior backend engineer with Python, FastAPI, SQL,
  distributed systems, and cloud deployment experience.
- `1` weak match: Resume describes a frontend developer with JavaScript and
  React. Job asks for a machine learning engineer with Python, model training,
  experiment tracking, and data pipelines.
- `2` reasonable match: Resume describes a Python backend developer with
  FastAPI, SQL, Docker, and two API projects. Job asks for backend engineering
  plus AWS, Kubernetes, and three years of production operations experience.
- `3` strong match: Resume describes a backend engineer with Python, FastAPI,
  PostgreSQL, Docker, AWS deployment, CI, monitoring, and production API
  ownership. Job asks for the same stack and similar responsibility level.

## Hard Negatives

Hard negatives are resume/job pairs that look similar by keywords but are not
good matches. Include them deliberately because they reveal whether semantic
matching improves beyond keyword overlap.

Identify hard negatives from similar job families, such as:

- Frontend developer vs full-stack developer
- Data analyst vs data scientist
- Machine learning engineer vs backend AI application engineer
- DevOps engineer vs backend engineer with basic Docker usage
- Java backend engineer vs JavaScript frontend engineer

Annotators should mark the pair according to actual role fit, not just shared
terms.

## Privacy

Names, emails, phone numbers, addresses, links to personal profiles, employer
IDs, government IDs, and other personal identifiers must be removed before data
is stored for annotation or evaluation.

Do not include real candidate identity details in examples, tests, or templates.

## Label Sources

Allowed `label_source` values:

- `human`
- `llm_assisted`

LLM-generated labels are weak labels. They may help triage or pre-label data,
but they must not be treated as verified ground truth.

Validation and locked-test sets must be human-reviewed.

## Disagreement Handling

For selected pairs, two reviewers independently assign labels. When labels
disagree, reviewers discuss the case, record the final decision, and add a
short reason in `label_reason`.

## Leakage Prevention

Prevent train/validation/test leakage by grouping related records:

- Use `candidate_group_id` for multiple versions of the same or closely related
  resume.
- Use `job_group_id` for duplicate, near-duplicate, or closely related job
  descriptions.

Splits must keep each `candidate_group_id` and `job_group_id` in only one split.

## Initial Milestones

Start with 100 reviewed pairs to validate the annotation process, label
definitions, reviewer agreement, and common edge cases.

After the process is stable, collect at least 1,000 diverse pairs for a credible
fine-tuning experiment.

## Future Evaluation Metrics

Future model comparisons should report:

- Keyword skill coverage
- Pearson correlation
- Spearman correlation
- Recall@1
- Recall@5
- nDCG@5

## Risks

Privacy risk: Resume text may contain direct and indirect personal identifiers.
Data must be anonymized before annotation, training, or evaluation.

Fairness risk: Labels may encode bias involving school names, employment gaps,
career changes, location, age, gender, disability, or nontraditional experience.
Reviewers must use only job-relevant evidence.

Dataset-bias risk: A narrow dataset may overrepresent specific roles,
industries, seniority levels, writing styles, or resume formats. The dataset
should include diverse job families and candidate backgrounds.

## Running the Baseline Benchmark

Run the deterministic benchmark against the included synthetic smoke-test
dataset:

```bash
make benchmark
```

The generated JSON report is written to:

```text
/tmp/careercraft-benchmark.json
```

To evaluate a populated labelled dataset with the optional semantic matcher:

```bash
cd backend

../.venv/bin/python -m app.benchmark \
  --dataset ../data/your-labelled-dataset.csv \
  --output /tmp/careercraft-benchmark.json \
  --include-semantic
```

The included `data/benchmark_sample.csv` contains synthetic, LLM-assisted
examples for verifying that the benchmark pipeline works. Its metrics must
not be presented as evidence of real model quality.

The current benchmark reports:

- Mean absolute error
- Pearson correlation
- Spearman correlation
- Per-pair deterministic and semantic scores

Ranking metrics such as Recall@1, Recall@5, and nDCG@5 are deferred until
the dataset contains multiple candidate resumes grouped under each job query.
