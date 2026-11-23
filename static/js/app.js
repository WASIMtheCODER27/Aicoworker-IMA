/**
 * AI CareerPilot - Modular Client Application Controller
 * Handles form validation, drag-and-drop resume ingestion, staged orchestration loading,
 * API communication, safe sanitized rendering, and dashboard interactions.
 */

(function () {
  'use strict';

  // State Management
  const state = {
    isSubmitting: false,
    selectedFile: null,
    analysisReport: null,
    stepperInterval: null
  };

  // DOM Selectors
  const dom = {
    form: document.getElementById('career-form'),
    submitBtn: document.getElementById('analyze-submit-btn'),
    fillSampleBtn: document.getElementById('fill-sample-btn'),
    quickStartBtn: document.getElementById('quick-start-btn'),
    quickTargetInput: document.getElementById('quick-target-input'),

    // Inputs
    nameInput: document.getElementById('input-name'),
    educationInput: document.getElementById('input-education'),
    degreeInput: document.getElementById('input-degree'),
    yearSelect: document.getElementById('input-year'),
    locationInput: document.getElementById('input-location'),
    goalsInput: document.getElementById('input-goals'),
    targetRoleInput: document.getElementById('input-target-role'),
    experienceSelect: document.getElementById('input-experience'),
    skillsInput: document.getElementById('input-skills'),
    hoursSlider: document.getElementById('input-hours-slider'),
    hoursDisplay: document.getElementById('hours-display'),
    hoursHidden: document.getElementById('input-hours'),
    interestsInput: document.getElementById('input-interests'),

    // File Upload
    dropZone: document.getElementById('resume-drop-zone'),
    fileInput: document.getElementById('resume-file-input'),
    dropZoneIdle: document.getElementById('drop-zone-idle'),
    fileChipWrap: document.getElementById('file-chip-wrap'),
    attachedFilename: document.getElementById('attached-filename'),
    attachedFilesize: document.getElementById('attached-filesize'),
    removeFileBtn: document.getElementById('remove-file-btn'),

    // Field Error Elements
    errEducation: document.getElementById('err-education'),
    errTargetRole: document.getElementById('err-target-role'),
    errSkills: document.getElementById('err-skills'),
    errFile: document.getElementById('err-file'),

    // Sections
    intakeSection: document.getElementById('intake-section'),
    loadingSection: document.getElementById('loading-section'),
    agentCurrentStatus: document.getElementById('agent-current-status'),
    stepper: document.getElementById('stepper'),
    globalErrorCard: document.getElementById('global-error-card'),
    errorMessageText: document.getElementById('error-message-text'),
    errorRetryBtn: document.getElementById('error-retry-btn'),
    errorContinueNoFileBtn: document.getElementById('error-continue-no-file-btn'),
    resultsSection: document.getElementById('results-section'),

    // Demo Banner
    demoBanner: document.getElementById('demo-banner'),
    closeBannerBtn: document.getElementById('close-banner'),
    fallbackCallout: document.getElementById('fallback-callout-card'),
    fallbackCalloutText: document.getElementById('fallback-callout-text'),

    // Dashboard Elements
    candidateName: document.getElementById('res-candidate-name'),
    roleChip: document.getElementById('res-target-role-chip'),
    expChip: document.getElementById('res-experience-chip'),
    modeChip: document.getElementById('res-engine-mode-chip'),
    readinessScoreText: document.getElementById('readiness-score-text'),
    readinessCircleProgress: document.getElementById('readiness-circle-progress'),
    readinessBadge: document.getElementById('readiness-level-badge'),
    readinessSummary: document.getElementById('res-readiness-summary'),
    domainVal: document.getElementById('res-domain-val'),
    commitmentVal: document.getElementById('res-commitment-val'),
    atsMetric: document.getElementById('res-ats-metric'),
    trajectoryText: document.getElementById('res-trajectory-text'),
    agentsTraceCloud: document.getElementById('res-agents-trace-cloud'),
    strengthsList: document.getElementById('res-strengths-list'),
    growthList: document.getElementById('res-growth-list'),
    atsBadge: document.getElementById('res-ats-badge'),
    atsRecsList: document.getElementById('res-ats-recs-list'),
    resumeWeakList: document.getElementById('res-resume-weak-list'),
    resumeMissingList: document.getElementById('res-resume-missing-list'),
    careerPathsGrid: document.getElementById('res-career-paths-grid'),
    skillGapTbody: document.getElementById('skill-gap-tbody'),
    competitiveAdv: document.getElementById('res-competitive-adv'),
    timelinePhases: document.getElementById('res-timeline-phases'),
    roadmapSummarySub: document.getElementById('roadmap-summary-sub'),
    projectsGrid: document.getElementById('res-projects-grid'),
    techQaList: document.getElementById('res-tech-qa-list'),
    behavioralQaList: document.getElementById('res-behavioral-qa-list'),
    practiceBox: document.getElementById('res-practice-box'),
    nextStepsChecklist: document.getElementById('res-next-steps-checklist'),

    // Actions
    btnExportJson: document.getElementById('btn-export-json'),
    btnPrintReport: document.getElementById('btn-print-report'),
    btnStartOver: document.getElementById('btn-start-over')
  };

  // Utilities: HTML Sanitization
  function escapeHTML(str) {
    if (typeof str !== 'string') return '';
    return str
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  function formatBytes(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
  }

  // Range Slider Handler
  if (dom.hoursSlider && dom.hoursDisplay && dom.hoursHidden) {
    dom.hoursSlider.addEventListener('input', (e) => {
      const val = parseFloat(e.target.value).toFixed(1);
      dom.hoursDisplay.innerText = `${val} hrs/day`;
      dom.hoursHidden.value = val;
    });
  }

  // Quick Start Prompt Bar
  if (dom.quickStartBtn && dom.quickTargetInput) {
    dom.quickStartBtn.addEventListener('click', () => {
      const targetVal = dom.quickTargetInput.value.trim();
      if (targetVal) {
        dom.targetRoleInput.value = targetVal;
      }
      dom.intakeSection.scrollIntoView({ behavior: 'smooth' });
      dom.targetRoleInput.focus();
    });

    dom.quickTargetInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        e.preventDefault();
        dom.quickStartBtn.click();
      }
    });
  }

  // Sample Data Preset
  if (dom.fillSampleBtn) {
    dom.fillSampleBtn.addEventListener('click', () => {
      dom.nameInput.value = 'Jordan Lee';
      dom.educationInput.value = "Bachelor's in Computer Science";
      dom.degreeInput.value = 'Software Engineering';
      dom.yearSelect.value = 'Final Year Student';
      dom.locationInput.value = 'Remote / New York, NY';
      dom.goalsInput.value = 'Aiming to secure a high-impact role building production microservices and scalable web applications in modern cloud architectures.';
      dom.targetRoleInput.value = 'Full-Stack Developer';
      dom.experienceSelect.value = 'Entry-level';
      dom.skillsInput.value = 'JavaScript, TypeScript, Python, React, Node.js, Express, PostgreSQL, Git, HTML5, CSS3';
      dom.hoursSlider.value = 3.0;
      dom.hoursDisplay.innerText = '3.0 hrs/day';
      dom.hoursHidden.value = '3.0';
      dom.interestsInput.value = 'Distributed Systems, Cloud Platforms, AI Agents, Microservices';

      clearErrors();
    });
  }

  // Banner Close
  if (dom.closeBannerBtn && dom.demoBanner) {
    dom.closeBannerBtn.addEventListener('click', () => {
      dom.demoBanner.classList.add('hidden');
    });
  }

  // Drag-and-Drop Resume Ingestion
  if (dom.dropZone && dom.fileInput) {
    ['dragenter', 'dragover'].forEach((eventName) => {
      dom.dropZone.addEventListener(eventName, (e) => {
        e.preventDefault();
        e.stopPropagation();
        dom.dropZone.classList.add('drag-over');
      });
    });

    ['dragleave', 'drop'].forEach((eventName) => {
      dom.dropZone.addEventListener(eventName, (e) => {
        e.preventDefault();
        e.stopPropagation();
        dom.dropZone.classList.remove('drag-over');
      });
    });

    dom.dropZone.addEventListener('drop', (e) => {
      const dt = e.dataTransfer;
      const files = dt.files;
      if (files && files.length > 0) {
        handleFileSelection(files[0]);
      }
    });

    dom.dropZone.addEventListener('click', (e) => {
      // Prevent recursion if clicking remove button
      if (e.target.closest('#remove-file-btn')) return;
      dom.fileInput.click();
    });

    dom.fileInput.addEventListener('change', (e) => {
      if (e.target.files && e.target.files.length > 0) {
        handleFileSelection(e.target.files[0]);
      }
    });

    if (dom.removeFileBtn) {
      dom.removeFileBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        clearFileSelection();
      });
    }
  }

  function handleFileSelection(file) {
    dom.errFile.innerText = '';
    const validExtensions = ['pdf', 'txt', 'md'];
    const ext = file.name.split('.').pop().toLowerCase();

    if (!validExtensions.includes(ext)) {
      dom.errFile.innerText = `Unsupported file type (.${ext}). Please upload a PDF, TXT, or MD resume.`;
      clearFileSelection();
      return;
    }

    if (file.size > 5 * 1024 * 1024) {
      dom.errFile.innerText = `File is too large (${formatBytes(file.size)}). Max allowed is 5MB.`;
      clearFileSelection();
      return;
    }

    state.selectedFile = file;
    dom.attachedFilename.innerText = file.name;
    dom.attachedFilesize.innerText = formatBytes(file.size);

    dom.dropZoneIdle.classList.add('hidden');
    dom.fileChipWrap.classList.remove('hidden');
  }

  function clearFileSelection() {
    state.selectedFile = null;
    dom.fileInput.value = '';
    dom.dropZoneIdle.classList.remove('hidden');
    dom.fileChipWrap.classList.add('hidden');
  }

  // Validation
  function clearErrors() {
    dom.errEducation.innerText = '';
    dom.errTargetRole.innerText = '';
    dom.errSkills.innerText = '';
    dom.errFile.innerText = '';
    dom.globalErrorCard.classList.add('hidden');
  }

  function validateForm() {
    clearErrors();
    let isValid = true;

    if (!dom.educationInput.value.trim()) {
      dom.errEducation.innerText = 'Education level is required.';
      isValid = false;
    }

    if (!dom.targetRoleInput.value.trim()) {
      dom.errTargetRole.innerText = 'Target career role is required.';
      isValid = false;
    }

    if (!dom.skillsInput.value.trim()) {
      dom.errSkills.innerText = 'At least one skill is required.';
      isValid = false;
    }

    return isValid;
  }

  // Staged Agent Stepper Animation
  const agentStages = [
    { step: 1, label: 'Profile Analysis Agent: Evaluating background & goals...' },
    { step: 2, label: 'Resume Analyzer Agent: Auditing ATS score & metrics...' },
    { step: 3, label: 'Career Path Agent: Benchmarking market trajectories...' },
    { step: 4, label: 'Skill Gap Agent: Calculating competency delta...' },
    { step: 5, label: 'Learning Roadmap Agent: Structuring weekly milestones...' },
    { step: 6, label: 'Interview Preparation Agent: Synthesizing coaching plan...' }
  ];

  function startStepperAnimation() {
    let currentStageIndex = 0;
    const steps = [1, 2, 3, 4, 5, 6].map(i => document.getElementById(`step-${i}`));

    // Reset steps
    steps.forEach(s => s && s.classList.remove('active', 'completed'));
    if (steps[0]) steps[0].classList.add('active');
    dom.agentCurrentStatus.innerText = agentStages[0].label;

    clearInterval(state.stepperInterval);
    state.stepperInterval = setInterval(() => {
      if (currentStageIndex < agentStages.length - 1) {
        if (steps[currentStageIndex]) {
          steps[currentStageIndex].classList.remove('active');
          steps[currentStageIndex].classList.add('completed');
        }
        currentStageIndex++;
        if (steps[currentStageIndex]) {
          steps[currentStageIndex].classList.add('active');
        }
        dom.agentCurrentStatus.innerText = agentStages[currentStageIndex].label;
      }
    }, 1800);
  }

  function stopStepperAnimation() {
    clearInterval(state.stepperInterval);
    const steps = [1, 2, 3, 4, 5, 6].map(i => document.getElementById(`step-${i}`));
    steps.forEach(s => s && s.classList.add('completed'));
  }

  // Form Submission
  if (dom.form) {
    dom.form.addEventListener('submit', async (e) => {
      e.preventDefault();

      if (state.isSubmitting) return;
      if (!validateForm()) {
        dom.intakeSection.scrollIntoView({ behavior: 'smooth' });
        return;
      }

      state.isSubmitting = true;
      dom.submitBtn.disabled = true;
      dom.submitBtn.querySelector('.btn-text').innerText = 'Analyzing with 6 Agents...';

      // UI Transition to Loading State
      dom.loadingSection.classList.remove('hidden');
      dom.resultsSection.classList.add('hidden');
      dom.globalErrorCard.classList.add('hidden');
      dom.loadingSection.scrollIntoView({ behavior: 'smooth' });
      startStepperAnimation();

      // Build Form Payload
      const formData = new FormData();
      formData.append('name', dom.nameInput.value.trim());
      formData.append('education', dom.educationInput.value.trim());
      formData.append('degree', dom.degreeInput.value.trim());
      formData.append('year_of_study', dom.yearSelect.value);
      formData.append('location', dom.locationInput.value.trim());
      formData.append('career_goals', dom.goalsInput.value.trim());
      formData.append('target_role', dom.targetRoleInput.value.trim());
      formData.append('experience_level', dom.experienceSelect.value);
      formData.append('current_skills', dom.skillsInput.value.trim());
      formData.append('hours_per_day', dom.hoursHidden.value);
      formData.append('interests', dom.interestsInput.value.trim());

      if (state.selectedFile) {
        formData.append('resume', state.selectedFile);
      }

      try {
        const response = await fetch('/api/analyze', {
          method: 'POST',
          body: formData
        });

        const result = await response.json();
        stopStepperAnimation();

        if (!response.ok || !result.success) {
          throw new Error(result.error || `Server responded with status ${response.status}`);
        }

        // Store Report & Render Dashboard
        state.analysisReport = result.report;
        renderDashboard(result.report);

        dom.loadingSection.classList.add('hidden');
        dom.resultsSection.classList.remove('hidden');
        dom.resultsSection.scrollIntoView({ behavior: 'smooth' });

      } catch (err) {
        stopStepperAnimation();
        dom.loadingSection.classList.add('hidden');
        const errMsg = err.message || 'An error occurred during analysis. Please check your inputs or retry.';
        dom.errorMessageText.innerText = errMsg;

        if (dom.errorContinueNoFileBtn) {
          if (errMsg.toLowerCase().includes('resume') || errMsg.toLowerCase().includes('pdf') || errMsg.toLowerCase().includes('ocr')) {
            dom.errorContinueNoFileBtn.classList.remove('hidden');
          } else {
            dom.errorContinueNoFileBtn.classList.add('hidden');
          }
        }

        dom.globalErrorCard.classList.remove('hidden');
        dom.globalErrorCard.scrollIntoView({ behavior: 'smooth' });
      } finally {
        state.isSubmitting = false;
        dom.submitBtn.disabled = false;
        dom.submitBtn.querySelector('.btn-text').innerText = 'Analyze My Career';
      }
    });
  }

  // Retry Button
  if (dom.errorRetryBtn) {
    dom.errorRetryBtn.addEventListener('click', () => {
      dom.globalErrorCard.classList.add('hidden');
      dom.intakeSection.scrollIntoView({ behavior: 'smooth' });
    });
  }

  // Continue Without Resume Button (One-click bypass when uploaded resume has OCR issues)
  if (dom.errorContinueNoFileBtn) {
    dom.errorContinueNoFileBtn.addEventListener('click', () => {
      dom.globalErrorCard.classList.add('hidden');
      dom.errorContinueNoFileBtn.classList.add('hidden');
      clearFileSelection();
      if (dom.form) {
        dom.form.dispatchEvent(new Event('submit', { cancelable: true }));
      }
    });
  }

  // ==========================================================================
  // Safe Dashboard Rendering Functions
  // ==========================================================================
  function renderDashboard(report) {
    if (!report) return;

    const candidate = report.candidate_summary || {};
    const profile = report.profile_analysis || {};
    const resume = report.resume_analysis || {};
    const paths = report.career_path_recommendations || [];
    const skillGap = report.skill_gap_analysis || {};
    const roadmap = report.learning_roadmap || {};
    const projects = report.suggested_projects || [];
    const interview = report.interview_preparation || {};
    const nextSteps = report.actionable_next_steps || [];
    const meta = report.orchestration_metadata || {};

    // 1. Candidate Header & Chips
    dom.candidateName.innerText = `${candidate.name || 'Candidate'}'s Career Intelligence`;
    dom.roleChip.innerText = candidate.target_role || 'Target Role';
    dom.expChip.innerText = candidate.experience_level || 'Level';
    dom.modeChip.innerText = meta.pipeline_mode || (report.is_fallback ? 'Demo Mode' : 'Live Multi-Agent');

    // 2. Fallback Callout
    if (report.is_fallback) {
      dom.fallbackCallout.classList.remove('hidden');
      dom.fallbackCalloutText.innerText = report.fallback_notice || 'Generated via heuristic synthesis because live AI is in demo mode.';
    } else {
      dom.fallbackCallout.classList.add('hidden');
    }

    // 3. Readiness Circular Gauge
    const score = Math.max(0, Math.min(100, candidate.overall_readiness_score || 70));
    dom.readinessScoreText.textContent = `${score}%`;
    dom.readinessCircleProgress.setAttribute('stroke-dasharray', `${score}, 100`);

    if (score >= 80) {
      dom.readinessBadge.innerText = 'High Market Readiness';
      dom.readinessBadge.className = 'badge badge-glow';
    } else if (score >= 60) {
      dom.readinessBadge.innerText = 'Moderate Alignment';
      dom.readinessBadge.className = 'badge badge-purple';
    } else {
      dom.readinessBadge.innerText = 'Foundational Stage';
      dom.readinessBadge.className = 'badge';
    }

    dom.readinessSummary.innerText = candidate.readiness_summary || 'Analysis complete.';
    dom.domainVal.innerText = candidate.domain_category || 'Technology';
    dom.commitmentVal.innerText = candidate.daily_learning_commitment || '2 hrs/day';
    dom.atsMetric.innerText = resume.has_resume ? `${resume.ats_compatibility_score || 75}/100` : 'No Resume';

    // 4. Trajectory & Agent Trace
    dom.trajectoryText.innerText = profile.career_trajectory || 'Gradual development toward specialized senior responsibilities.';
    dom.agentsTraceCloud.innerHTML = '';
    const agentsList = meta.agents_executed || [
      'Profile Agent', 'Resume Auditor', 'Career Pathing', 'Skill Gap Matrix', 'Roadmap Planner', 'Interview Coach'
    ];
    agentsList.forEach((agent) => {
      const tag = document.createElement('span');
      tag.className = 'trace-tag';
      tag.innerText = typeof agent === 'string' ? agent : (agent.name || 'Agent');
      dom.agentsTraceCloud.appendChild(tag);
    });

    // 5. Strengths & Growth Areas
    dom.strengthsList.innerHTML = '';
    (profile.key_strengths || []).forEach(item => {
      const li = document.createElement('li');
      li.innerText = item;
      dom.strengthsList.appendChild(li);
    });

    dom.growthList.innerHTML = '';
    (profile.growth_areas || []).forEach(item => {
      const li = document.createElement('li');
      li.innerText = item;
      dom.growthList.appendChild(li);
    });

    // 6. Resume Audit & ATS Health
    dom.atsBadge.innerText = resume.has_resume
      ? `ATS Score: ${resume.ats_compatibility_score || 70}/100`
      : 'Manual Profile Assessment';

    dom.atsRecsList.innerHTML = '';
    (resume.ats_recommendations || []).forEach(item => {
      const li = document.createElement('li');
      li.innerText = item;
      dom.atsRecsList.appendChild(li);
    });

    dom.resumeWeakList.innerHTML = '';
    (resume.weak_areas || []).forEach(item => {
      const li = document.createElement('li');
      li.innerText = item;
      dom.resumeWeakList.appendChild(li);
    });

    dom.resumeMissingList.innerHTML = '';
    (resume.missing_sections || []).forEach(item => {
      const li = document.createElement('li');
      li.innerText = item;
      dom.resumeMissingList.appendChild(li);
    });

    // 7. Recommended Career Paths
    dom.careerPathsGrid.innerHTML = '';
    paths.forEach(role => {
      const card = document.createElement('div');
      card.className = 'career-role-card';

      const reqPills = (role.entry_requirements || []).map(r =>
        `<span class="req-pill">${escapeHTML(r)}</span>`
      ).join('');

      card.innerHTML = `
        <div class="role-header">
          <h4 class="role-title">${escapeHTML(role.title || 'Role')}</h4>
          <span class="match-score-pill">${escapeHTML(String(role.match_score || 80))}% Match</span>
        </div>
        <div class="role-meta-row">
          <span class="meta-item">Demand: <strong>${escapeHTML(role.demand_level || 'High')}</strong></span>
          <span class="meta-item">Salary: <strong>${escapeHTML(role.salary_range || 'Competitive')}</strong></span>
        </div>
        <p class="role-reason">${escapeHTML(role.fit_reason || '')}</p>
        <div class="reqs-label">Core Entry Requirements:</div>
        <div class="reqs-tags">${reqPills}</div>
      `;
      dom.careerPathsGrid.appendChild(card);
    });

    // 8. Skill Gap Matrix Table
    dom.skillGapTbody.innerHTML = '';
    const missingSkills = skillGap.prioritized_missing_skills || [];
    missingSkills.forEach(skill => {
      const tr = document.createElement('tr');
      const priorityClass =
        (skill.priority || '').toLowerCase() === 'high' ? 'priority-high' :
        (skill.priority || '').toLowerCase() === 'medium' ? 'priority-medium' : 'priority-low';

      tr.innerHTML = `
        <td><strong>${escapeHTML(skill.skill || 'Skill')}</strong></td>
        <td><span class="text-muted">${escapeHTML(skill.category || 'General')}</span></td>
        <td><span class="priority-pill ${priorityClass}">${escapeHTML(skill.priority || 'Medium')}</span></td>
        <td><code>${escapeHTML(skill.time_to_learn || '2-4 weeks')}</code></td>
        <td class="text-muted">${escapeHTML(skill.importance || '')}</td>
      `;
      dom.skillGapTbody.appendChild(tr);
    });

    if (skillGap.competitive_advantage) {
      dom.competitiveAdv.innerHTML = `<strong>Strategic Market Advantage:</strong> ${escapeHTML(skillGap.competitive_advantage)}`;
    }

    // 9. Phased Learning Roadmap
    dom.timelinePhases.innerHTML = '';
    dom.roadmapSummarySub.innerText = `${roadmap.total_estimated_weeks || 10} weeks total (${roadmap.weekly_hours || 14} hrs/week)`;

    (roadmap.phases || []).forEach(phase => {
      const phaseCard = document.createElement('div');
      phaseCard.className = 'phase-card';

      const focusList = (phase.focus_areas || []).map(f => `<li>${escapeHTML(f)}</li>`).join('');

      phaseCard.innerHTML = `
        <div class="phase-header">
          <h4 class="phase-title">${escapeHTML(phase.phase_title || 'Phase')}</h4>
          <span class="phase-time-pill">${escapeHTML(phase.duration || '')}</span>
        </div>
        <ul class="bullet-list cyan-bullets">${focusList}</ul>
        <div class="milestone-badge">
          <span>🎯 Target Milestone:</span>
          <strong>${escapeHTML(phase.milestone || 'Project completion')}</strong>
        </div>
      `;
      dom.timelinePhases.appendChild(phaseCard);
    });

    // 10. Suggested Projects
    dom.projectsGrid.innerHTML = '';
    projects.forEach(proj => {
      const pCard = document.createElement('div');
      pCard.className = 'project-card';

      const techTags = (proj.tech_stack || []).map(t =>
        `<span class="req-pill">${escapeHTML(t)}</span>`
      ).join('');

      pCard.innerHTML = `
        <div class="project-header">
          <h4 class="project-title">${escapeHTML(proj.title || 'Portfolio Project')}</h4>
          <span class="project-difficulty">${escapeHTML(proj.difficulty || 'Intermediate')}</span>
        </div>
        <div class="reqs-tags mb-3">${techTags}</div>
        <p class="project-desc">${escapeHTML(proj.description || '')}</p>
        <div class="project-bullet-box">
          <span class="bullet-label">Resume Bullet Example:</span>
          <span>${escapeHTML(proj.resume_bullet || '')}</span>
        </div>
      `;
      dom.projectsGrid.appendChild(pCard);
    });

    // 11. Interview Preparation Coach
    renderInterviewSection(interview);

    // 12. Actionable Next Steps Checklist
    dom.nextStepsChecklist.innerHTML = '';
    nextSteps.forEach((step, idx) => {
      const item = document.createElement('div');
      item.className = 'check-item';
      item.innerHTML = `
        <input type="checkbox" id="check-step-${idx}" class="check-checkbox">
        <label for="check-step-${idx}" class="check-text">${escapeHTML(step)}</label>
      `;
      dom.nextStepsChecklist.appendChild(item);
    });
  }

  function renderInterviewSection(interview) {
    // Technical Questions
    dom.techQaList.innerHTML = '';
    (interview.technical_questions || []).forEach((q, idx) => {
      const qaCard = document.createElement('div');
      qaCard.className = 'qa-card';

      const points = (q.key_talking_points || []).map(p => `<li>${escapeHTML(p)}</li>`).join('');

      qaCard.innerHTML = `
        <div class="qa-header">
          <span class="qa-question">${idx + 1}. ${escapeHTML(q.question || '')}</span>
          <span class="qa-badge">${escapeHTML(q.focus_area || 'Technical')}</span>
        </div>
        <div class="qa-body">
          <div class="qa-guidance"><strong>Evaluation Guidance:</strong> ${escapeHTML(q.sample_guidance || '')}</div>
          <div class="talking-points-label">Key Points to Articulate:</div>
          <ul class="bullet-list cyan-bullets">${points}</ul>
        </div>
      `;
      dom.techQaList.appendChild(qaCard);
    });

    // Behavioral Questions
    dom.behavioralQaList.innerHTML = '';
    (interview.behavioral_questions || []).forEach((q, idx) => {
      const qaCard = document.createElement('div');
      qaCard.className = 'qa-card';

      const points = (q.key_talking_points || []).map(p => `<li>${escapeHTML(p)}</li>`).join('');

      qaCard.innerHTML = `
        <div class="qa-header">
          <span class="qa-question">${idx + 1}. ${escapeHTML(q.question || '')}</span>
          <span class="qa-badge">${escapeHTML(q.competency || 'STAR')}</span>
        </div>
        <div class="qa-body">
          <div class="qa-guidance"><strong>STAR Strategy:</strong> ${escapeHTML(q.sample_guidance || '')}</div>
          <div class="talking-points-label">Talking Points:</div>
          <ul class="bullet-list purple-bullets">${points}</ul>
        </div>
      `;
      dom.behavioralQaList.appendChild(qaCard);
    });

    // Practice Exercise
    dom.practiceBox.innerText = interview.practice_exercise || 'Design a microservice architecture and test for concurrency bottlenecks.';
  }

  // Interview Tabs Handler
  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));

      btn.classList.add('active');
      const targetTab = btn.getAttribute('data-tab');
      const pane = document.getElementById(targetTab);
      if (pane) pane.classList.add('active');
    });
  });

  // Export JSON Report
  if (dom.btnExportJson) {
    dom.btnExportJson.addEventListener('click', () => {
      if (!state.analysisReport) return;
      const dataStr = 'data:text/json;charset=utf-8,' + encodeURIComponent(JSON.stringify(state.analysisReport, null, 2));
      const downloadAnchor = document.createElement('a');
      downloadAnchor.setAttribute('href', dataStr);
      downloadAnchor.setAttribute('download', 'ai_careerpilot_report.json');
      document.body.appendChild(downloadAnchor);
      downloadAnchor.click();
      downloadAnchor.remove();
    });
  }

  // Print Report Handler
  if (dom.btnPrintReport) {
    dom.btnPrintReport.addEventListener('click', () => {
      window.print();
    });
  }

  // Start Over Button
  if (dom.btnStartOver) {
    dom.btnStartOver.addEventListener('click', () => {
      dom.resultsSection.classList.add('hidden');
      dom.intakeSection.scrollIntoView({ behavior: 'smooth' });
    });
  }

})();
