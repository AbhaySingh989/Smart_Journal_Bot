# EPIC: OCI Modernization & Advanced Features

## Description
This EPIC focuses on transforming the existing Smart Journal Bot into a production-ready, efficiently containerized application on Oracle Cloud Infrastructure (OCI). It includes a strategic upgrade to the Gemini 2.5 Flash model for optimal performance/cost balance and the implementation of advanced user-centric features like Analytics and Goal Tracking.

## User Stories

### Story 1: Project Cleanup & Organization
**Status:** Completed
**Date:** 2026-01-05
**As a** Developer,
**I want** to organize the project file structure by moving documentation and scripts to dedicated folders,
**So that** the project root is clean, maintainable, and easy to navigate.

**Acceptance Criteria:**
- [ ] `docs/` folder created.
- [ ] `Plan.md`, `Product_Architecture.md`, `Gemini.md`, `GEMINI_MODELS_AND_LIMITS.md`, `LICENSE`, `README.md` moved to `docs/`.
- [ ] `scripts/` folder created.
- [ ] `migrate.py` moved to `scripts/`.
- [ ] `requirements-dev.txt` is removed, and necessary dev dependencies are merged into the main `requirements.txt` or a dedicated test setup.
- [ ] The application still runs correctly after file moves (imports checked).

### Story 2: OCI Docker Containerization
**Status:** Completed
**Date:** 2026-01-05
**As a** DevOps Engineer,
**I want** to containerize the bot using Docker and Docker Compose,
**So that** I can easily deploy and manage the application on an OCI instance with consistent environments.

**Acceptance Criteria:**
- [ ] `Dockerfile` created using a multi-stage build (Python 3.11-slim) to minimize image size.
- [ ] `graphviz` system dependency installed in the Docker image.
- [ ] `docker-compose.yml` created defining the `bot` service.
- [ ] `docker-compose.yml` configures a named volume or bind mount for `bot_data/` to ensure database persistence.
- [ ] Environment variables (`TELEGRAM_BOT_TOKEN`, `GEMINI_API_KEY`, etc.) are correctly injected into the container.
- [ ] `.dockerignore` file created to exclude `venv`, `.git`, and temp files.

### Story 3: Gemini Model Upgrade & Rate Limiting
**Status:** Completed
**Date:** 2026-01-05
**As a** Product Owner,
**I want** the bot to use the `gemini-2.5-flash` model and handle rate limits gracefully,
**So that** users get fast responses within the free tier limits (15 RPM / 1500 RPD) without the bot crashing.

**Acceptance Criteria:**
- [ ] `GEMINI_MODEL_NAME` in `bot/utils.py` (or `constants.py`) is updated to `gemini-2.5-flash`.
- [ ] A `RateLimiter` class/function is implemented to track request frequency.
- [ ] Exponential backoff logic is added to retry requests on `429 Too Many Requests` errors.
- [ ] Logs show which model is being used.

### Story 7: Deployment on OCI
**Status:** Completed
**Date:** 2026-01-06
**As a** developer,
**I want** to deploy the bot on OCI,
**So that** it is accessible to users.

**Acceptance Criteria:**
- [x] The bot is running on an OCI instance.
- [x] The bot is accessible via the Telegram UI.
- [x] The deployment process is documented in `docs/OCI_Deployment_Guide.md`.

### Story 4: OCI Deployment Guide
**Status:** Completed
**Date:** 2026-01-05
**As a** User,
**I want** a comprehensive, step-by-step guide on deploying the bot to OCI,
**So that** I can set up my own instance without prior cloud expertise.

**Acceptance Criteria:**
- [ ] `docs/OCI_Deployment_Guide.md` is created.
- [ ] Guide includes steps to create an Always Free AMD/Ampere instance (Ubuntu/Oracle Linux).
- [ ] Guide includes commands to install Docker & Docker Compose on the instance.
- [ ] Guide includes steps to clone the repo, set `.env`, and run `docker-compose up -d`.
- [ ] Guide includes maintenance tips (viewing logs, backing up DB).

### Story 5: Advanced Analytics Feature
**Status:** Completed
**Date:** 2026-01-05
**As a** User,
**I want** to see visual analytics of my journaling habits (sentiment, word count, topics),
**So that** I can understand my emotional trends over time.

**Acceptance Criteria:**
- [ ] `bot/database.py` updated with queries for sentiment aggregation and word count trends.
- [ ] `bot/utils.py` includes logic to straightforwardly visualize this data (e.g., text-based charts or simple Graphviz plots).
- [ ] New `/analytics` command added to `bot/handlers.py`.
- [ ] Command output displays a summary and a visual representation of the data.

### Story 6: Goal Tracking Feature
**Status:** Completed
**Date:** 2026-01-05
**As a** User,
**I want** to set and track personal goals within the bot,
**So that** I can keep myself accountable and monitor my progress.

**Acceptance Criteria:**
- [ ] Database schema updated with `Goals` and `GoalProgress` tables.
- [ ] New commands `/setgoal` and `/mygoals` implemented.
- [ ] Logic added to `bot/handlers.py` to allow users to update progress on standard goals.
- [ ] (Optional/Advanced) Logic added to infer goal progress from journal entries.

## Documentation Updates
**Status:** Completed
**Date:** 2026-01-05
**As a** System,
**I must** update the core documentation to reflect these changes.

**Acceptance Criteria:**
- [ ] `docs/Product_Architecture.md` updated with the new Docker-based deployment context and table schemas.
- [ ] `docs/README.md` updated with new setup instructions (Docker vs. local) and new commands.
