const fileInput = document.querySelector("#resume-file");
const fileName = document.querySelector("#file-name");
const parseButton = document.querySelector("#parse-button");
const analyzeButton = document.querySelector("#analyze-button");
const resumeText = document.querySelector("#resume-text");
const jobDescription = document.querySelector("#job-description");
const statusMessage = document.querySelector("#status");
const results = document.querySelector("#results");
const matchScore = document.querySelector("#match-score");
const skillScore = document.querySelector("#skill-score");
const structureScore = document.querySelector("#structure-score");
const semanticScore = document.querySelector("#semantic-score");
const semanticStatus = document.querySelector("#semantic-status");
const scoreBar = document.querySelector("#score-bar");
const matchedSkills = document.querySelector("#matched-skills");
const missingSkills = document.querySelector("#missing-skills");
const foundSections = document.querySelector("#found-sections");
const missingSections = document.querySelector("#missing-sections");
const recommendations = document.querySelector("#recommendations");
const interviewQuestions = document.querySelector("#interview-questions");
const methodology = document.querySelector("#methodology");
const downloadReportButton = document.querySelector(
  "#download-report-button"
);

let latestAnalysis = null;

fileInput.addEventListener("change", () => {
  const file = fileInput.files[0];
  fileName.textContent = file ? file.name : "No file selected";
  latestAnalysis = null;
  results.hidden = true;
  setStatus("");
});

parseButton.addEventListener("click", parseResume);
analyzeButton.addEventListener("click", analyzeResume);
downloadReportButton.addEventListener("click", downloadAnalysisReport);

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
        include_semantic: true,
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
  latestAnalysis = payload;
  const score = payload.assessment.overall_score;
  matchScore.textContent = `${score}%`;
  skillScore.textContent = `${payload.assessment.skill_score}%`;
  structureScore.textContent = `${payload.assessment.structure_score}%`;
  renderSemanticMatch(payload.semantic);
  scoreBar.style.width = `${Math.min(Math.max(score, 0), 100)}%`;
  renderTags(matchedSkills, payload.result.matched_skills, "No matched skills");
  renderTags(missingSkills, payload.result.missing_skills, "No missing skills");
  renderTags(
    foundSections,
    payload.assessment.found_sections,
    "No standard sections detected"
  );
  renderTags(
    missingSections,
    payload.assessment.missing_sections,
    "No standard sections missing"
  );
  renderRecommendations(payload.assessment.recommendations);
  renderInterviewQuestions(payload.interview_questions);
  methodology.textContent = payload.methodology;
  results.hidden = false;
  results.scrollIntoView({behavior: "smooth", block: "start"});
}

function renderSemanticMatch(semantic) {
  semanticScore.textContent =
    semantic.status === "available" ? `${semantic.score}%` : "—";
  semanticStatus.textContent = semantic.note;
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

function renderRecommendations(items) {
  recommendations.replaceChildren();

  for (const item of items) {
    const listItem = document.createElement("li");
    listItem.textContent = item;
    recommendations.append(listItem);
  }
}

function downloadAnalysisReport(event) {
  event.preventDefault();

  if (!latestAnalysis) {
    setStatus("Run an analysis before downloading a report.", true);
    return;
  }

  const form = document.createElement("form");
  const payloadInput = document.createElement("input");

  form.method = "POST";
  form.action = "/api/report";
  form.hidden = true;

  payloadInput.type = "hidden";
  payloadInput.name = "payload";
  payloadInput.value = JSON.stringify(latestAnalysis);

  form.append(payloadInput);
  document.body.append(form);
  form.submit();
  form.remove();

  setStatus("Analysis report download started.");
}

function renderInterviewQuestions(items) {
  interviewQuestions.replaceChildren();

  for (const item of items) {
    const details = document.createElement("details");
    details.className = "interview-question";

    const summary = document.createElement("summary");
    const category = document.createElement("span");
    const question = document.createElement("span");
    const answer = document.createElement("p");

    category.className = "interview-category";
    category.textContent = item.category.replace("_", " ");
    question.textContent = item.question;
    answer.textContent = `Answer outline: ${item.answer_outline}`;

    summary.append(category, question);
    details.append(summary, answer);
    interviewQuestions.append(details);
  }
}

function formatInterviewQuestions(items) {
  return items
    .map(
      (item, index) =>
        `${index + 1}. [${item.category.replace("_", " ")}] ` +
        `${item.question}\n   Answer outline: ${item.answer_outline}`
    )
    .join("\n");
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
