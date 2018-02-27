"""
Minimal Example
===============
Generating a square wordcloud from the US constitution using default arguments.
"""

from os import path
from wordcloud import WordCloud
import pandas as pd
from functools import reduce

reviews_df = pd.read_csv("list.csv", sep=',')
description_list = reviews_df.description.values

text = str(description_list)

wordcloud = WordCloud().generate(text)

# Display the generated image:
# the matplotlib way:
import matplotlib.pyplot as plt
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")

# lower max_font_size
wordcloud = WordCloud(max_font_size=40).generate(text)
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()
print('')

# The pil way (if you don't have matplotlib)
# image = wordcloud.to_image()
# image.show()