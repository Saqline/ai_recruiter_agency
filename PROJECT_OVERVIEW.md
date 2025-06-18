# Project Overview

This project is an AI-powered recruitment system designed to automate and enhance the process of matching job candidates with suitable positions. It takes a candidate's resume as input, analyzes its content, and compares it against a database of job openings to find the best matches. The system then provides a detailed analysis, screening results, and a final recommendation.

The main technologies used in this project are:

*   **Ollama (llama3.2)**: An advanced large language model used for natural language processing tasks such as extracting information from resumes, analyzing candidate profiles, and generating recommendations.
*   **Swarm Framework**: A conceptual framework for coordinating multiple AI agents, each specialized in a specific task within the recruitment workflow. This allows for a modular and scalable architecture.
*   **Streamlit**: A Python library used to create a modern and interactive web application for uploading resumes and visualizing the analysis results.

## Project Structure

The project is organized into the following main directories:

*   **`agents/`**: Contains the Python code for all AI agents.
    *   `base_agent.py`: Defines a base class with common functionalities for all agents.
    *   `orchestrator.py`: Houses the `OrchestratorAgent` which manages the overall workflow.
    *   Other files (e.g., `extractor_agent.py`, `analyzer_agent.py`): Define specialized agents for specific tasks.
*   **`data/`**: Includes data-related modules.
    *   `job_database.py`: Likely responsible for managing and accessing the job listings.
*   **`db/`**: Contains database-related files, including:
    *   `database.py`: Probably contains schema definitions or database connection logic.
    *   `jobs.sqlite`: An SQLite database file used to store job listings.
    *   `schema.sql`: SQL schema for the database.
    *   `seed_jobs.py`: A script to populate the job database with initial data.
*   **`resumes/`**: A directory to store sample resumes for testing or demonstration.
*   **`results/`**: This directory is used to save the output of the analysis performed on resumes.
*   **`tools/`**: May contain utility scripts or tools for development or operational purposes (currently seems to have only `__init__.py`).
*   **`utils/`**: Contains utility modules for common functionalities like logging (`logger.py`) and custom exception handling (`exceptions.py`).
*   **`app.py`**: The main entry point for the application. It includes the code for both the Streamlit web interface and the command-line interface (CLI).
*   **`requirements.txt`**: Lists the Python dependencies required to run the project.

## Workflow

The resume processing workflow is orchestrated by the `OrchestratorAgent` located in `agents/orchestrator.py`. When a resume is submitted (either through the Streamlit UI or the CLI), the following sequence of operations takes place:

1.  **Input**: The system receives the path to a resume file (typically a PDF) and a submission timestamp.
2.  **Extraction**: The `ExtractorAgent` is invoked. Its primary role is to parse the resume content and extract key information such as skills, experience, education, and contact details.
3.  **Analysis**: The extracted data is then passed to the `AnalyzerAgent`. This agent analyzes the candidate's profile, potentially assessing their strengths, weaknesses, and overall suitability for various roles. It might also generate a confidence score for the extracted information.
4.  **Matching**: The analysis results are fed into the `MatcherAgent`. This agent compares the candidate's profile against the job descriptions stored in the `jobs.sqlite` database. It identifies potential job matches and may assign a match score to each.
5.  **Screening**: The information gathered so far (extracted data, analysis, and job matches) is provided to the `ScreenerAgent`. This agent performs a more in-depth screening of the candidate for the matched positions, possibly based on specific criteria or requirements for those roles. It generates a screening report and a screening score.
6.  **Recommendation**: Finally, the `RecommenderAgent` takes all the processed information (context including resume data, extraction, analysis, matching, and screening results) to generate a final recommendation. This could be a summary of the candidate's suitability, suggestions for next steps, or an overall fitness score.
7.  **Output**: The `OrchestratorAgent` aggregates the results from all stages and returns a comprehensive output. This output is then displayed in the user interface (Streamlit or CLI) and can be saved to a text file in the `results/` directory.

The `OrchestratorAgent` ensures a smooth flow of data between these specialized agents, maintaining context and compiling the final results. Each specialized agent focuses on its specific task, contributing to a modular and maintainable system.

## Agents

The core logic of the recruitment system is implemented through a set of AI agents. These agents are built upon a base class and an orchestrator that coordinates their activities.

### `BaseAgent` (`agents/base_agent.py`)

This class serves as the foundation for all other agents in the system. Its key responsibilities include:

