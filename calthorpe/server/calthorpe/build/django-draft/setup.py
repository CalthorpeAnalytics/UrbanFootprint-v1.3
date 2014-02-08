from setuptools import setup, find_packages

setup(
    name = "django-draft",
    version = "0.2.2",
    description = """
    Drafts for django admin
    """,
    author = "Platypus Creation",
    author_email = "contact@platypus-creation.com",
    url = "https://github.com/platypus-creation/django-draft",
    packages = find_packages(),
    include_package_data=True,
)
