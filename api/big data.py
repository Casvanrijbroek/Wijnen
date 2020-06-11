import wijnen
import time
import ast

starttime = time.time()
file = "C:\\Users\\Lex\\PycharmProjects\\untitled20\\message (11).txt"
with open(file, "r") as bigdatafile:
    data = ast.literal_eval(bigdatafile.read())
testdata = wijnen.wijnen.Wijnen("coronakraft.online", "6969", "merlot").get_variations(data)
print({'filtered': len(testdata["filtered"]), 'not_found': len(testdata['not_found'])})

print(time.time()-starttime)