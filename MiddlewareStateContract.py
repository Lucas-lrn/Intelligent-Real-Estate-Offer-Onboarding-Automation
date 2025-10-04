from flask import Flask, request, jsonify
import logging
from datetime import datetime
import os
import xmltodict
import base64
import requests  # for calling UiPath Orchestrator
import json

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Directories to save PDFs
PDF_DIR = "signed_pdfs"
os.makedirs(PDF_DIR, exist_ok=True)

# UiPath Orchestrator settings
UIPATH_ORCH_URL = 'https://cloud.uipath.com/cloudnfxpxxr/DefaultTenant/orchestrator_//odata/Jobs/UiPath.Server.Configuration.OData.StartJobs'
UIPATH_PROCESS_NAME = "Monitor_DocuSign"  # the process in UiPath Orchestrator
UIPATH_BEARER_TOKEN = "rt_5F1B89F956A03A391AFD44B62576F87E3175C99270C65982759342F8712D0D0C-1"

@app.route('/docusign-webhook', methods=['POST'])
def docusign_webhook():
    try:
        content_type = request.content_type
        raw_data = request.data.decode('utf-8')
        logging.info(f"Content-Type: {content_type}")

        envelope_id = None
        envelope_status = None
        recipients_info = []
        pdf_files = []

        if 'text/xml' in content_type or 'application/xml' in content_type:
            data_dict = xmltodict.parse(raw_data)

            # Envelope info
            envelope_status_info = data_dict['DocuSignEnvelopeInformation']['EnvelopeStatus']
            envelope_id = envelope_status_info.get('EnvelopeID')
            envelope_status = envelope_status_info.get('Status')

            # Recipient info
            recipient_statuses = envelope_status_info['RecipientStatuses']['RecipientStatus']
            if isinstance(recipient_statuses, dict):
                recipient_statuses = [recipient_statuses]

            for recipient in recipient_statuses:
                recipients_info.append({
                    "RecipientId": recipient.get('RecipientId'),
                    "Status": recipient.get('Status')
                })

            # Save PDFs
            documents = data_dict['DocuSignEnvelopeInformation'].get('DocumentPDFs', {}).get('DocumentPDF', [])
            if isinstance(documents, dict):
                documents = [documents]

            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            for doc in documents:
                name = doc.get('Name', 'document.pdf')
                pdf_b64 = doc.get('PDFBytes')
                pdf_path = None
                if pdf_b64:
                    pdf_data = base64.b64decode(pdf_b64)
                    pdf_path = os.path.join(PDF_DIR, f"{timestamp}_{name}")
                    with open(pdf_path, 'wb') as f:
                        f.write(pdf_data)
                pdf_files.append({
                    "Name": name,
                    "PDFPath": pdf_path,
                })

            # Prepare variables to send to UiPath
            uipath_input = {
                "envelopeId": envelope_id,
                "envelopeStatus": envelope_status,
                "recipients": recipients_info,
                "pdfFiles": pdf_files
            }

            # Trigger UiPath Process
            headers = {"Authorization": "Bearer " + UIPATH_BEARER_TOKEN, "X-UIPATH-OrganizationUnitId" : "6669357", "Content-Type" : "application/json"}
            
            payload = {
                "startInfo": {
                    "ReleaseKey": "b5d0eae2-83c0-4899-8d33-ee5cf60210b0",  # get from UiPath Orchestrator
                    "Strategy": "ModernJobsCount",
                    "InputArguments": json.dumps(uipath_input)
                }
            }
            response = requests.post(UIPATH_ORCH_URL, json=payload, headers=headers)
            logging.info(f"UiPath Trigger Response: {response.status_code} {response.text}")

        else:
            logging.warning(f"Unsupported Content-Type: {content_type}")
            return jsonify({"error": "Unsupported Content-Type"}), 415

        return jsonify({
            "message": "Webhook processed and UiPath triggered",
            "EnvelopeID": envelope_id,
            "EnvelopeStatus": envelope_status,
            "Recipients": recipients_info,
            "PDFs": pdf_files
        }), 200

    except Exception as e:
        logging.error(f"Error processing webhook: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)