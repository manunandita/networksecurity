from setuptools import setup,find_packages
from typing import List

def get_requirements()->List[str]:
    try:
        requirement=[]
        with open("requirements.txt","r") as file:
            file_lines=file.readlines()
            for file_line in file_lines:
                lib=file_line.strip()
                if lib!="-e .":
                   requirement.append(lib) 
    except FileNotFoundError:
        raise("requirements.txt file not found")
    return requirement

setup(
    name="NetworkSecurityp",
    version="0.0.1",
    author="nandita manu",
    author_email="manunandita2005@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements()

)

