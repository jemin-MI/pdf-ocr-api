from datetime import datetime
import os
from google.api_core.client_options import ClientOptions
from google.cloud import documentai
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/mind/Documents/jem_test/pdf-ocr-api/google_private/medico_key.json"

class GoogleDocAI:
    def __init__(self):
        self.project_id = os.getenv("PROJECT_ID")
        self.location = os.getenv("LOCATION")
        self.processor_id = os.getenv("PROCESSOR_ID")
        self.processor_version_id = os.getenv("PROCESSOR_VERSION_ID")
        self.mime_type = os.getenv("MIME_TYPE", "application/pdf")
        self.field_mask = os.getenv("FIELD_MASK",None)

        if not all([self.project_id, self.location, self.processor_id]):
            raise ValueError("Missing required environment variables (PROJECT_ID, LOCATION, PROCESSOR_ID)")

    def get_summary_using_google(self, file):
        """
        Process a document using Google Document AI and extract a summary.

        Args:
            file (str): The path to the PDF document.

        Returns:
            str: The extracted summary text.
        """
        location = self.location
        processor_version_id = self.processor_version_id
        project_id = self.project_id
        processor_id = self.processor_id
        mime_type = self.mime_type
        field_mask = self.field_mask

        opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")

        client = documentai.DocumentProcessorServiceClient(client_options=opts)
        if processor_version_id:
            # The full resource name of the processor version, e.g.:
            # `projects/{project_id}/locations/{location}/processors/{processor_id}/processorVersions/{processor_version_id}`
            name = client.processor_version_path(
                project_id, location, processor_id, processor_version_id
            )
        else:
            # The full resource name of the processor, e.g.:
            # `projects/{project_id}/locations/{location}/processors/{processor_id}`
            name = client.processor_path(project_id, location, processor_id)

        # Read the file into memory
        image_content = file.file.read()
        raw_document = documentai.RawDocument(content=image_content, mime_type=mime_type)

        # For more information: https://cloud.google.com/document-ai/docs/reference/rest/v1/ProcessOptions
        # Optional: Additional configurations for processing.
        process_options = documentai.ProcessOptions(
            individual_page_selector=documentai.ProcessOptions.IndividualPageSelector(pages=[1]))

        # Configure the process request
        request = documentai.ProcessRequest(
            name=name,
            raw_document=raw_document,
            field_mask=field_mask,
            process_options=process_options,
        )

        result = client.process_document(request=request)

        # For a full list of `Document` object attributes, reference this page:
        # https://cloud.google.com/document-ai/docs/reference/rest/v1/Document

        document = result.document.entities
        summarise_text = document[0].mention_text

        return summarise_text
