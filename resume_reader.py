"""
resume_reader.py

This module is responsible for reading resume and job-description
text files.

No external packages are used.
Only Python built-in features are used.
"""


def read_text_file(file_path):
    """
    Read a text file and return its contents.

    Parameters:
        file_path (str): Path of the text file.

    Returns:
        str: Contents of the file.
    """

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        return content

    except FileNotFoundError:
        print(f"Error: File not found -> {file_path}")
        return ""

    except PermissionError:
        print(f"Error: Permission denied -> {file_path}")
        return ""

    except Exception as error:
        print(f"Error while reading file: {error}")
        return ""


def read_resume(file_path):
    """
    Read the resume file.

    Parameters:
        file_path (str): Path of the resume.

    Returns:
        str: Resume content.
    """

    return read_text_file(file_path)


def read_job_description(file_path):
    """
    Read the Job Description (JD) file.

    Parameters:
        file_path (str): Path of the JD.

    Returns:
        str: Job description content.
    """

    return read_text_file(file_path)


def validate_file(file_path):
    """
    Check whether a file can be opened and contains data.

    Parameters:
        file_path (str): Path of the file.

    Returns:
        bool: True if valid, otherwise False.
    """

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read().strip()

        if content:
            return True

        return False

    except (FileNotFoundError, PermissionError, OSError):
        return False


def get_file_statistics(file_path):
    """
    Return basic statistics about a text file.

    The statistics include:
        - number of characters
        - number of words
        - number of lines

    Parameters:
        file_path (str): Path of the file.

    Returns:
        dict: File statistics.
    """

    content = read_text_file(file_path)

    if not content:
        return {
            "characters": 0,
            "words": 0,
            "lines": 0
        }

    words = content.split()
    lines = content.splitlines()

    return {
        "characters": len(content),
        "words": len(words),
        "lines": len(lines)
    }


# Test section
# This section runs only when this file is executed directly.
if __name__ == "__main__":

    print("=" * 50)
    print("RESUME READER TEST")
    print("=" * 50)

    test_file = "sample_data/resume.txt"

    if validate_file(test_file):

        resume = read_resume(test_file)

        print("\nResume successfully loaded!")
        print("-" * 50)

        print(resume)

        print("-" * 50)

        statistics = get_file_statistics(test_file)

        print("File Statistics")
        print("Characters :", statistics["characters"])
        print("Words      :", statistics["words"])
        print("Lines      :", statistics["lines"])

    else:
        print("Resume file could not be found.")
        print(f"Expected location: {test_file}")