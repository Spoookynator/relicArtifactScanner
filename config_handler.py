import ast


def read_bounding_box_file(file_path):
    config_data = {}

    try:
        with open(file_path, 'r') as file:
            current_section = None

            for line in file:
                line = line.strip()

                if not line:
                    # Skip empty lines
                    continue

                if line.startswith('[') and line.endswith(']'):
                    # This line indicates the start of a new section
                    current_section = line[1:-1]  # Extract the section name
                    config_data[current_section] = {}
                elif current_section:
                    # Process key-value pairs within the current section
                    key, value = line.split()
                    config_data[current_section][key] = float(value)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        raise
    except ValueError:
        print(f"Error parsing file. Ensure each line has the format 'key value': {file_path}")
        raise

    return config_data


def write_bounding_box_file(file_path, config_data):
    try:
        with open(file_path, 'w') as file:
            for section, section_data in config_data.items():
                file.write(f'[{section}]\n')
                for key, value in section_data.items():
                    file.write(f'{key} {value}\n')
                file.write('\n')  # Add a newline between sections
    except Exception as e:
        print(f"Error writing to file: {e}")
        raise


def read_whitelist_file(file_path):
    whitelist_data = {}

    try:
        with open(file_path, 'r') as file:
            current_section = None

            for line in file:
                line = line.strip()
                if not line:
                    # Skip empty lines
                    continue

                if line.startswith('[') and line.endswith(']'):
                    # This line indicates the start of a new section
                    current_section = line[1:-1]  # Extract the section name
                    whitelist_data[current_section] = []
                elif current_section:
                    # Process lines within the current section
                    whitelist_data[current_section].append(line)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        raise

    return whitelist_data


def read_config_file(file_path):
    config_data = {}

    try:
        with open(file_path, 'r') as file:
            current_section = None

            for line in file:
                line = line.strip()

                if not line:
                    # Skip empty lines
                    continue

                if line.startswith('[') and line.endswith(']'):
                    # This line indicates the start of a new section
                    current_section = line[1:-1]  # Extract the section name
                    config_data[current_section] = {}
                elif current_section:
                    # Process key-value pairs within the current section
                    key, value = map(str.strip, line.split(maxsplit=1))

                    # Use ast.literal_eval to safely evaluate the value
                    try:
                        value = ast.literal_eval(value)
                    except (ValueError, SyntaxError):
                        # If literal_eval fails, treat the value as a string
                        pass

                    config_data[current_section][key] = value
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        raise

    return config_data


def write_config_file(file_path, config_data):
    try:
        with open(file_path, 'w') as file:
            for section, section_data in config_data.items():
                file.write(f'[{section}]\n')
                for key, value in section_data.items():
                    file.write(f'{key} {value}\n')
                file.write('\n')  # Add a newline between sections
    except Exception as e:
        print(f"Error writing to file: {e}")