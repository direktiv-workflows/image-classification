# Image classification as SFW / NSFW

The workflow will classify an image uploaded to an Azure Storage Account as SFW or NSFW. The workflow is activated by Microsoft Storage CloudEvent.

## Workflow overview

The worklfow is a pretty comprehensive example of event-driven workflows, serverless functions and Direktiv Apps being used. The workflow does the following:

1. When an image is uploaded to Azure Blob Storage, an event is recieved by Direktiv with the URL of the uploaded image (see https://docs.direktiv.io/events/cloud/azure/ for details on how to configure Azure)
2. The image is then classified using the Google Vision API (http-request)
3. Based on the rating given by Google Vision, we add a watermark to the image:
    - The watermark is added by the Python script (classify-image.yaml.add-watermark.py)
    - The Ptyhon script is run serverless by Direktiv in the Python container
4. An email template is created (in HTML) using Mustache (a Direktiv App https://apps.direktiv.io/search-results/mustache?v=1.0)
5. Send an email with the image (watermarked) to the recipients. 
6. Watermarked image is then uploaded back into Azure Storage and the old image deleted

Any errors are captured using exception handling and ServiceNow incidents are created using the snc-incidet-subflow.yaml workflow

## Variables

 - add-watermark.py: Python code to add a watermark to the image
 - requirements.txt: Python modules to install during runtime
 - Roboto-Black.ttf: Additional fonts used in Python code for the watermark
 - notify-processed.tpl: template used in Mustache to create the notification email

## Secrets

 - GCP_KEY: Google Image classification API key
 - EMAIL_USER, EMAIL_PASSWORD: email credentials
 - AZ_USER, AZ_PASSWORD, AZ_TENANT, AZ_STORAGE_ACCOUNT: Azure credentials
 - SNC_URL, SNC_USER, SNC_PASSWORD: ServiceNow credentials

## Namespace Services

 - None

## Input examples

```json
{
  "Microsoft.Storage.BlobCreated": {
    "data": {
      "api": "PutBlob",
      "blobType": "BlockBlob",
      "clientRequestId": "f9146d76-246b-4fec-75e3-5b8e5daa0c68",
      "contentLength": 602091,
      "contentType": "image/png",
      "eTag": "0x8DB500B45DF658D",
      "requestId": "feaf5f0b-e01e-0038-4ef4-814210000000",
      "sequencer": "00000000000000000000000000010C26000000000067dc78",
      "storageDiagnostics": {
        "batchId": "efa5d22c-2006-006a-00f4-813ef8000000"
      },
      "url": "https://direktiv.blob.core.windows.net/upload/direktiv-overview.png"
    },
    "id": "feaf5f0b-e01e-0038-4ef4-8142100607cf",
    "source": "/subscriptions/40eb3cb3-a114-4cd1-b584-5bbedd2126a2/resourceGroups/vorteil-demo/providers/Microsoft.Storage/storageAccounts/direktiv",
    "specversion": "1.0",
    "subject": "/blobServices/default/containers/upload/blobs/direktiv-overview.png",
    "time": "2023-05-08T21:29:15.0197922Z",
    "type": "Microsoft.Storage.BlobCreated"
  }
}
```