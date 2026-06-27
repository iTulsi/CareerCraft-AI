const fileInput = document.querySelector("#resume-file");
const fileName = document.querySelector("#file-name");
const parseButton = document.querySelector("#parse-button");
const analyzeButton = document.querySelector("#analyze-button");
const resumeText = document.querySelector("#resume-text");
const jobDescription = document.querySelector("#job-description");
const statusMessage = document.querySelector("#status");
const results = document.querySelector("#results");
const matchScore = document.querySelector("#match-score");
const scoreBar = document.querySelector("#score-bar");
const matchedSkills = document.querySelector("#matched-skills");
const missingSkills = document.querySelector("#missing-skills");
const methodology = document.querySelector("#methodology");

fileInput.addEventListener("change", () => {
  const file = fileInput.files[0];
  fileName.textContent = file ? file.name : "No file selected";
  results.hidden = true;
  setStatus("");
});

parseButton.addEventListener("click", parseResume);
analyzeButton.addEventListener("click", analyzeResume);

async function parseResume() {
  const file = fileInput.files[0];

  if (!file) {
    setStatus("Choose a resume file first.", true);
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  setBusy(parseButton, true, "Extracting...");
  setStatus("Reading resume...");

  try {
    const response = await fetch("/api/resume/parse", {
      method: "POST",
      body: formData,
    });
    const payload = await readJson(response);

    if (!response.ok) {
      throw new Error(payload.detail || "Resume parsing failed.");
    }

    resumeText.value = payload.text;
    setStatus(
      `Extracted ${payload.word_count} words from ${payload.filename}.`
    );
  } catch (error) {
    setStatus(error.message, true);
  } finally {
    setBusy(parseButton, false, "Extract resume text");
  }
}

async function analyzeResume() {
  const resume = resumeText.value.trim();
  const job = jobDescription.value.trim();

  if (resume.length < 30) {
    setStatus("Resume text must contain at least 30 characters.", true);
    return;
  }

  if (job.length < 30) {
    setStatus("Job description must contain at least 30 characters.", true);
    return;
  }

  setBusy(analyzeButton, true, "Analyzing...");
  setStatus("Comparing resume skills with the job requirements...");
  results.hidden = true;

  try {
    const response = await fetch("/api/analyze", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        resume_text: resume,
        job_description: job,
      }),
    });
    const payload = await readJson(response);

    if (!response.ok) {
      throw new Error(formatApiError(payload));
    }

    renderResults(payload);
    setStatus("Analysis complete.");
  } catch (error) {
    setStatus(error.message, true);
  } finally {
    setBusy(analyzeButton, false, "Analyze match");
  }
}

function renderResults(payload) {
  const score = payload.result.match_score;
  matchScore.textContent = `${score}%`;
  scoreBar.style.width = `${Math.min(Math.max(score, 0), 100)}%`;
  renderTags(matchedSkills, payload.result.matched_skills, "No matched skills");
  renderTags(missingSkills, payload.result.missing_skills, "No missing skills");
  methodology.textContent = payload.methodology;
  results.hidden = false;
  results.scrollIntoView({behavior: "smooth", block: "start"});
}

function renderTags(container, skills, emptyMessage) {
  container.replaceChildren();

  if (skills.length === 0) {
    const message = document.createElement("p");
    message.className = "empty-state";
    message.textContent = emptyMessage;
    container.append(message);
    return;
  }

  for (const skill of skills) {
    const tag = document.createElement("span");
    tag.textContent = skill;
    container.append(tag);
  }
}

function setBusy(button, isBusy, label) {
  button.disabled = isBusy;
  button.textContent = label;
}

function setStatus(message, isError = false) {
  statusMessage.textContent = message;
  statusMessage.classList.toggle("error", isError);
}

async function readJson(response) {
  try {
    return await response.json();
  } catch {
    return {};
  }
}

function formatApiError(payload) {
  if (typeof payload.detail === "string") {
    return payload.detail;
  }

  return "The analysis request could not be completed.";
}
