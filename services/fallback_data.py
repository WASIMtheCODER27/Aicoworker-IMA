"""Comprehensive offline fallback and demo data generator for AI CareerPilot."""
from typing import Dict, Any, List

def generate_fallback_career_data(profile: Dict[str, Any], has_resume: bool = False, resume_text: str = "") -> Dict[str, Any]:
    """
    Generate an intelligent, personalized career assessment fallback
    when Gemini API key is missing or quota/network fails.
    Clearly marks is_fallback: True.
    """
    target_role = profile.get("target_role", "Software Engineer")
    skills = profile.get("current_skills", ["Problem Solving", "Communication"])
    education = profile.get("education", "Computer Science")
    exp_level = profile.get("experience_level", "Entry-level")
    hours_per_day = profile.get("hours_per_day", 2.0)
    name = profile.get("name", "Aspiring Professional")

    # Generate tailored skill gaps based on target role
    target_lower = target_role.lower()
    
    if "data" in target_lower or "ai" in target_lower or "ml" in target_lower:
        matched_category = "AI & Data Science"
        rec_roles = [
            {
                "title": target_role,
                "match_score": 78,
                "demand_level": "Very High",
                "salary_range": "$95,000 - $140,000",
                "fit_reason": f"Strong alignment with your interest in {target_role} and existing foundation in {', '.join(skills[:2])}.",
                "entry_requirements": ["Proficiency in Python/R", "Statistical Modeling & ML algorithms", "Data visualization with Matplotlib/Seaborn", "SQL & Database querying"]
            },
            {
                "title": "Machine Learning Engineer",
                "match_score": 72,
                "demand_level": "High",
                "salary_range": "$110,000 - $160,000",
                "fit_reason": "Applies software engineering principles to productionize and deploy models at scale.",
                "entry_requirements": ["Model deployment (FastAPI/Docker)", "Deep learning frameworks (PyTorch/TensorFlow)", "CI/CD & MLOps pipelines"]
            },
            {
                "title": "Business Intelligence Analyst",
                "match_score": 84,
                "demand_level": "High",
                "salary_range": "$80,000 - $115,000",
                "fit_reason": "Great entry route to work directly with business stakeholders while sharpening analytical capabilities.",
                "entry_requirements": ["Advanced SQL & Tableau/PowerBI", "Data storytelling & dashboard design", "Business metrics KPI analysis"]
            }
        ]
        missing_skills = [
            {"skill": "MLOps & Docker Deployment", "priority": "High", "time_to_learn": "4-6 weeks", "category": "Deployment", "importance": "Crucial for packaging and deploying ML models to production environments."},
            {"skill": "Advanced Feature Engineering", "priority": "High", "time_to_learn": "3 weeks", "category": "Data Processing", "importance": "Transforms raw tables into predictive signals that boost model metrics."},
            {"skill": "PyTorch / Deep Learning", "priority": "Medium", "time_to_learn": "6-8 weeks", "category": "Algorithms", "importance": "Required for neural architectures, computer vision, and modern NLP."},
            {"skill": "Cloud Data Warehousing (BigQuery/Snowflake)", "priority": "Medium", "time_to_learn": "2-3 weeks", "category": "Cloud & DB", "importance": "Essential for enterprise scale querying and data pipelines."}
        ]
    elif "cloud" in target_lower or "devops" in target_lower or "sys" in target_lower:
        matched_category = "Cloud & DevOps"
        rec_roles = [
            {
                "title": target_role,
                "match_score": 80,
                "demand_level": "Extreme",
                "salary_range": "$105,000 - $155,000",
                "fit_reason": f"Matches your target path with immediate industry demand for infrastructure reliability.",
                "entry_requirements": ["Linux shell scripting & networking", "Infrastructure as Code (Terraform)", "Docker & Kubernetes cluster management", "AWS/GCP/Azure certification"]
            },
            {
                "title": "Site Reliability Engineer (SRE)",
                "match_score": 74,
                "demand_level": "High",
                "salary_range": "$115,000 - $165,000",
                "fit_reason": "Focuses on high availability, latency reduction, and automated incident recovery.",
                "entry_requirements": ["Observability (Prometheus, Grafana)", "Python/Go systems automation", "SLO/SLI engineering"]
            },
            {
                "title": "Cloud Solutions Architect",
                "match_score": 68,
                "demand_level": "High",
                "salary_range": "$130,000 - $180,000",
                "fit_reason": "Strategic architecture role for scaling multi-tenant cloud ecosystems.",
                "entry_requirements": ["Multi-region VPC design", "Zero-trust security policies", "Cost optimization frameworks"]
            }
        ]
        missing_skills = [
            {"skill": "Kubernetes Container Orchestration", "priority": "High", "time_to_learn": "5-6 weeks", "category": "Orchestration", "importance": "Standard deployment platform for containerized microservices."},
            {"skill": "Terraform (IaC)", "priority": "High", "time_to_learn": "3-4 weeks", "category": "Infrastructure", "importance": "Enables declarative, reproducible multi-cloud provisioning."},
            {"skill": "CI/CD Pipeline Automation (GitHub Actions)", "priority": "Medium", "time_to_learn": "2 weeks", "category": "DevOps", "importance": "Eliminates manual deployments and enforces security testing."},
            {"skill": "Linux Internals & eBPF Monitoring", "priority": "Medium", "time_to_learn": "4 weeks", "category": "Systems", "importance": "Deep diagnostics for network bottlenecks and memory leaks."}
        ]
    elif "security" in target_lower or "cyber" in target_lower:
        matched_category = "Cybersecurity"
        rec_roles = [
            {
                "title": target_role,
                "match_score": 76,
                "demand_level": "Extreme",
                "salary_range": "$95,000 - $145,000",
                "fit_reason": f"Directly targets critical defensive and security analysis competencies.",
                "entry_requirements": ["Network traffic inspection (Wireshark)", "SIEM log analysis (Splunk/ELK)", "Vulnerability assessment (Nessus)", "CompTIA Security+ or CEH"]
            },
            {
                "title": "Application Security Engineer",
                "match_score": 70,
                "demand_level": "High",
                "salary_range": "$110,000 - $160,000",
                "fit_reason": "Bridges software engineering and offensive testing for web applications.",
                "entry_requirements": ["OWASP Top 10 mitigation", "SAST/DAST tooling in CI/CD", "Secure code review"]
            },
            {
                "title": "SOC Analyst (Level 2)",
                "match_score": 82,
                "demand_level": "High",
                "salary_range": "$75,000 - $105,000",
                "fit_reason": "Great launchpad to triage live alerts and investigate intrusions.",
                "entry_requirements": ["Incident response protocols", "Threat intelligence feeds", "Endpoint detection (EDR)"]
            }
        ]
        missing_skills = [
            {"skill": "OWASP Top 10 & API Security", "priority": "High", "time_to_learn": "3-4 weeks", "category": "AppSec", "importance": "Prevents unauthorized data exfiltration and injection exploits."},
            {"skill": "SIEM Configuration & Querying", "priority": "High", "time_to_learn": "4 weeks", "category": "Blue Team", "importance": "Identifies anomalies and correlates threat indicators in real-time."},
            {"skill": "Linux Network Forensics", "priority": "Medium", "time_to_learn": "3 weeks", "category": "Forensics", "importance": "Investigates compromised hosts and reconstructs attack chains."}
        ]
    else:
        # Software Engineering / Full Stack default
        matched_category = "Full-Stack Software Engineering"
        rec_roles = [
            {
                "title": target_role,
                "match_score": 82,
                "demand_level": "High",
                "salary_range": "$85,000 - $130,000",
                "fit_reason": f"Leverages your background in {education} and proficiency with {', '.join(skills[:3])}.",
                "entry_requirements": ["Solid frontend and backend architecture", "RESTful & GraphQL API design", "Relational database modeling (PostgreSQL)", "Unit & integration testing"]
            },
            {
                "title": "Backend Systems Engineer",
                "match_score": 75,
                "demand_level": "High",
                "salary_range": "$95,000 - $145,000",
                "fit_reason": "Focuses on high-throughput services, distributed caching, and data pipelines.",
                "entry_requirements": ["Concurrent programming", "Redis caching & message queues (Kafka/RabbitMQ)", "Microservices design patterns"]
            },
            {
                "title": "Frontend / Full-Stack UI Specialist",
                "match_score": 79,
                "demand_level": "Moderate to High",
                "salary_range": "$85,000 - $125,000",
                "fit_reason": "Ideal if you enjoy building intuitive, reactive client-side experiences and design systems.",
                "entry_requirements": ["TypeScript & modern SPA frameworks", "State management & WebSockets", "Web accessibility (WCAG) & performance audits"]
            }
        ]
        missing_skills = [
            {"skill": "System Design & Architecture", "priority": "High", "time_to_learn": "4-6 weeks", "category": "Architecture", "importance": "Crucial for scaling services, handling concurrency, and passing senior technical loops."},
            {"skill": "Docker & Containerized Microservices", "priority": "High", "time_to_learn": "2-3 weeks", "category": "DevOps", "importance": "Guarantees reproducible runtime environments across staging and cloud production."},
            {"skill": "Automated Testing & CI/CD", "priority": "Medium", "time_to_learn": "2 weeks", "category": "Quality", "importance": "Prevents regressions and automates linting, testing, and deployment workflows."},
            {"skill": "Distributed Caching (Redis/Memcached)", "priority": "Medium", "time_to_learn": "2 weeks", "category": "Performance", "importance": "Drastically reduces database latency under high traffic loads."}
        ]

    # Calculate realistic readiness score
    readiness_score = 74 if has_resume else 68

    return {
        "is_fallback": True,
        "fallback_notice": "DEMO MODE: Generated via intelligent heuristic fallback. To enable live multi-agent Google Gemini analysis, configure your GEMINI_API_KEY in the .env file.",
        "candidate_summary": {
            "name": name,
            "target_role": target_role,
            "domain_category": matched_category,
            "experience_level": exp_level,
            "education": education,
            "daily_learning_commitment": f"{hours_per_day} hours/day",
            "overall_readiness_score": readiness_score,
            "readiness_summary": f"{name} demonstrates an encouraging foundation in {', '.join(skills[:3])}. With structured focus on high-priority gaps over the next 8-12 weeks, you will be strongly positioned for competitive {target_role} positions."
        },
        "profile_analysis": {
            "key_strengths": [
                f"Strong academic / practical orientation in {education}.",
                f"Demonstrated command of core tools: {', '.join(skills)}.",
                f"Proactive career intent focused on {target_role}.",
                f"Consistent daily commitment of {hours_per_day} hours dedicated to technical upskilling."
            ],
            "growth_areas": [
                "Translating individual code scripts into production-tested, deployable web services.",
                "Quantifying project metrics and business impact in portfolios and interviews.",
                "Deepening architectural knowledge regarding system scalability and fault tolerance."
            ],
            "career_trajectory": f"Gradual evolution from {exp_level} to specialized {target_role} with strong potential for autonomous ownership within 12 months."
        },
        "resume_analysis": {
            "has_resume": has_resume,
            "ats_compatibility_score": 78 if has_resume else 0,
            "strengths": [
                "Clear technical skills taxonomy and educational background.",
                "Logical chronological layout and clean contact formatting."
            ] if has_resume else ["Profile inputs provided directly via platform form."],
            "weak_areas": [
                "Bullet points emphasize responsibilities rather than measurable business metrics (e.g. latency reduced by 30%).",
                "Action verbs could be more assertive (prefer 'Architected', 'Spearheaded', 'Optimized' over 'Helped with')."
            ] if has_resume else ["Upload a PDF or TXT resume to receive granular ATS and section-by-section audit."],
            "missing_sections": [
                "Key Performance Indicators (KPIs) or measurable impact metrics.",
                "Direct links to deployed live URLs or GitHub repositories.",
                "Targeted professional summary tailored to the target role."
            ] if has_resume else ["Complete formal resume upload recommended for comprehensive ATS parsing."],
            "ats_recommendations": [
                "Use standard section headers: 'Work Experience', 'Technical Skills', 'Education', 'Projects'.",
                "Avoid complex multi-column tables, text boxes, or embedded images that disrupt parser reading order.",
                "Incorporate exact keywords from target job listings directly into your project descriptions."
            ]
        },
        "career_path_recommendations": rec_roles,
        "skill_gap_analysis": {
            "current_strengths": skills,
            "prioritized_missing_skills": missing_skills,
            "competitive_advantage": f"Combining {skills[0] if skills else 'fundamentals'} with modern deployment best practices will elevate you above typical applicant pools."
        },
        "learning_roadmap": {
            "total_estimated_weeks": 10,
            "weekly_hours": round(hours_per_day * 7, 1),
            "phases": [
                {
                    "phase_title": "Phase 1: Deepening Core Technical Fundamentals",
                    "duration": "Weeks 1 - 3",
                    "weekly_hours": round(hours_per_day * 7, 1),
                    "focus_areas": [
                        "Master advanced patterns in your primary programming language.",
                        "Solve 20 medium data structures & algorithms problems (graphs, trees, two pointers).",
                        "Design clean modular APIs adhering to REST conventions."
                    ],
                    "milestone": "Build and document a robust RESTful API with automated unit testing."
                },
                {
                    "phase_title": "Phase 2: Architectural Gaps & Containerization",
                    "duration": "Weeks 4 - 6",
                    "weekly_hours": round(hours_per_day * 7, 1),
                    "focus_areas": [
                        f"Implement {missing_skills[0]['skill']}.",
                        "Configure Dockerfiles and multi-stage builds for minimal container image sizes.",
                        "Integrate persistent storage and relational database schemas with indexing."
                    ],
                    "milestone": "Deploy a containerized microservice to a cloud platform (Render, Fly.io, or AWS ECS)."
                },
                {
                    "phase_title": "Phase 3: Production Hardening & CI/CD",
                    "duration": "Weeks 7 - 8",
                    "weekly_hours": round(hours_per_day * 7, 1),
                    "focus_areas": [
                        "Automate testing and deployment pipelines using GitHub Actions.",
                        "Implement Redis caching, rate limiting, and structured logging.",
                        "Conduct load testing and optimize database query plans."
                    ],
                    "milestone": "Full CI/CD pipeline triggering automated testing and zero-downtime deployment."
                },
                {
                    "phase_title": "Phase 4: Capstone Showcase & Interview Sprints",
                    "duration": "Weeks 9 - 10",
                    "weekly_hours": round(hours_per_day * 7, 1),
                    "focus_areas": [
                        "Polish capstone portfolio project with live interactive demo and comprehensive README.",
                        "Conduct mock behavioral interviews using the STAR method.",
                        "Network with engineers and hiring managers on LinkedIn."
                    ],
                    "milestone": "Publish production capstone with live URL, demo video, and interactive metrics."
                }
            ]
        },
        "suggested_projects": [
            {
                "title": f"Production-Grade {target_role} Capstone Service",
                "difficulty": "Intermediate to Advanced",
                "tech_stack": [skills[0] if skills else "Python", "FastAPI / Flask", "PostgreSQL", "Docker", "GitHub Actions"],
                "description": f"An end-to-end cloud platform solving a real-world data or workflow challenge, featuring JWT authentication, automated CI/CD pipelines, and responsive frontend.",
                "resume_bullet": f"Architected a scalable {target_role} service with automated CI/CD and sub-80ms response times for concurrent requests."
            },
            {
                "title": "Real-Time Telemetry & Analytics Dashboard",
                "difficulty": "Intermediate",
                "tech_stack": ["WebSocket", "Redis", "TypeScript / Vanilla JS", "Chart.js"],
                "description": "Live event-streaming dashboard tracking asynchronous system events, latency metrics, and error rates with instant alerting.",
                "resume_bullet": "Developed a real-time event analytics dashboard processing 1,000+ simulated events/sec using WebSockets and Redis Pub/Sub."
            }
        ],
        "interview_preparation": {
            "technical_questions": [
                {
                    "question": f"Explain the architectural trade-offs you consider when designing a service for {target_role}.",
                    "focus_area": "System Architecture & Design",
                    "sample_guidance": "Discuss latency vs. throughput, synchronous HTTP vs. asynchronous queues, caching strategies, and data consistency models.",
                    "key_talking_points": ["Monolith vs. Microservices", "Database normalization vs. denormalization", "Idempotency in API endpoints"]
                },
                {
                    "question": "How do you detect, isolate, and debug a performance bottleneck in a live production environment?",
                    "focus_area": "Troubleshooting & Observability",
                    "sample_guidance": "Outline a systematic methodology: examine APM metrics, inspect slow database query logs, analyze thread dumps, and reproduce in staging.",
                    "key_talking_points": ["Application Performance Monitoring (APM)", "Database EXPLAIN ANALYZE", "Memory leak profiling"]
                },
                {
                    "question": f"How do you ensure data integrity and security when handling external inputs in {skills[0] if skills else 'your application'}?",
                    "focus_area": "Security & Validation",
                    "sample_guidance": "Emphasize zero-trust input validation, parameterized queries to avoid SQL injection, sanitization against XSS, and proper auth middleware.",
                    "key_talking_points": ["Schema validation", "SQL parameterization", "Least privilege principle"]
                }
            ],
            "behavioral_questions": [
                {
                    "question": "Describe a scenario where you had to quickly learn an unfamiliar technology or framework to deliver a project.",
                    "competency": "Agility & Continuous Learning",
                    "sample_guidance": "Use the STAR method (Situation, Task, Action, Result). Highlight your strategy for breaking down documentation, building a prototype, and delivering on schedule.",
                    "key_talking_points": ["Systematic learning approach", "Rapid prototyping", "Successful delivery under deadlines"]
                },
                {
                    "question": "Tell me about a time you encountered a difficult technical disagreement with a teammate. How did you resolve it?",
                    "competency": "Collaboration & Conflict Resolution",
                    "sample_guidance": "Focus on data-driven decision making, separating egos from architectural decisions, creating benchmark tests, and aligning with business goals.",
                    "key_talking_points": ["Objective benchmarks", "Active listening", "Team consensus"]
                }
            ],
            "practice_exercise": f"Spend 45 minutes designing a mock architecture for a URL shortener or real-time notification service tailored for {target_role}. Document your API endpoints, database schema, and caching tier."
        },
        "actionable_next_steps": [
            "Review your prioritized skill gaps and schedule dedicated calendar blocks for Phase 1.",
            "Refactor your primary portfolio project to include unit tests and a Dockerfile.",
            "Update your resume bullet points using the Action-Verb + Context + Measurable Result formula.",
            "Set up a GitHub Actions workflow to verify build and test passes on every commit.",
            "Connect with 5 professionals currently working as " + target_role + " on LinkedIn for informational chats."
        ]
    }
