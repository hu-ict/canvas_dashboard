from azure.storage.blob import BlobServiceClient
import os

CONNECTION_STRING = os.getenv('STORAGE_CONNECTION_STRING', 'DefaultEndpointsProtocol=https;AccountName=canvasdashboardstorage;AccountKey=f3e0CWszKW3E/dPJbaKz2Kenn5bq/nVrxY/wieDui6DL9Uu6U5LZD9UUNDn6tOjSu3JldqePwcKW+AStPJFEWw==;EndpointSuffix=core.windows.net')
CONTAINER_NAME = os.getenv('STORAGE_CONTAINER_NAME', 'webapp')
local_directory = os.path.abspath(os.path.join(os.getcwd(), "courses"))


def delete_all_blobs(container_name):
    service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
    container_client = service_client.get_container_client(container_name)

    print(f"Deleting all blobs in container: {container_name}")

    blobs = container_client.list_blobs()
    for blob in blobs:
        print(f"Deleting blob: {blob.name}")
        container_client.delete_blob(blob.name)

    print("All blobs have been deleted.")

def upload_files_with_overwrite():
    print("Starting upload of files with overwriting")

    if not os.path.exists(local_directory):
        print(f"Error: Path '{local_directory}' does not exist!")
        return

    service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
    container_client = service_client.get_container_client(CONTAINER_NAME)

    for root, dirs, files in os.walk(local_directory):
        print(f"Processing folder: {root}")
        print(f"Subdirectories: {dirs}")
        print(f"Files: {files}")

        for file in files:
            blob_path = os.path.relpath(os.path.join(root, file), local_directory)
            blob_client = container_client.get_blob_client(blob_path)

            with open(os.path.join(root, file), "rb") as data:
                blob_client.upload_blob(data, overwrite=True)
                print(f"Uploaded (overwritten if exists): {blob_path}")

# def find_blob_by_name(container_name, file_name, students_folder="test_inno/dashboard_test_inno/students/"):
#     service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
#     container_client = service_client.get_container_client(container_name)
#
#     # List blobs in the students folder
#     print(f"Searching for {file_name} in {students_folder}...")
#     blobs = container_client.list_blobs(name_starts_with=students_folder)
#
#     for blob in blobs:
#         if blob.name.endswith(file_name):
#             blob_url = f"https://{service_client.account_name}.blob.core.windows.net/{container_name}/{blob.name}"
#             print(f"Found file: {blob_url}")
#             return read_blob_content(CONTAINER_NAME, blob.name)
#     print(f"File {file_name} not found in {students_folder}.")
#     return None

def find_teacher_index():
    service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
    container_client = service_client.get_container_client(CONTAINER_NAME)

    print(f"Searching for index in the container '{CONTAINER_NAME}'...")

    blobs = container_client.list_blobs()

    for blob in blobs:
        if f"index" in blob.name:
            blob_url = f"https://{service_client.account_name}.blob.core.windows.net/{CONTAINER_NAME}/{blob.name}"
            print(f"Found file: {blob_url}")
            return read_blob_content(CONTAINER_NAME, blob.name)

    print(f"File index not found in the container '{CONTAINER_NAME}'.")
    return None

def find_blob_by_name(file_name):
    service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
    container_client = service_client.get_container_client(CONTAINER_NAME)

    print(f"Searching for {file_name} in the container '{CONTAINER_NAME}'...")

    blobs = container_client.list_blobs()

    for blob in blobs:
        if f"students/{file_name}" in blob.name:
            blob_url = f"https://{service_client.account_name}.blob.core.windows.net/{CONTAINER_NAME}/{blob.name}"
            print(f"Found file: {blob_url}")
            return read_blob_content(CONTAINER_NAME, blob.name)

    print(f"File {file_name} not found in the container '{CONTAINER_NAME}'.")
    return None

def read_blob_content(container_name, blob_name):
    service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
    container_client = service_client.get_container_client(container_name)

    try:
        blob_client = container_client.get_blob_client(blob_name)
        content = blob_client.download_blob().readall().decode("utf-8")
        print(f"Read content from blob: {blob_name}")
        return content
    except Exception as e:
        print(f"Error reading blob {blob_name}: {e}")
        return None


# delete_all_blobs(CONTAINER_NAME)


# upload_files_with_overwrite()



# file_to_find = "Jeroen Cabri index.html"
# blob_name = find_blob_by_name(CONTAINER_NAME, file_to_find)
#
# if blob_name:
#     content = read_blob_content(CONTAINER_NAME, blob_name)
#     print(f"\nContent of {file_to_find}:\n{content[:1200]}...")

# find_teacher_index()
#
# blob_name = find_teacher_index()
#
# if blob_name:
#     content = read_blob_content(CONTAINER_NAME, blob_name)
#     print(f"\nContent of index:\n{content[:500]}...")