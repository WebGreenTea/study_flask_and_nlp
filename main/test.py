# import spacy
# from spacy import displacy

# nlp = spacy.load("en_core_web_sm")
# text = """In ancient Rome, some neighbors live in three adjacent houses. In the center is the house of Senex, who lives there with wife Domina, son Hero, and several slaves, including head slave Hysterium and the musical's main character Pseudolus. A slave belonging to Hero, Pseudolus wishes to buy, win, or steal his freedom. One of the neighboring houses is owned by Marcus Lycus, who is a buyer and seller of beautiful women; the other belongs to the ancient Erronius, who is abroad searching for his long-lost children (stolen in infancy by pirates). One day, Senex and Domina go on a trip and leave Pseudolus in charge of Hero. Hero confides in Pseudolus that he is in love with the lovely Philia, one of the courtesans in the House of Lycus (albeit still a virgin)."""
# doc = nlp(text)

# print(displacy.render(doc, style="ent"))


# from datetime import datetime as date



# N = str(date.now()).replace('.','_')
# print(N)
# import pathlib
# path = f"{str(pathlib.Path(__file__).parent.resolve().as_posix())}/text_files/testfile"

# file = open(path, "w") 
# file.write("Your text goes here") 
# file.close() 




import re
text = 'Facebook is an online social media and social networking service owned by American company Meta Platforms. Founded in 2004 by Mark Zuckerberg with fellow Harvard College students and roommates Eduardo Saverin, Andrew McCollum, Dustin Moskovitz, and Chris Hughes, its name comes from the facebook directories often given to American university students. Membership was initially limited to Harvard students, gradually expanding to other North American universities and, since 2006, anyone over 13 years old. As of 2020, Facebook claimed 2.8 billion monthly active users,[2] and ranked fourth in global internet usage.[6] It was the most downloaded mobile app of the 2010s.[7]'
match = re.findall(r'facebook', text,flags=re.IGNORECASE) 
print(match)
match = list(dict.fromkeys(match))
print(match)
for word in match:
    text = re.sub(word, f'<mark>{word}</mark>', text)


print(text)