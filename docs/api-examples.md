# API Examples

Start the application before running these examples:

```bash
make run
```

The default local address is `http://127.0.0.1:8000`.

## Health check

```bash
curl --fail http://127.0.0.1:8000/api/health
```

## Parse a resume

```bash
curl --fail \
  -X POST \
  -F "file=@resume.pdf" \
  http://127.0.0.1:8000/api/resume/parse
```

Supported formats are PDF, DOCX, and UTF-8 TXT. The upload limit is 5 MB.

## Analyze resume alignment

```bash
curl --fail \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "resume_text": "Skills\nPython, FastAPI and Docker\nProjects\nBuilt and tested a production API service.\nEducation\nB.Tech Computer Science.",
    "job_description": "Seeking a Python backend engineer with FastAPI, Docker, AWS and automated testing experience.",
    "include_semantic": false
  }' \
  http://127.0.0.1:8000/api/analyze
```

Set `include_semantic` to `true` only when the optional machine-learning
requirements are installed.

## Interactive documentation

Open `http://127.0.0.1:8000/docs` to inspect schemas and execute requests from
the browser.
