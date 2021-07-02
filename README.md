# Text-Based Search Engine
This project is an implementation of a Text-Based Search Engine. The search engine employs methods:
1. **Wikipedia based Explicit Semantic Analysis (ESA-Wiki)** for Information Retrieval
2. **Convolution Latent Semantic Model (CLSM)** based methods for Query Autocomplete
3. **Contextual Spell Checker using BERT** for SpellCheck

## SpellCheck
[Contextual spell checker using BERT](https://spacy.io/universe/project/contextualSpellCheck), while learning BERT model looks for the [MASK] tokens and then attempts to predict the original value of the masked words, based on the context provided by the other, non-masked, words in the sequence. During testing the incorrect words are masked and the other non-masked words are used to predict the masked words. In the current project we used pre-trained contextual spell checker. The short coming of this spacy.io model is that it’s more focused on the non-word spelling.
### Example:
_Input Text (with spelling error):_ "Income was $9.4 melon compared to the prior year of $2.7 milion"

_Output Text (after spellcheck):_ "Income was $9.4 million compared to the prior year of $2.7 million"

As seen above can not only detect and fix non-words (milion→million ) butalso word spelling errors (melon→million) based on the context of the sentence.


## Information Retrieval - ESA Wikipedia
Explicit  Semantic  Analysis  (ESA)  represents  meaning  in  a  high-dimensional space of concepts, automatically derived from human-built repositories such as Wikipedia. In ESA Wikipedia, each word is represented by a vector storing the word’s association weights to Wikipedia-derived concepts. Each concept is generated from a single Wikipedia article, and is represented as a vector of words that occur in this article weighted by their tf.idf score. Once these concept vectors are generated, an inverted index is created to map back from each word to the concepts it is associated with.

### Architecture Used
Each Document is split into length-based overlapping passages (document concepts). The reasons for doing this:
* A  small  part  of  a  long  document  might  be  relevant  to  the  current  query, but  the  semantics  of  this  part  may  be  under-represented  in  the  concepts vector  (gotten  from  ESA)  for  the  full  document.  Previous  research  using BOW representation has shown that breaking long documents into shorter passages  can  improve  document  retrieval [Callan  1994;  Liu  and  Croft 2002].
* Furthermore, it has often been shown that fixed-length passages yield better results than passages based on syntactic or semantic segmentation [Callan 1994; Kaszkiel and Zobel 2001].

Upon receiving a query, the algorithm first converts it to an ESA concept vector. The representation method is identical to the one by which documents are represented at index time. Then the cosine similarity between the document vectors (passages) and the query vectors are calculated and the score of the best performing passage of a particular document is considered the cosine similarity score for that document.

The ESA library used here is from [ESA Wiki](https://pypi.org/project/esa-wiki/). The library builds the tf.idf matrix given the set of Wikipedia articles in xml format. These articles dumps can be found at [http://dumps.wikimedia.org/enwiki/](http://dumps.wikimedia.org/enwiki/).

To read more about the architecture used here you can read the paper by Evgeniy Gabrilovich and Shaul Markovitch: Computing Semantic Relatedness usingWikipedia-based Explicit Semantic Analysis.

### Example Query and Retrieved Document:
_Query:_ "what are the structural and aeroelastic problems associated with flight of high speed aircraft"

_Top Document Retrieved:_ "The effect of turbulence on slider bearing lubrication . based on prandtl’s mixing-length mechanism, the pressure equation for turbulent flow in slider-bearing lubrication is derived . an analytical solution is given and compared with the one for laminar flow . it is found that the turbulent effect increases the pressure and consequently, the load-carrying capacity. however, the power loss also increases"

As  seen  above  the  Semantic  Interpreter  is  able  to  make  relations  outside  just word matching.

## Query Autocomplete System
There are two parts to Query Autocomplete namely, Candidate Generation and Candidate Ranking. The proposed methods for each of the following are mentioned below.

### Candidate Generation
From every query in the search engine logs we generate  all  possible  n-grams  from  the  end  of  the  query.  For  example,  from  the query ”bank  of  america”  we  generate  the  suffixes  ”america”,  ”of  america” and ”bank of america”. Next, for a given prefix we extract the end-term. We match all the suffixes that start with the end-term from our precomputed set. These selected  suffixes  are  appended  to  the  prefix  to  generate  synthetic  suggestion candidates.

### Candidate Ranking
For ranking the generated candidates we use a Convolutional Latent Semantic Model (CLSM) as mentioned in the paper (by YelongShen  et.  al).  The  latent  semantic  model  incorporates  a  convolutional-pooling structure over word sequences to learn low-dimensional, semantic vector representations for search queries and Web documents.

We  adopt  the  CLSM  by  training  on  a  prefix-suffix  pairs  dataset  (instead  of query-document titles). The training data for the CLSM is generated by sampling  queries  from  the  search  logs  and  splitting  each  query  at  every  possible word  boundary.  Now  given  a  prefix  P  and  a  suggestion  candidate  C,  we  extract a normalized prefix p and a normalized suffix s. Then we use the trained CLSM  model  to  project  the  normalized  prefix  and  the  normalized  suffix  to  a common n-dimensional (128-dimensional) space and compute a clsmsim feature. The clsmsim feature used here is cosine similarity between the two n-dimensional vectors.

You can read more about this from the paper by Bhaskar Mitra and Nick Craswell: Query Auto-Completion for Rare Prefixes.

### Example Partial Query and Suggestions:
_Partial Query:_ "structural and aero"

_Suggestions:_
* "structural and aerodynamic problems"
* "structural and aerodynamic heat transfer to conical bodies for both laminar and turbulent flow"
* "structural and aerodynamic coefficients during re-entry"

## Usage
README and Usage of the code is given under the Project Directory.
