import numpy as np
from PIL import Image
from wordcloud import WordCloud, STOPWORDS


WC_IMAGE_PATH = 'linkbook/media/wc.png'
WC_MASK_PATH = 'linkbook/media/cloud.png'

def wcloud_generator(tags):

	mask = np.array(Image.open(WC_MASK_PATH))
	words = {}
	for idx, tag in enumerate(tags[::-1]):
		words[tag] = idx
	
	wc = WordCloud( background_color="white", 
					max_words=30,
					mask = mask, 
					width=1800, 
					height=1400, 
					mode="RGB")
	wc.generate_from_frequencies(words)
	wc.to_file(WC_IMAGE_PATH)
	


'''
(self, font_path=None, width=400, height=200, margin=2,
		 ranks_only=None, prefer_horizontal=0.9, mask=None, scale=1,
		 color_func=random_color_func, max_words=200, min_font_size=4,
		 stopwords=None, random_state=None, background_color='black',
		 max_font_size=None, font_step=1, mode="RGB", relative_scaling=0, regexp=None)
'''