*   **Initialization**: Takes a `name` and `instructions` for the agent. The `instructions` parameter provides the system prompt that guides the behavior of the Ollama language model for that specific agent.
*   **Ollama Client**: Sets up a client to communicate with the Ollama API (configured to `http://localhost:11434/v1` by default). It uses the `llama3.2:1b-instruct-q5_0` model.
*   **`_query_ollama(prompt)`**: A protected method that sends a given prompt (along with the agent's system instructions) to the Ollama model and returns the model's textual response. It handles API communication and error reporting.
*   **`_parse_json_safely(text)`**: A utility method to parse JSON content from the Ollama model's response. It includes error handling for cases where the response might not be valid JSON.
*   **`run(messages)`**: A method that is intended to be overridden by each specialized agent. This method defines the specific logic for how an agent processes input messages.

### `OrchestratorAgent` (`agents/orchestrator.py`)

As described in the Workflow section, the `OrchestratorAgent` is responsible for managing the end-to-end processing of a resume. It initializes and calls the specialized agents in the correct sequence, passing data from one agent to the next.

### Specialized Agents

These agents inherit from `BaseAgent` and implement specific tasks in the recruitment pipeline:

*   **`ExtractorAgent` (`agents/extractor_agent.py`)**:
    *   **Purpose**: To extract structured information from the unstructured text of a resume.
    *   **Input**: Resume data (file path).
    *   **Output**: A dictionary containing extracted details like skills, work experience, education, etc.
*   **`AnalyzerAgent` (`agents/analyzer_agent.py`)**:
    *   **Purpose**: To analyze the extracted candidate profile. This might involve assessing the quality of skills, years of experience, and overall coherence of the resume.
    *   **Input**: Extracted data from the `ExtractorAgent`.
    *   **Output**: Analysis results, which could include a summary of the candidate's strengths, areas of improvement, and a confidence score for the analysis.
*   **`MatcherAgent` (`agents/matcher_agent.py`)**:
    *   **Purpose**: To match the analyzed candidate profile with relevant job descriptions from the database.
    *   **Input**: Analysis results from the `AnalyzerAgent`.
    *   **Output**: A list of matched jobs, potentially with details like job title, location, and a match score indicating the relevance.
*   **`ScreenerAgent` (`agents/screener_agent.py`)**:
    *   **Purpose**: To perform a detailed screening of the candidate against the matched jobs or specific screening criteria.
    *   **Input**: The current workflow context, including extracted data, analysis, and job matches.
    *   **Output**: A screening report and a screening score (e.g., a percentage).
*   **`RecommenderAgent` (`agents/recommender_agent.py`)**:
    *   **Purpose**: To provide a final recommendation based on all preceding stages.
    *   **Input**: The complete workflow context.
    *   **Output**: A textual recommendation, which might summarize the candidate's suitability, suggest interview progression, or highlight key decision factors.

Each specialized agent uses the `_query_ollama` method from `BaseAgent` to interact with the language model, guided by its specific `instructions`.

## Data Management

Effective data management is crucial for the recruitment system, covering how job data is stored and how candidate resumes are handled.

### Job Data

*   **Storage**: Job listings are stored in an SQLite database. The database file is `db/jobs.sqlite`.
*   **Schema (`db/schema.sql`)**: This SQL file defines the structure of the database tables used for storing job information. This likely includes tables for jobs, with columns for job ID, title, description, location, requirements, etc.
*   **Database Interaction (`db/database.py`)**: This module probably contains functions to connect to the SQLite database, execute queries, and manage data (e.g., adding, updating, or retrieving job listings). The `MatcherAgent` would use these functions to fetch job descriptions for comparison with candidate profiles.
*   **Seeding Data (`db/seed_jobs.py`)**: This script is used to populate the `jobs.sqlite` database with initial or sample job listings. This is useful for setting up the system for demonstration or testing.
*   **Job Database Module (`data/job_database.py`)**: While `db/database.py` might handle low-level database connections, `data/job_database.py` could provide a higher-level API or ORM-like interface for agents to interact with job data more abstractly, without needing to write direct SQL queries. For instance, it might offer functions like `get_all_jobs()` or `find_jobs_by_criteria()`.

### Resume Handling

*   **Input**: Resumes are expected to be PDF files.
*   **Uploads (Streamlit)**: When using the Streamlit web application:
    *   Users upload resume PDF files via a file uploader widget.
    *   The `save_uploaded_file` function in `app.py` saves the uploaded resume to a temporary location in an `uploads/` directory (created if it doesn't exist). The filename is made unique using a timestamp.
    *   This temporary file path is then passed to the `OrchestratorAgent` for processing.
    *   After processing is complete, the temporary file is deleted for cleanup.
*   **Input (CLI)**: When using the command-line interface:
    *   The user provides the direct file path to the PDF resume as a command-line argument.
    *   This path is directly used by the `OrchestratorAgent`.
*   **Storage of Resumes**: The system, as described, primarily processes resumes on-the-fly. It does not appear to store the resume files themselves or the extracted resume content in a persistent database beyond the temporary storage during processing. The focus is on processing and then saving the *results* of the analysis.
*   **Sample Resumes (`resumes/`)**: The `resumes/` directory contains sample PDF resumes (e.g., `John_Doe_Resume.pdf`, `sample_resume.pdf`). These are used for testing and demonstrating the system's capabilities.

### Results

*   **Storage (`results/`)**: The output from the `OrchestratorAgent` (which includes analysis, matches, screening, and recommendations) is saved as a text file in the `results/` directory.
*   **Filename**: The filenames for these results are generated with a timestamp (e.g., `analysis_YYYYMMDD_HHMMSS.txt`) to ensure uniqueness.

## User Interface

The project offers two primary ways to interact with the recruitment system: a web-based application and a command-line interface. Both are implemented within `app.py`.

### Streamlit Web Application

The Streamlit application provides an interactive and user-friendly interface for resume analysis.

*   **Launch**: It's a web application that can be run locally.
*   **Navigation**:
    *   A sidebar provides navigation with options like "Upload Resume" and "About".
    *   The "About" page gives a brief overview of the AI Recruiter Agency and the technologies it uses.
*   **Resume Upload**:
    *   On the "Upload Resume" page, users can upload a resume in PDF format using a file uploader component.
    *   The application saves the uploaded file temporarily.
*   **Processing and Display**:
    *   Once a resume is uploaded, the system processes it using the `OrchestratorAgent`.
    *   Progress is indicated with a spinner and a progress bar.
    *   Upon completion, the results are displayed in a tabbed interface:
        *   **Analysis**: Shows skills analysis and a confidence score.
        *   **Job Matches**: Lists matched job positions, including title, match score (if available), and location. It handles cases where no suitable positions are found and avoids displaying duplicate job titles.
        *   **Screening**: Displays the screening score and a detailed screening report.
        *   **Recommendation**: Presents the final recommendation from the system.
*   **Results Saving**: After displaying the results, the application saves them to a text file in the `results/` directory.
*   **Styling**: Custom CSS is used to enhance the visual appearance of the application, including styling for progress bars and text elements (success, warning, error messages).

### Command-Line Interface (CLI)

The CLI provides a way to process resumes directly from the terminal, suitable for scripting or users who prefer command-line tools. The CLI part of `app.py` is currently commented out but demonstrates the intended functionality.

*   **Invocation**: If enabled, it would be run using a command like `python app.py <path_to_resume.pdf>`.
*   **Input**: Takes the path to a PDF resume file as a command-line argument.
*   **Processing**:
    *   It validates the file path and checks if the file is a PDF.
    *   It uses the `OrchestratorAgent` to process the resume, similar to the Streamlit app.
    *   Progress is displayed in the console using `rich` library components (spinner, progress bar).
*   **Output**:
    *   Results are displayed in the console using formatted tables and panels provided by the `rich` library for better readability. This includes:
        *   Skills analysis and confidence score.
        *   A table of job matches (position, match score, location).
        *   Screening results (score and report).
        *   The final recommendation.
*   **Results Saving**: Like the Streamlit app, the CLI saves the detailed analysis results to a text file in the `results/` directory.
*   **Verbose Mode**: An option for `--verbose` output is included, managed via `argparse`.

Both interfaces rely on the same underlying `OrchestratorAgent` and agent system, ensuring consistency in the analysis regardless of how the system is accessed.

## Configuration

The primary configuration for the system revolves around the AI model interaction and Python dependencies.

### Ollama Model Configuration

*   **Model Used**: The system is configured to use `llama3.2:1b-instruct-q5_0`. This is specified in the `_query_ollama` method within the `agents/base_agent.py` file.
    ```python
    response = self.ollama_client.chat.completions.create(
        model="llama3.2:1b-instruct-q5_0", # Model specification
        messages=[
            {"role": "system", "content": self.instructions},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        max_tokens=2000,
    )
    ```
*   **Ollama API Endpoint**: The `BaseAgent` class initializes the OpenAI client (which is adapted for Ollama) to connect to `http://localhost:11434/v1`.
    ```python
    self.ollama_client = OpenAI(
        base_url="http://localhost:11434/v1", # Ollama server address
        api_key="ollama",  # Required by the library but unused by Ollama
    )
    ```
    To use a different Ollama instance (e.g., running on a different host or port), this `base_url` would need to be modified.
*   **Model Parameters**:
    *   `temperature`: Set to `0.7` to control the randomness of the model's output.
    *   `max_tokens`: Set to `2000` to limit the length of the generated response.
    These parameters can also be adjusted in `agents/base_agent.py` if different model behavior is desired.
*   **Running Ollama**: The system requires a running Ollama instance with the `llama3.2:1b-instruct-q5_0` model downloaded and available. Instructions for setting up Ollama and pulling models can be found on the [Ollama website](https://ollama.com/).

### Python Dependencies

*   **`requirements.txt`**: This file lists all the Python packages required for the project to run correctly. Key dependencies likely include:
    *   `streamlit`: For the web application.
    *   `openai`: The client library used to interact with the Ollama API.
    *   `rich`: For enhanced CLI output (if the CLI part is used).
    *   PDF processing libraries (e.g., `pypdf2` or `pdfminer.six`) would be implicitly needed by the `ExtractorAgent`, though not directly configured in `BaseAgent`. These would be part of the overall project setup.
*   **Installation**: Dependencies should be installed using pip:
    ```bash
    pip install -r requirements.txt
    ```

### Agent Instructions

*   Each specialized agent (`ExtractorAgent`, `AnalyzerAgent`, etc.) is initialized with specific `instructions` in its constructor. These instructions act as the system prompt for the Ollama model, guiding its behavior for the task that particular agent is designed for. Modifying these instructions is a key way to alter or refine how each agent performs. For example, in `agents/orchestrator.py`:
    ```python
    def _setup_agents(self):
        """Initialize all specialized agents"""
        self.extractor = ExtractorAgent() # Default instructions from ExtractorAgent class
        self.analyzer = AnalyzerAgent()
        # ...and so on
    ```
    The actual instruction strings are defined within each agent's class definition (e.g., in `agents/extractor_agent.py`).

### Database Configuration

*   **Database File**: The SQLite database path is implicitly configured by its usage in `db/database.py` and potentially `data/job_database.py` to point to `db/jobs.sqlite`. If the database file needs to be moved or renamed, the paths in these files would need to be updated.

No external configuration files (e.g., `.env` or `.ini`) seem to be in use; configurations are mostly hardcoded or managed through `requirements.txt`.

## How to Run

This section provides instructions on how to set up and run the AI Recruitment Agency system.

### Prerequisites

1.  **Python**: Ensure you have Python installed (version 3.8 or higher is recommended).
2.  **Ollama**:
    *   Install Ollama by following the instructions on the [Ollama website](https://ollama.com/).
    *   Pull the required language model:
        ```bash
        ollama pull llama3.2:1b-instruct-q5_0
        ```
    *   Ensure the Ollama application is running and accessible at `http://localhost:11434`.
3.  **Project Files**: Clone or download the project repository to your local machine.

### Setup

1.  **Navigate to Project Directory**:
    Open your terminal or command prompt and change to the root directory of the project.
    ```bash
    cd path/to/your/project-directory
    ```
2.  **Install Dependencies**:
    Install the necessary Python packages using the `requirements.txt` file. It's recommended to do this within a virtual environment.
    ```bash
    # (Optional) Create and activate a virtual environment
    # python -m venv venv
    # source venv/bin/activate  # On Windows: venv\Scripts\activate

    pip install -r requirements.txt
    ```
3.  **Initialize Job Database (if needed)**:
    If the job database `db/jobs.sqlite` is empty or does not exist, you may need to populate it. The project includes a script `db/seed_jobs.py` for this purpose.
    ```bash
    python db/seed_jobs.py
    ```
    Check the script or related documentation for any specific instructions on its usage.

### Running the Streamlit Web Application

1.  **Ensure Ollama is Running**: Verify that your local Ollama instance is active and the `llama3.2:1b-instruct-q5_0` model is available.
2.  **Start Streamlit App**:
    From the project's root directory, run the following command:
    ```bash
    streamlit run app.py
    ```
3.  **Access the Application**:
    Streamlit will typically open the application automatically in your web browser. If not, it will display a local URL (usually `http://localhost:8501`) that you can open manually.
4.  **Usage**:
    *   Navigate to the "Upload Resume" section using the sidebar.
    *   Click the "Choose a PDF resume file" button to upload a resume.
    *   The system will process the resume and display the analysis, job matches, screening results, and recommendations in their respective tabs.

### Running the Command-Line Interface (CLI)

The CLI part of `app.py` is currently commented out in the provided codebase. If it were enabled:

1.  **Ensure Ollama is Running**: Same as for the Streamlit app.
2.  **Run the CLI Script**:
    Execute `app.py` with the path to a resume PDF as a command-line argument:
    ```bash
    python app.py /path/to/your/resume.pdf
    ```
    For example, to use one of the sample resumes:
    ```bash
    python app.py resumes/John_Doe_Resume.pdf
    ```
3.  **View Output**: The results of the analysis will be printed to the console, formatted using the `rich` library. The output will also be saved to a file in the `results/` directory.
    You might use the `--verbose` flag if implemented:
    ```bash
    python app.py resumes/John_Doe_Resume.pdf --verbose
    ```

**Note**: Since the CLI functionality is commented out in the current `app.py`, these CLI instructions are based on its structure and would require uncommenting and potentially minor adjustments to the CLI-specific code block in `app.py` to be fully operational.

## Potential Modifications and Future Enhancements

This AI recruitment system provides a solid foundation. Here are some potential areas for modification, improvement, and future development:

### 1. Agent Enhancements

*   **Refine Agent Instructions**: Experiment with different system prompts (instructions) for each agent to improve the accuracy and relevance of their outputs.
*   **Advanced Error Handling**: Implement more sophisticated error handling and retry mechanisms within agents, especially for Ollama API calls.
*   **State Management**: For more complex interactions or multi-turn conversations within an agent's task, consider more advanced state management.
*   **New Specialized Agents**:
    *   *Feedback Agent*: An agent that collects user feedback on match quality to fine-tune future results.
    *   *Interview Question Generator*: An agent that suggests relevant interview questions based on the candidate's profile and the job description.
    *   *Salary Benchmarking Agent*: An agent that could provide estimated salary ranges based on the role and candidate experience (would require external data sources).

### 2. Model and NLP Improvements

*   **Experiment with Different LLMs**: Try other Ollama models or even integrate with other LLM providers to compare performance and capabilities.
*   **Fine-tuning**: For higher accuracy, consider fine-tuning a smaller model on a domain-specific dataset of resumes and job descriptions.
*   **Improved PDF Parsing**: The accuracy of PDF text extraction is crucial. Investigate more robust PDF parsing libraries or techniques, especially for complex resume layouts, tables, and images.
*   **NER and Relation Extraction**: Enhance the `ExtractorAgent` with more advanced Named Entity Recognition (NER) for specific entities (e.g., company names, job titles, specific tools/technologies) and relation extraction (e.g., "worked at X as Y").

### 3. Data Management and Storage

*   **Persistent Resume Storage**: Implement an option to securely store uploaded resumes and their analysis results in a database for historical tracking and re-analysis, respecting data privacy regulations.
*   **User Accounts**: Add user authentication and accounts to allow recruiters to manage their own job listings and candidate pools.
*   **Job Database Enhancements**:
    *   Support for more complex job queries.
    *   Integration with external job boards via APIs to expand the job database.
*   **Vector Database for Matching**: For more sophisticated semantic matching between resumes and job descriptions, consider using a vector database (e.g., FAISS, Weaviate, Pinecone) to store embeddings of resumes and jobs.

### 4. User Interface and User Experience

*   **CLI Activation**: Fully implement and test the CLI interface.
*   **Interactive Feedback in UI**: Allow users to provide feedback directly in the Streamlit UI (e.g., thumbs up/down on job matches) to help refine the underlying models or algorithms.
*   **Batch Resume Processing**: Add functionality to upload and process multiple resumes at once.
*   **Customizable Dashboards**: Allow users to customize the information displayed in the results.
*   **Export Options**: Provide options to export analysis results in different formats (e.g., CSV, JSON, detailed PDF report).

### 5. System Architecture and Deployment

*   **Asynchronous Task Queues**: For handling large volumes of resume submissions or longer processing times, implement a task queue (e.g., Celery with Redis or RabbitMQ) to process resumes asynchronously.
*   **Configuration Management**: Move hardcoded configurations (like Ollama URL or model name) to external configuration files (e.g., `.env`, YAML) for easier management.
*   **Dockerization**: Containerize the application using Docker for easier deployment and scalability.
*   **Testing**:
    *   Develop a comprehensive suite of unit tests for individual agents and utility functions.
    *   Implement integration tests for the overall workflow.

### 6. Security and Compliance

*   **Data Privacy**: Ensure compliance with data privacy regulations (e.g., GDPR, CCPA) if handling real candidate data, especially if storing resumes.
*   **Input Sanitization and Security**: Strengthen security measures against potential vulnerabilities, especially in the web interface.

These suggestions range from minor tweaks to significant architectural changes, offering a roadmap for evolving the project.
