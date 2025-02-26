import os
from typing import Optional

def search_process(id: str) -> str:
    """
    Search for a SEI process folder in the file system.

    Use this function to locate administrative process documents by their reference number.
    The function handles both traditional (166/2025) and compact (1662025) ID formats.

    Args:
        id (str): Process number in either format:
            - Separated format: "166/2025"
            - Compact format: "1662025"
            The number will be automatically padded if needed.

    Returns:
        str: One of:
            - Folder name (e.g., "SEI_00166_2025") if process exists
            - None if process not found (compact format)
            - "Process not found" if process not found (separated format or errors)
    """
    root_path = os.path.abspath("")
    processes_path = os.path.join(root_path, "processos")
    try:
        if len(id) < 9:
            if id.find("/") == -1:
                id = id.zfill(9)
            else:
                id = id.split("/")
                id[0] = id[0].zfill(5)
                id[1] = id[1]
                id = "/".join(id)
        if id.find("/") == -1:
            folder = f"SEI_{id[:-4]}_{id[-4:]}"
            # print(f"Searching for {folder}")
            if os.path.exists(os.path.join(processes_path, folder)):
                # print(f"Process {id} found!")
                return folder
            else:
                # print(f"Process {id} not found!")
                return "Process not found"
        else:
            folder = f"SEI_{id.split('/')[0]}_{id.split('/')[1]}"
            # print(f"Searching for {folder}")
            if os.path.exists(os.path.join(processes_path, folder)):
                # print(f"Process {id} found!")
                return folder
            else:
                # print(f"Process {id} not found!")
                return "Process not found"
    except Exception as e:
        print(f"Error: {e}")
        return "Process not found"

def get_documents_from_process(
    parameters: str
) -> list[str]:
    """
    Retrieve PDF documents from a SEI process folder with pagination support.

    Use this function to get a list of PDF documents within a process folder.
    Results can be paginated using limit and offset parameters.
    Typically used after locating a process folder with search_process().

    Args:
        parameters (str): A string containing the process folder name and pagination parameters.
            The string should be formatted as follows:
            "process_folder,limit,offset"
            - process_folder: The name of the process folder (e.g., "SEI_00166_2025")
            - limit: The maximum number of documents to return (default: 10)
            - offset: The number of documents to skip (default: 0)

    Returns:
        Union[dict(str : list[str], str : int), str]: One of:
            - A dict containing:
                - "documents": A list of PDF document names
                - "total_number_of_documents": The total number of documents in the folder
            - "Invalid parameters" if the input string is not formatted correctly
            - "Process folder not found" if the process folder does not exist
    """
    try:
        process_folder, limit, offset = parameters.split(",")
        limit = int(limit)
        offset = int(offset)
    except Exception as e:
        print(f"Error: {e}")
        return "Invalid parameters"
    try:
        tree = os.walk(os.path.join(os.path.abspath(""), "processos", process_folder))
        documents = []
        for root, dirs, files in tree:
            documents.extend([
                file
                for file in files
                if file.endswith(".pdf")
                ])
        documents.sort()
        return {
            "documents" : documents[offset:offset+limit],
            "total_number_of_documents" : len(documents)
        }
    except Exception as e:
        print(f"Error: {e}")
        return "Process folder not found"

def read_doc(file_path: str) -> Optional[str]:
    """
    Reads a PDF document and extracts its text content.

    Args:
        file_path (str): The path to the PDF file.

    Returns:
        Optional[str]: The extracted text from the PDF, or None if an error occurs.

    Notes:
        - Uses PyPDF2 to read the PDF.
        - Returns None if the file cannot be read or an exception occurs.
    """
    from PyPDF2 import PdfReader
    try:
        reader = PdfReader(file_path)
        contents = []
        for i in range(len(reader.pages)):
            page = reader.pages[i]
            contents.append(page.extract_text())
        return "\n".join(contents)
    except Exception as e:
        return f"Error: {e}"