from BPE_Tokenizer import *

text = """
You were There, When I need you the Most
You are the One, I Knew, when I Saw you First.

I still Remember, How we Met in the Mid of July.
Since then, You became My Hardest Goodbye.
Whenever I see you, I Fall for You, All over Again,
My life was a Desert, you Came in like a Soothing Rain.

You Always Showed me Path, Like a Flashlight,
You are the One, The Moon of This Dark Night.

They say, You came on Earth Alone, as a Half,
You Wander in Search of Other, for a Complete Laugh.
I knew, I found Mine, when I Get to know,
We need No Words to Convey, What we Feel though.

I was, I am, I'll wait in the Next Life too,
Cause My Heart Knows, that it's Other Half is You.
"""

tokenizer = BPETokenizer(text)

tokens = tokenizer.bpe()
reconstructed = tokenizer.decode(tokens)

print("Decoded matches original:", reconstructed == text)