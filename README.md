# Data Engineering Learning Path Repository

This repository aims to store all activities related to the data engineering learning path. The projects are divided by branches, following the pattern `feat/activity01`. You can browse through them, and for each one, there is a README with explanations on how to run the projects.

## Current Projects

- **Two Docker Applications (`feat/atividade01`):** A frontend and a backend application for handling JSON files.
- **Spotify API Frontend Application (`feat/atividade02`):** A frontend application with a connection to the Spotify API for music recommendations.
- **Edited CRM Dashboard (`feat/atividade03`):** A modified version of a CRM dashboard built with React.
- **Pyspark and Spark Exercises (`feat/spark`)**
- **Pyspark and Airflow Exercises (`feat/atividade04`)**: Tool to orchestrate Spark applications using Airflow.


## Commit Patterns

Clear commit messages help us understand the evolution of the code and make it easier to locate specific changes. With this in mind, it was created a prompt helper to assist in writing commit messages. The messages are categorized by type:

* feat: for new functionalities
* fix: for bug fixes
* refac: for code changes that don’t alter functionality
* docs: for documentation updates, such as changes to README.md
* test: for adding or modifying tests

Since this tool was developed using [Python 3.11](https://www.python.org/), please ensure that you have it installed on your computer.

Next, create and activate a [virtual environment](https://docs.python.org/3/library/venv.html). After activating the virtual environment, you can run the command: `pip install -r requirements.txt`.

Once the installation is complete, you’re good to go!

Before committing your changes, make sure you have followed all the necessary [Git Steps](https://git-scm.com/docs/gittutorial).

To run the script, use the command: `python commit.py`. If you need to exit the prompt due to an error or any other reason, simply press Ctrl + C.