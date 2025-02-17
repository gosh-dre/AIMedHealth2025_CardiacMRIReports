# QnA Tool : Question and Answer tool using Tranformers for Entity extraction

## 🚀 Introduction

We have developed this application to extract key entities from unstructured text with the help of Large Language Models.textual data in healthcare is often unlabelled and lacks structure, thereby constraining the use of
such data for research. This tool can work with different models; and can be flexible with different prompting styles



## Getting Started

Before getting started with this Tool, Process the pdf files using the 'docprocessor' tool to generate the intermediate JSON files; the QnA tool is designed to work with the data structure of intermediate JSON files from the Docprocessor tool. Move the intermediate JSON files to the folder 'JSONInput'.

We have developed the pipeline considering 'roberta-large-squad2-hp' as the model for QnProcessor; but you can choose different models. just make sure the input and output data flows of the model is compatible with existing pipeline or do some data reshaping just to make sure everything is compatible.

You can edit the 'prompt.json' file in the folder prompts to change the questions and formating according to your requirement.

## 📚 Installations

# Run without Docker

To install and run it locally on your laptop without a docker/podman container,

1. clone the repository
2. setup a virtual environment with python= ">=3.10,<3.11" and use the following command to install packages via [poetry](https://python-poetry.org/) 

```
cd QnProcessor
poetry install
poetry run QnProcessor.py

```

You will be able to see the progress of the pipeline in the console; also corresponding structured information against each intermediate json file will be populated in the folder 'JSONOutput' and logfiles in the folder 'logreports'

# Run with Docker

1. clone the repository
2. use the Dockerfile script to create the container image

```
docker build -t qnatool .

```

Run the docker container with access to shell.

```
docker run -it qnatool /bin/bash .

```

Once the files are moved to 'JSONInput' folder, run the QnA pipeline by running the following command in the docker shell.

```

poetry run QnProcessor.py 

```

An output screen will show the file that is being processed and the time it is taken to complete.
you will be able to see the log of the process in the file 'processing.log' in the logreports folder.
As each pdf file is processed, you can see the corresponding JSON file in the jsonreports folder.





## Further information

### 🤝 Core Contributors
- Sebin Sabu (Maintainer) - Data Scientist @ GOSH DRIVE
- Pavithra Rajendran      - NLP & Computer Vision Lead @ GOSH DRIVE
- Alexandros Zenonas      - PHC Digital Solutions Lead @ Roche
- Jonny Sheldon           - Software Engineer @ GOSH DRIVE

### 🧑🏽‍🤝‍🧑🏽 Citing & Authors

if you find this repository helpful, feel free to cite our publication [Investigating General-Purpose Large Language Models for Patient Information Extraction: A Case Study on Real-World Cardiac MRI Reports](to be updated):

```
@article{
    title = "Investigating General-Purpose Large Language Models for Patient Information Extraction: A Case Study on Real-World Cardiac MRI Reports",
    author = "Sabu, Sebin and Zenonos, Alexandros and Taylor, Andrew and Sheldon, Jonny and Pope, Rebecca and Sebire, Neil and Rajendran, Pavi and Patel, Shirin",
    booktitle = "to be updated",
    month = "to be updated",
    year = "to be updated",
    publisher = "to be updated",
    url = "to be updated",
}
```


### 📃 Licenses

Code in this repository is covered by the MIT License and for all documentation the Open Government License (OGL) is used.
Copyright (c) 2025 Crown Copyright