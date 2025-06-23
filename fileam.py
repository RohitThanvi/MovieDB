import os

def create_file_with_path():
    file_path = input("Enter the full filename (with or without path): ").strip()

    directory = os.path.dirname(file_path)
    filename = os.path.basename(file_path)

    if directory:
        os.makedirs(directory, exist_ok=True)

    full_file_path = os.path.join(directory, filename) if directory else filename

    try:
        with open(full_file_path, 'w') as file:
            pass  
        print(f"File created successfully: {full_file_path}")
    except Exception as e:
        print(f"Failed to create the file. Error: {e}")

create_file_with_path()
