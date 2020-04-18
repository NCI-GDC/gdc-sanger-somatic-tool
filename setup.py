from setuptools import setup, find_packages

setup(
    name = "gdc-sanger-tools",
    author = "Kyle Hernandez",
    author_email = "kmhernan@uchicago.edu",
    version = 0.1, 
    description = "Utility tool for GDC Sanger Somatic Workflow",
    license = "Apache 2.0",
    packages = find_packages(),
    python_requires='>=3.5',
    entry_points= {
        'console_scripts':
        ['gdc-sanger-tools=gdc_sanger_tools.__main__:main']
    },
)
