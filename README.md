# Fragrance Search Engine

## Overview
This project implements a fragrance search engine using **Elasticsearch**, **Kibana**, and **Flask**. The system allows users to perform full-text searches and explore a fragrance dataset. The application integrates Elasticsearch for indexing and searching data, while Kibana is used for monitoring and visualization.

## Features
- **Elasticsearch Integration**:
  - Handles full-text search on fragrance products.
  - Indexes and retrieves data efficiently.
- **Kibana Dashboard**:
  - Provides a graphical interface for monitoring Elasticsearch.
  - Allows administrators to visualize dataset queries.
- **Flask Web Application**:
  - Acts as the frontend for the search engine.
  - Provides a user-friendly interface to explore fragrance products.

## Technologies Used
- **Elasticsearch 8.10.2**: For indexing and search.
- **Kibana 8.10.2**: For data visualization and monitoring.
- **Flask**: Backend web framework.
- **Python**: Core programming language.

## Team Members
- **Miss Suphavadee Cheng** - ID: 6488120
- **Miss Jidapa Moolkaew** - ID: 6488176
- **Miss Pimmada Chompurat** - ID: 6488204

## Prerequisites
- Anaconda (to manage virtual environments and dependencies)
- Elasticsearch 8.10.2
- Kibana 8.10.2

## Installation and Setup
1. **Download Required Files**:
   - Download the project files from [this link](https://drive.google.com/drive/folders/15OnLM_zg1v_5EanuVgijPE-4qNJqax6m?usp=drive_link).

2. **Run Elasticsearch**:
   - Open **Anaconda Prompt #1** and navigate to the Elasticsearch directory:
     ```bash
     cd {Path}\SourceCode_120_176_204\elasticsearch-8.10.2\bin
     .\elasticsearch.bat
     ```

3. **Run Kibana**:
   - Open **Anaconda Prompt #2** and navigate to the Kibana directory:
     ```bash
     cd {Path}\SourceCode_120_176_204\kibana-8.10.2\bin
     .\kibana.bat
     ```

4. **Run Flask Application**:
   - Open **Anaconda Prompt #3** and navigate to the search engine directory:
     ```bash
     cd {Path}\SourceCode_120_176_204\search_engine
     set FLASK_APP=search_app
     set FLASK_ENV=development
     flask run
     ```

5. **Import the Dataset**:
   - Use the Kibana interface to import the dataset (`fragrance-dataset`).
   - Index Name: **fragrance_products**

## Usage
- Access the **Kibana Dashboard** at:
  [http://localhost:5601/](http://localhost:5601/)
- Access the **Fragrance Search Engine** web application at:
  [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

## Notes
- Ensure all necessary services (Elasticsearch, Kibana, and Flask) are running before accessing the application.
- The dataset (`fragrance-dataset`) must be properly indexed in Elasticsearch for search functionality to work.

