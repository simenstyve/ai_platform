# Welcome!
And thank you for applying to join the AI Platform team!

The task you are about to complete is a simplified version of the kind of work carried out by the AI Platform team. On this occasion, the requirement is to build a tool that enables the migration of prompts from a local environment to cloud storage.

You have a choice of two options for completing the task:
* **In-person**: Building the feature while pairing with one of us. If this is how you wish to proceed, just make sure to build the environment and check that you can successfully run the commands under [Prerequisites](#prerequisites) and [Local Development Environment Setup](#local-development-environment-setup) prior to the pairing session.
* **Take-home**: Building the feature in your own time, before sharing it with us. If you choose this option, please start by completing [Prerequisites](#prerequisites) and [Local Development Environment Setup](#local-development-environment-setup), then continue to [Take-Home Task Instructions](#take-home-task-instructions).

## Prerequisites
### Docker
- Install Docker Desktop or another Docker engine.
  - [Mac](https://docs.docker.com/desktop/setup/install/mac-install/)
  - [Windows](https://docs.docker.com/desktop/setup/install/windows-install/)
  - [Linux](https://docs.docker.com/desktop/setup/install/linux/)
- Ensure Docker is running.

### Start LocalStack
1. Open a terminal in the same directory as `docker-compose.yaml`.
2. Run the following command:
   ```bash
   docker-compose up -d
   ```
   This will launch the LocalStack container in detached mode.


## Local Development Environment Setup
1. Create a virtual environment:
   ```bash
   python -m venv .venv
   ```
2. Activate the virtual environment:
   ```bash
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Make the code available as an editable install:
   ```bash
   pip install -e .
   ```
5. Run the main script:
   ```bash
   python src/main.py 'Hello world!'
   ```

   You should see logs similar to:
   ```
   INFO:__main__:Sending message to LLM chat client: Hello world!
   INFO:__main__:Creating bucket 'ai-platform'
   INFO:__main__:Response from LLM chat client: System prompt: System prompt not found on ai-platform
   User prompt: User prompt not found on ai-platform
   Message: Hello world!
   ``` 

   If running the main script fails, you may need to set the project root on the Python path, e.g.:
   ```bash
   export PYTHONPATH="$PWD"
   ```
6. Run tests (3 tests should pass, 4 should fail):
   ```bash
   pytest .
   ```

## Take-Home Task Instructions
### Background
In this repository, every feature in `/src/features` will have an accompanying `prompts/` folder with prompts stored as `.txt` files.

The prompts may be developed and modified locally, but once we are happy with them, we want to migrate them to an S3 bucket. For the purposes of this task, we will use a locally running S3 bucket named `ai-platform`. We will use LocalStack to simulate a remote AWS environment.

The prompt migration should be triggered by running:
```bash
python src/prompt_service/sync.py 'llm_chat'
```

### Requirements
1. Given an execution of the prompt service's sync migration tool triggered by running `python src/prompt_service/sync.py 'llm_chat'`:
   1. If the `ai-platform` bucket does not exist, then it is created.
   2. Local prompt files in `/src/features/prompts/` are compared with the prompt files stored on the S3 bucket `ai-platform` in the `llm_chat` folder:
      1. Files that **exist on the S3 bucket**, but **do not exist locally**, will be deleted from S3.
      2. Files that **exist locally**, but **do not exist on the S3 bucket**, will be uploaded to S3.
      3. Files that **exist both locally and on S3**, but have **different contents**, will be uploaded from the local environment to S3.
   3. The `ai-platform` S3 bucket will contain the keys `llm_chat/system_prompt.txt` and `llm_chat/user_prompt.txt` With contents `A test system prompt.` and `A test user prompt.` respectively.
2. All tests must pass.
3. Formatting and linting checks must be run and issues addressed.

## Repository Contents
- `.flake8` settings for flake8
- `.gitignore`
- `docker-compose.yaml` for pulling and running LocalStack
- `pyproject.toml` formatter settings
- `README.md`
- `requirements.txt`
- `/src`
  - `/aws`
    - `s3.py` provides an S3 client connected to LocalStack
  - `/features`
    - `/llm_chat`
      - `client.py` a dummy implementation of a chat client
      - `/prompts`
        - `system_prompt.txt`
        - `user_prompt.txt`
  - `/prompt_service`
    - `sync.py` the entry point for the prompt migration tool
  - `main.py` a CLI tool that calls the LLM Chat client

## Formatting & Linting
1. Sort imports:
   ```bash
   isort .
   ```
2. Format the code:
   ```bash
   black .
   ```
3. Run lint checks:
   ```bash
   flake8 .
   ```