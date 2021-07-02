## Install All Dependencies:
1. run pip install -r requirements.txt
2. run python -m spacy download en_core_web_sm

------------------------------------------------------------------------------------------------------------------------

## Build Environment:
1. Go into the esa_wiki-0.0.1 folder and run
    python setup.py build
    python setup.py install

### Build concept Space for ESA Wikipedia. 
Go into esa_wiki-0.0.1 folder and Run:

    python -m esa_wiki.xml_parse <wiki dump file>
    
    python -m esa_wiki.generate_indices
    
    python -m esa_wiki.matrix_builder

    The wiki dump files are: (choose one)
    a. medium_wiki.xml
    b. nano_wiki.xml or
    c. Download any one of the dumps from https://dumps.wikimedia.org/enwiki/
    d. The dump with 100 articles is present here:
       https://drive.google.com/file/d/1Kt94MWGsxMNZY26lCjS_PSXrLk3XnEOz/view?usp=sharing

Place the downloaded dumps under esa_wiki-0.0.1 folder

------------------------------------------------------------------------------------------------------------------------
Download CDDSM Pre-Trained Model from [here](https://drive.google.com/file/d/1dxdg1aVLzeH-ZlDqUjiTwAnDThUjhuhv/view?usp=sharing) and unzip the folder and place it main directory.

------------------------------------------------------------------------------------------------------------------------
This folder contains the template code for a search engine application.

**main.py** - The main module that contains the outline of the Search Engine. Do not change anything in this file.

**ESA_Wiki.py** - Contains the module to perform Information retrieval using Wikipedia-based Explicit Semantic Analysis

**query_autocomplete.py** - Contains the module to perform query suggestion tasks.

**contextualSpellCheck.py** - Contains module for spellcheck operations

**util.py** - An extra file where you can add any additional processing or utility functions that you may need for any of the sub-tasks.

**sentenceSegmentation.py, tokenization.py, inflectionReduction.py and stopwordRemoval.py** - Implement the corresponding sub-tasks inside the functions in these files.

**Run main.py with the appropriate arguments**

**Usage:** main.py [-custom] [-dataset DATASET FOLDER] [-out_folder OUTPUT FOLDER]

               [-segmenter SEGMENTER TYPE (naive|punkt)] [-tokenizer TOKENIZER TYPE (naive|ptb)]
               
               [-spellcheck] [-spellcheck_doc] [-spellcheck_query] [-eval_query]

When -spellcheck is passed, spellcheck operations are done for both documents as well as the queries.

If -spellcheck_doc is given, spellcheck operations are done only on the documents.

If -spellcheck_query is given, spellcheck operations are done only on the queries.

If -eval_query is passed, the main.py programs runs evaluation on the Query Autocomplete System

When the -custom flag is passed, the system will take a query from the user as input. When the flag is not passed, all

the queries in the Cranfield dataset are considered, for example:

> python main.py -custom
> Enter query below
> Papers on Aerodynamics
> 
This will generate *queries.txt files in the OUTPUT FOLDER after each stage of preprocessing of the query and *docs.txt files in the OUTPUT FOLDER after each stage of preprocessing of the documents.

