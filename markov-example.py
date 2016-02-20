from markov import MarkovTextGenerator

with open('standup.txt', 'r') as f:
    s = ''.join(f.readlines())

sources = ['standup.txt', 'lyrics.txt']

m = MarkovTextGenerator()
# Usage 1 -> single text
#m.train(s)
# Usage 2 -> list of filenames
m.train(sources)
print(m.generate_text("How can I", 60))
