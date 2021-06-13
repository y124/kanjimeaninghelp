import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
     name='kanjilearn',  
     version='1.1.1',
     scripts=['kanjilearn', 'data1.json', 'data2.json', 'kanjimemo', 'RAWKANJI'] ,
     install_requires=requirements,
     author="y124",
     author_email="y124@y124.tk",
     description="Learn kanji with tkinter app",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="https://github.com/y124/kanjimeaninghelp",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
