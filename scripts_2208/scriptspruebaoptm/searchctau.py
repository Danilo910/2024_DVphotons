import os

def search_ctau(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py") or file.endswith(".cpp") or file.endswith(".h"):
                filepath = os.path.join(root, file)
                for encoding in ["utf-8", "latin-1"]:  # Try different encoding formats
                    try:
                        with open(filepath, 'r', encoding=encoding) as f:
                            for line_num, line in enumerate(f, start=1):
                                if 'EvtPDL' in line:
                                    print(f"{filepath}:{line_num}: {line.strip()}")
                        break  # Break the loop if file is successfully decoded
                    except (UnicodeDecodeError, OSError):
                        pass  # Continue to the next encoding format or file

# Replace '/path/to/mg5_amc' with the actual path to your MadGraph5_aMC@NLO installation directory
search_directory = '/Collider/MG5_aMC_v2_9_11/HEPTools'

search_ctau(search_directory)

