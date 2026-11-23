"""AI CareerPilot - Flask Application Server."""
import json
import logging
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from flask import Flask, request, jsonify, render_template
from werkzeug.exceptions import RequestEntityTooLarge

from config import Config
from services.validator import validate_profile_input, validate_uploaded_file
from services.file_extractor import extract_resume_text
from services.gemini_service import GeminiService
from agents.orchestrator import CareerOrchestrator

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("CareerPilot")

def create_app(config_class=Config) -> Flask:
    """Application factory for AI CareerPilot."""
    base_dir = Path(__file__).resolve().parent
    app = Flask(
        __name__,
        template_folder=str(base_dir / "templates"),
        static_folder=str(base_dir / "static")
    )
    app.config.from_object(config_class)

    # Ensure upload directory exists if needed
    try:
        os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    except OSError:
        pass

    # Initialize Services & Orchestrator
    gemini_service = GeminiService(
        api_key=app.config.get("GEMINI_API_KEY"),
        model=app.config.get("GEMINI_MODEL")
    )
    orchestrator = CareerOrchestrator(gemini_service=gemini_service)

    start_time = datetime.now(timezone.utc)

    # ------------------ ROUTES ------------------

    @app.route("/")
    def index():
        """Serve main frontend interface."""
        return render_template(
            "index.html",
            is_ai_live=gemini_service.is_configured(),
            model_name=gemini_service.model
        )

    @app.route("/api/health", methods=["GET"])
    def health_check():
        """Health check endpoint providing system status and service readiness."""
        uptime_seconds = (datetime.now(timezone.utc) - start_time).total_seconds()
        is_live = gemini_service.is_configured()

        return jsonify({
            "status": "healthy",
            "service": "AI CareerPilot",
            "version": "1.0.0",
            "uptime_seconds": round(uptime_seconds, 1),
            "ai_integration": {
                "provider": "Google AI (Gemma/Gemini)",
                "model": gemini_service.model,
                "api_key_configured": is_live,
                "mode": "Live Multi-Agent AI" if is_live else "Intelligent Demo / Fallback Mode"
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }), 200

    @app.route("/api/analyze", methods=["POST"])
    def analyze():
        """
        Analyze user career profile and resume.
        Accepts multipart/form-data or application/json.
        """
        raw_file = None
        data = {}

        if request.content_type and "multipart/form-data" in request.content_type:
            # Handle Form Data
            if "resume" in request.files:
                raw_file = request.files["resume"]

            # Collect form fields
            form_dict = request.form.to_dict()
            # If payload was sent as json string inside formData
            if "payload" in form_dict:
                try:
                    data = json.loads(form_dict["payload"])
                except Exception:
                    data = form_dict
            else:
                data = form_dict

                # Parse skills if passed as comma separated or string list
                if "current_skills" in data and isinstance(data["current_skills"], str):
                    skills_val = data["current_skills"].strip()
                    if skills_val.startswith("[") and skills_val.endswith("]"):
                        try:
                            data["current_skills"] = json.loads(skills_val)
                        except Exception:
                            data["current_skills"] = [s.strip() for s in skills_val.strip("[]").replace('"', '').split(",") if s.strip()]
                    else:
                        data["current_skills"] = [s.strip() for s in skills_val.split(",") if s.strip()]

        elif request.is_json:
            data = request.get_json() or {}
        else:
            return jsonify({
                "success": False,
                "error": "Unsupported Content-Type. Please send multipart/form-data or application/json."
            }), 400

        # Validate Profile Inputs
        is_valid, val_err, sanitized_profile = validate_profile_input(data)
        if not is_valid:
            logger.warning(f"Validation failed: {val_err}")
            return jsonify({
                "success": False,
                "error": val_err
            }), 400

        # Validate Uploaded File
        has_file = raw_file is not None and raw_file.filename != ""
        if has_file:
            file_valid, file_err, ext = validate_uploaded_file(raw_file)
            if not file_valid:
                logger.warning(f"File validation failed: {file_err}")
                return jsonify({
                    "success": False,
                    "error": file_err
                }), 400

        # Extract Text from Resume
        resume_text = ""
        if has_file:
            extract_success, extract_err, resume_text = extract_resume_text(raw_file, gemini_service=gemini_service)
            if not extract_success:
                logger.warning(f"Resume text extraction failed: {extract_err}")
                return jsonify({
                    "success": False,
                    "error": f"Resume processing error: {extract_err}"
                }), 422

        # Run Multi-Agent Orchestrator
        try:
            logger.info(f"Starting career analysis for target role '{sanitized_profile['target_role']}' (Resume attached: {bool(resume_text)})")
            report = orchestrator.analyze_career(
                profile=sanitized_profile,
                resume_text=resume_text,
                has_resume=bool(resume_text)
            )

            return jsonify({
                "success": True,
                "report": report
            }), 200

        except Exception as e:
            logger.error(f"Career analysis pipeline exception: {str(e)}", exc_info=True)
            return jsonify({
                "success": False,
                "error": "An internal error occurred while executing the AI career analysis pipeline. Please try again."
            }), 500

    # ------------------ ERROR HANDLERS ------------------

    @app.errorhandler(RequestEntityTooLarge)
    def handle_file_too_large(e):
        """Handle request exceeding MAX_CONTENT_LENGTH."""
        max_mb = Config.MAX_CONTENT_LENGTH / (1024 * 1024)
        return jsonify({
            "success": False,
            "error": f"Uploaded file is too large. Maximum allowed upload size is {max_mb:.0f} MB."
        }), 413

    @app.errorhandler(404)
    def handle_not_found(e):
        if request.path.startswith("/api/"):
            return jsonify({"success": False, "error": "Endpoint not found."}), 404
        return render_template("index.html", is_ai_live=gemini_service.is_configured(), model_name=gemini_service.model), 404

    @app.errorhandler(500)
    def handle_server_error(e):
        return jsonify({
            "success": False,
            "error": "An unexpected server error occurred."
        }), 500

    return app

app = create_app()

if __name__ == "__main__":
    port = Config.PORT
    host = Config.HOST
    logger.info(f"Starting AI CareerPilot on http://{host}:{port}")
    app.run(host=host, port=port, debug=Config.DEBUG)
