IMG_PROMPT_10 = """
I am sending you an image. This image was downloaded from mentioned article. Check if it can help you anwer the questions.
Description to this image is: {description}
"""


MP3_PROMPT_10 = """
I am sending transcription form audio file found on article. Check if it can help you anwer the questions. It was found in the article
near \"rafal_dyktafon.mp3\" text. 
The transcription is: {transcription}
"""

CONTENT_PROMPT_10 = """
I am sending you the content of the article. Check if it can help you anwer the questions.
The content of the artivle: {content}
"""

GENERAL_PROMPT_10 = """
I've sent you transcription from audio file, image and content of the article. Check if it can help you answer the questions.
Answer the questions based on the information provided. 


As result I need python dict with question id as key and YOUR ANSWER as value. Send me only the dictionary. Your result will be input to method dict() in python. It must fit. DOn't use \"```\" in your answer.
As question I will put the json, where keys are questions IDs and values are the questions

Questions: {questions}.

If you can't find answer in the provided information, try to use your knowledge to find it. There are always some hints in the text or in the pictures.
Remember to analyze the content of the article, transcription and the image.
"""