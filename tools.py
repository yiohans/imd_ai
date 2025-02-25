from typing import Optional

def search_process(id: str) -> Optional[str]:
    """
    Search for a process in the processes folder

    Args:
        id (str): Process number to search for
        e.g. 166/2025 or 1662025

    Returns:
        Optional[str]: Folder name of
        the process if found, None otherwise
    """
    import os

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
            print(f"Searching for {folder}")
            if os.path.exists(os.path.join(processes_path, folder)):
                print(f"Process {id} found!")
                return folder
            else:
                print(f"Process {id} not found!")
                return None
        else:
            folder = f"SEI_{id.split('/')[0]}_{id.split('/')[1]}"
            print(f"Searching for {folder}")
            if os.path.exists(os.path.join(processes_path, folder)):
                print(f"Process {id} found!")
                return folder
            else:
                print(f"Process {id} not found!")
                return None
    except Exception as e:
        print(f"Error: {e}")
        return None

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
    
print(read_doc("processos/SEI_00166_2025/Empenho 0146555.pdf"))