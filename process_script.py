from azure.identity import ManagedIdentityCredential
from azure.storage.blob import BlobServiceClient
import csv
import io
import sys

# Get filename from ADF trigger
FILE_NAME = sys.argv[1]

STORAGE_ACCOUNT_URL = "https://8911midterm.blob.core.windows.net"
SOURCE_CONTAINER = "input"
DEST_CONTAINER = "output"

credential = ManagedIdentityCredential()
client = BlobServiceClient(account_url=STORAGE_ACCOUNT_URL, credential=credential)

source_blob = client.get_container_client(SOURCE_CONTAINER).get_blob_client(FILE_NAME)
dest_blob = client.get_container_client(DEST_CONTAINER).get_blob_client(FILE_NAME)

# Download CSV text from source blob
csv_text = source_blob.download_blob().readall().decode("utf-8-sig")

# Parse all numeric values in the CSV
numbers = []
for row in csv.reader(io.StringIO(csv_text)):
    for cell in row:
        value = cell.strip()
        if not value:
            continue
        try:
            numbers.append(float(value))
        except ValueError:
            # Skip non-numeric cells (e.g., headers)
            pass

# Sort ascending (use reverse=True for descending)
numbers.sort()

# Write sorted numbers back as one number per CSV row
out = io.StringIO()
writer = csv.writer(out, lineterminator="\n")
for n in numbers:
    writer.writerow([int(n) if n.is_integer() else n])

# Upload sorted CSV to destination blob
dest_blob.upload_blob(out.getvalue(), overwrite=True)

# Uncomment for true "move" behavior
# source_blob.delete_blob()

print(f"Sorted {FILE_NAME} and wrote it to {DEST_CONTAINER}/{FILE_NAME}")