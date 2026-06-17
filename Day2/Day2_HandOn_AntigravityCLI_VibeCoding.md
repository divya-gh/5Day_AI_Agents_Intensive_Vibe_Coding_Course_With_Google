# Vibe coding with Antigravity CLI

 Ask Antigravity CLI to generate an application and then push the initial version to a GitHub repository.

 ## Prerequisite

- Git
- Antigravity CLI
- Python 3 environment
- Setup gh ( GitHub CLI tool).
- Familiarity with Git basics and a bit of programming knowledge

# WorkFlow

1. Git bash into your Home directory 
2.  Creat a folder :  `mkdir agy-cli-projects`
3. `cd` into 'agy-cli-projects'
4. Creat a sub folder :  `bq-releases-note`
5.  `cd .` back to 'agy-cli-projects'
6. Launch antigravity CLI from bash: `agy`
7. Prompt :
```
"Please build a web application for me using Python Flask and plain vanilla HTML, JavaScript and CSS that fetches the BigQuery Release notes from (https://docs.cloud.google.com/feeds/bigquery-release-notes.xml) and shows them to me. 

A simple refresh button with a spinner is good enough, anytime I'd like to refresh the details. 

I would also like the ability to take any specific update, select it and then Tweet about it."
```
- Antigravity CLI will come up with a plan and ask you for any confirmations / clarifications or go ahead
- Need to follow the instruction


### Antigravity Artifacts
Artifacts are how the Antigravity CLI keeps us in the loop with an implementation plan.
- Includes 
    - `list of tasks` that it is working on, 
    - verifiable outputs and more. 
- These files are generated and are a record of the work that Antigravity is doing, its plan, task list and more.

#### implementation_plan.md
 - outline of the design and architecture of your projects
    - the BigQuery Release Notes Web Application.

### View Artifacts
- command `/artifact` : display the artifact that it generated `implementation_plan.md `

## Push changes to a Github repository
- Follow the instruction to provide permission
    - gitHub repo created
    - authenticated
    - gitignore added
    - Project pushed to github

<img src=".././Images/antigravity_cli_git.png" width="400" height="500">

## Website: 
<img src=".././Images/website_antgr_CLI.png" width="400" height="500">

----------

## Using Antigravity CLI to work with a code repository

### Goal:
* Understanding the code base
* Generating documentation
* Implementing a new feature

### Prerequisite
**To perform the tasks in this section, you will need to the following:**
- Antigravity CLI
- You should have completed the previous section and have the code that has been generated handy, where we created a BigQuery Release Notes reader.

## Workflow

### 1. Understanding the code base - Prompts:

```
I would like to understand this project in detail. Help me understand the main features and then break it down into Server and Client side. Take a sample flow and show me how the request and response works. 
```
- Check `**/artifact****command.**`

### 2. ```Explain @app.py```

### 3. Generating a README file
  - Prompt : ```Generate a README file for this project.```


--------------------

## Implementing a new feature
### Prompt:
```
Please implement two simple utility features: a "Copy to Clipboard" button on each card and an "Export to CSV" button.
Please implement a simple toggle switch in the header that swaps the page's color scheme from dark to light mode by overriding the CSS root variables.
```
- provides you with a plan to approve
- On approval, Antigravity CLI will go ahead and make those changes.
- Check out for bugs
- Ask Antigravity CLI to fix it.

## Generate Issues based on suggested features
prompt:
```
I would like you to assess the application from a user experience point of view. Ease of use, responsiveness, helpful messages and more. Please come up with a list of improvements and I would like you to provide them as a list to me.

```
- Use one of the issues ot improve the web page

## Other Use cases
- arranging files into folders, 
- fetching and summarizing content from the web, 
- processing image files and extracting content from them,
- working with databases and more.

## Example:

### 1. Organizing Files/Folders
- Open agy in the folder you want to be organized
- EX: your Desktop or your Downloads folder.
- Ask Antigravity CLI to create some folders first: Images, Documents, Videos and then you will ask Antigravity CLI to organize the files in the folders.

### 2. A few other organizing scenarios 
**(the prompts are given next to each scenario):**

### Summarization: 
For each document in the ‘Documents' folder, create a txt file in the same folder named ‘summary_ORIGINAL_FILENAME.txt' that contains a 3-sentence summary of the document's main points.

### Categorizing by Type: 
Scan all PDF and DOCX files in this directory. Move all files with "invoice" in their name or content into the ‘Financial/Invoices' folder. Move files with "receipt" into ‘Financial/Receipts'. Any other .docx files go into ‘Reports'.

### Extracting Key Information (and "tagging"): 
For each PDF file in the ‘Financial/Invoices' folder, read its content. If you find a date, rename the file to include that date in YYYY-MM-DD format, e.g., ‘invoice_2025-07-26_original_name.pdf'.


### 3. Summarizing Articles (Local Files or Web)
#### Summarize a web article (single URL): 
- Go to https://medium.com/google-cloud/antigravity-cli-tutorial-series-12b46cfe3bf2 and summarize the top 3 key takeaways from this news article.

#### Summarize multiple web articles (e.g., from a search): 
- Find the latest news articles about "Antigravity CLI" using Google Search. For the top 5 relevant articles, summarize each in 2-3 sentences and list their URLs.

#### Summarize a local text file: 
- Summarize the main points of the article in ‘my_research_paper.txt'. Focus on the methodology and conclusions.

