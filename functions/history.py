def history_put_on_top(filename, path_to_history):
    """
    Updates the history file by placing a specific filename at the top.

    Args:
    filename (str): The name of the file to be placed at the top of the history.
    path_to_history (str): The file path to the history file."""
    with open(path_to_history, "r") as file:
        lines = file.readlines()

    lines = [line for line in lines if line.strip("\n") != filename]
    lines.insert(0, filename + "\n")

    with open(path_to_history, "w") as file:
        file.writelines(lines)


def get_sorted_history(prompts_dictionary, path_to_history):
    """
    Returns the prompts sorted by the history and fixes the history file (purge inexistent files in history, add new files which were not present)
    """
    with open(path_to_history, "r") as file:
        history_filenames = file.readlines()
        history_filenames = [x.replace("\n", "") for x in history_filenames]

    files_in_folder = list(prompts_dictionary.values())

    # purging all the elements in history_filenames which are not present in files_in_folder
    history_filenames = [
        filename for filename in history_filenames if filename in files_in_folder
    ]

    # Taking all the elements in files_in_folder and adding them to the bottom of history_filenames
    for filename in files_in_folder:
        if filename not in history_filenames:
            history_filenames.append(filename)

    # Replace the old history
    with open(path_to_history, "w") as file:
        for name in history_filenames:
            file.write(name + "\n")

    # Generates the sorted prompts list from sorted file list
    sorted_promptnames = []
    for filename in history_filenames:
        sorted_promptnames.append(find_key(prompts_dictionary, filename))

    return sorted_promptnames


def find_key(dictionary, value):
    for key, val in dictionary.items():
        if val == value:
            return key
    return None
