from setuptools import find_packages
from setuptools import setup

with open("requirements.txt") as f:
    content = f.readlines()
requirements = [x.strip() for x in content if "git+" not in x]

setup(name='aiml_research_pulse',
      version="0.0.7",
      description="AI/ML Research Pulse",
      license="MIT",
      author="zmazz",
      author_email="ziad.mazzawi@gmail.com",
      #url="https://github.com/zmazz/aiml_research_pulse",
      install_requires=requirements,
      packages=find_packages(),
      test_suite="tests",
      # include_package_data: to install data from MANIFEST.in
      include_package_data=True,
      zip_safe=False)