#### Summarize a local PDF: 
- Read ‘financial_report_Q2_2025.pdf'. Provide a summary of the financial performance and key challenges mentioned.

### Extracting Specific Information (Local Files or Web)

#### Extract entities from a local article: 
- From ‘biography.txt', list all named individuals and the significant dates associated with them.

#### Extract data from a table in a PDF: 
- In ‘quarterly_sales.pdf', extract the data from the table on page 3 that shows "Product Sales by Region" and present it in a Markdown table format.

#### Extract news headlines and sources from a news website: 
 - Go to ‘https://news.google.com/' (or a similar news site). Extract the main headlines from the front page and their corresponding news sources. Present them as a bulleted list.

#### Find product specifications from an e-commerce page: 
- Browse to ‘https://www.amazon.in/Google-Cloud-Certified-Associate-Engineer/dp/1119871441' (example for a book). Extract the book title, author and other details. Present this in a structured JSON format.

#### Extract duration from a video, in a certain format (eg "2h37m42s").

Answering Questions based on Content (RAG-like behavior)
For each of the scenarios below, feel free to change the url, topic of interest and the local file names as applicable. The filenames provided are sample file names, you can replace them with filenames of files that you have on your system.

Try out any of the following scenarios (the prompts are given next to each scenario):

Q&A on a local document: I'm attaching ‘user_manual.pdf'. What are the steps to troubleshoot network connectivity issues?
Q&A on a web page: Using the content from ‘https://www.who.int/news-room/fact-sheets/detail/climate-change-and-health', what are the primary health risks associated with climate change according to WHO?
Compare information across multiple sources: I have two news articles: ‘article1.txt' and ‘article2.txt', both discussing the recent economic policy changes. Compare and contrast their views on the potential impact on small businesses.
Content Generation based on Extracted Information
For each of the scenarios below, feel free to change the url, topic of interest and the local file names as applicable.

Try out any of the following scenarios (the prompts are given next to each scenario):

Generate a news brief from an article: Read @tech_innovation_article.txt. Write a short, engaging news brief (around 150 words) suitable for a company newsletter, highlighting the new technology and its potential.
Draft an email summarizing a meeting transcript: Here is a meeting transcript file: @meeting_transcript.txt. Draft an email to the team summarizing the key decisions made and action items assigned, including who is responsible for each.


---------------------------

## Antigravity CLI multi-modal support
Antigraity CLI has multi-model support via Gemini and you can ask it to process multi modal files

- Process a bunch of invoice images with Antigraity CLI and extract key information from them. Follow the steps given below:

    - Create a folder on your machine and download some invoices from the following GitHub repository.
    - Launch Antigraity CLI from that folder
#### Prompt:
1. 
```
The current folder contains a list of invoice files in Image format. Go through all the files in this folder and extract the following invoice information in the form of a table: Invoice No, Invoice Date, Invoice Sent By, Due Date, Due Amount.
```
2. 
```
list all files with .png extension in this folder. Extract the invoice information from it by reading them locally and display it in a table format containing the following column headers: : Invoice No, Invoice Date, Invoice Sent By, Due Date, Due Amount. Add a column at the end of the table that shows a red cross emoji in case the due date is in the past.
```

------------------------------------

## Using Antigravity CLI to generate data
**Prompt Antigravity CLI to produce data in various data formats**

####  Sample Prompts:
```
Generate JSON data of sample customer reviews


Generate a JSON array of 3 synthetic customer reviews for a new smartphone. Each review should have 'reviewId' (string, UUID-like), 'productId' (string, e.g., 'SMARTPHONE_X'), 'rating' (integer, 1-5), 'reviewText' (string, 20-50 words), and 'reviewDate' (string, YYYY-MM-DD format).
Generating Mock API Responses (JSON)


Generate a JSON array representing 7 daily sales records for a mock API endpoint. Each record should include 'date' (YYYY-MM-DD, chronologically increasing), 'revenue' (float, between 5000.00 and 20000.00), 'unitsSold' (integer, between 100 and 500), and 'region' (string, either 'North', 'South', 'East', 'West').
Generating Sample Database Insert Statements (SQL)


Generate 5 SQL INSERT statements for a table named 'users' with columns: 'id' (INTEGER, primary key), 'username' (VARCHAR(50), unique), 'email' (VARCHAR(100)), 'password_hash' (VARCHAR(255)), 'created_at' (DATETIME, current timestamp). Ensure the password_hash is a placeholder string like 'hashed_password_X'.
Generating CSV Data for Data Loading/Analysis


Generate 10 lines of CSV data, including a header row, for customer transactions. Columns should be: 'TransactionID' (unique string), 'CustomerID' (integer), 'ItemPurchased' (string, e.g., 'Laptop', 'Monitor', 'Keyboard'), 'Quantity' (integer, 1-3), 'UnitPrice' (float, between 100.00 and 1500.00), 'TransactionDate' (YYYY-MM-DD).
Generate a Configuration file (YAML)


Generate a sample YAML configuration for a 'user_service'. Include sections for 'database' with 'host', 'port', 'username', 'password', 'database_name'. Also include a 'api_keys' section with 'payment_gateway' and 'email_service' placeholders. Use realistic default values.
Generating Test Data for Edge Cases/Validation


Generate a JSON array of 8 email addresses for testing purposes. Include a mix of: 2 valid standard emails, 2 with missing '@', 2 with invalid domains (e.g., '.com1'), and 2 with special characters in the local part that are usually invalid (e.g., spaces or multiple dots).
```
