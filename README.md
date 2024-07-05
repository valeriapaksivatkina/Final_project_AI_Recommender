# Final_project_AI_Recommender

# Overview 🌟
This repository provides an AI-driven tool recommender system built using Python. It utilizes natural language processing (NLP) techniques to recommend suitable AI tools based on user input. The system is designed to analyze user interests and match them with AI tools from a curated dataset.

# Key Features 🔍

*User Input Processing:* Utilizes spaCy for NLP to extract keywords from user input.

*Tool Recommendation:* Matches user-provided keywords with descriptions and use cases of AI tools to provide relevant recommendations.

*PDF Generation:* Generates a downloadable PDF report of recommended AI tools along with their details.

*Category Filtering:* Allows users to filter AI tools based on predefined categories such as social media assistant, research, e-commerce, and more.

*Detailed Tool Information:* Displays comprehensive details for each recommended tool, including description, use case, link, reviews, type (free/paid), and charges.


# System Components 💻
*Data Loading:* Loads a CSV dataset containing information about various AI tools.

*Keyword Extraction:* Utilizes spaCy to process user input by tokenizing the text into individual words and tagging each word with its part of speech (POS). It identifies relevant nouns (NOUN) that are not stop words and are alphabetic. 

*Matching Algorithm:* Matches extracted keywords with tool descriptions and use cases to determine relevant tools.

*PDF Generation Module:* Constructs a PDF document summarizing recommended AI tools.

*Streamlit Integration:* Integrates with Streamlit for a user-friendly web interface to interact with the recommender system.

# Usage 📝

*Input:* Users provide their interests through a text input interface.

*Recommendations:* Upon submission, the system generates personalized recommendations based on the input.

*Visualization:* Displays recommended tools in an organized format, with options to view detailed information or download a PDF summary.

*Evaluation:* Users can rate and review their experience with the app, contributing to ongoing improvements.
