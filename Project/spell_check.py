import contextualSpellCheck
import spacy

nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("contextual spellchecker")
doc = nlp("Income was $9.4 melon compared to the prior year of $2.7 milion.")

print(doc._.outcome_spellCheck)
