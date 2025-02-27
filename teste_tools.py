from tools import *

print(search_process("166/2025"))

print(get_document_list_from_process(f"{search_process("166/2025")},1,0"))

print(get_document_by_type("166/2025,Despacho"))