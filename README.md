# 🏗️ Intelligent Real Estate Offer & Onboarding Automation
## 📖 Description

This project demonstrates how to combine UiPath RPA (for Document Understanding, orchestrating workflows, and system integration) with Python (Flask) for AI-driven capabilities such as anomaly detection, smart summaries, and contact data creation.

It is designed for real estate businesses to automate repetitive manual tasks like building offers, onboarding customers, validating contracts, and managing contact data — freeing up teams from administrative bottlenecks.
## 🎯 Objectives

Automate the end-to-end real estate offer workflow.

Use UiPath Document Understanding to process contracts, addenda, invoices.

Call Python AI services (Flask APIs) for:

   - 🔎 Anomaly detection (detect unusual deals using Isolation Forest).

   - 📝 NLP Summaries (generate human-readable summaries of offers).

   - 👤 Contact Data API (create buyer/seller contacts with emails, phones, addresses).

- Reconcile extracted data with Excel / backend systems.

- Ensure enterprise-grade deployment: secure API, logging, monitoring.

## ⚙️ How It Works

UiPath extracts structured data from documents.

Calls Flask API endpoints with JSON payloads:

- /predict → anomaly detection on offer values.

- /summary → generates human-readable contract summary.

- /contact → creates contact payload for CRM/Google Contacts.

Flask returns JSON → UiPath continues workflow.

Final contracts are reconciled in Excel and sent for DocuSign.

## 📈 Future Enhancements

Fraud detection with duplicate / anomaly patterns.

LLM-powered contract clause suggestions.

ERP/CRM system API integrations (Salesforce, SAP, Dynamics).

Dashboard with offer pipeline analytics.

## Process Map
<img width="1678" height="276" alt="image" src="https://github.com/user-attachments/assets/0de07213-050d-4b0f-9367-97aa1f065395" />


### Documentation is included in the Documentation folder ###


### REFrameWork Template ###
**Robotic Enterprise Framework**

* Built on top of *Transactional Business Process* template
* Uses *State Machine* layout for the phases of automation project
* Offers high level logging, exception handling and recovery
* Keeps external settings in *Config.xlsx* file and Orchestrator assets
* Pulls credentials from Orchestrator assets and *Windows Credential Manager*
* Gets transaction data from Orchestrator queue and updates back status
* Takes screenshots in case of system exceptions


### How It Works ###

1. **INITIALIZE PROCESS**
 + ./Framework/*InitiAllSettings* - Load configuration data from Config.xlsx file and from assets
 + ./Framework/*GetAppCredential* - Retrieve credentials from Orchestrator assets or local Windows Credential Manager
 + ./Framework/*InitiAllApplications* - Open and login to applications used throughout the process

2. **GET TRANSACTION DATA**
 + ./Framework/*GetTransactionData* - Fetches transactions from an Orchestrator queue defined by Config("OrchestratorQueueName") or any other configured data source

3. **PROCESS TRANSACTION**
 + *Process* - Process trasaction and invoke other workflows related to the process being automated 
 + ./Framework/*SetTransactionStatus* - Updates the status of the processed transaction (Orchestrator transactions by default): Success, Business Rule Exception or System Exception

4. **END PROCESS**
 + ./Framework/*CloseAllApplications* - Logs out and closes applications used throughout the process


### For New Project ###

1. Check the Config.xlsx file and add/customize any required fields and values
2. Implement InitiAllApplications.xaml and CloseAllApplicatoins.xaml workflows, linking them in the Config.xlsx fields
3. Implement GetTransactionData.xaml and SetTransactionStatus.xaml according to the transaction type being used (Orchestrator queues by default)
4. Implement Process.xaml workflow and invoke other workflows related to the process being automated

