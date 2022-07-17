import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None

def find_entry_title(content):
    """
    Retrieves an changed entry title by searching between the re.search pattern.
    """
    """
    pattern = "# (.*?)\"
    title = re.search(pattern, content).group(1)
    """
    start = content.find("# ") + len("# ")
    end = content.find("\\")
    title = content[start:end]
    return title

def get_content_without_title(content):
    """
    Retrieves an changed entry content without title by searching between the re.search pattern.
    """
    start = content.find("\\") + len("\\")
    content = content[start:]
    return content