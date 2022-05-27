#pip install transformers
#pip install torch
#pip install sentence-splitter

import os
import torch
from transformers import PegasusForConditionalGeneration, PegasusTokenizer
from sentence_splitter import SentenceSplitter
from termcolor import colored



class PegasusParaphraser:
    def __init__(self, num_beams=10):
        self.module_dir = os.path.dirname(__file__)

        if(torch.cuda.is_available()):
            self.device = torch.device("cuda:0")
        else:
            self.device = torch.device("cpu:0")

        # Pegasus Tokenizer & Model for Paraphrasing
        print(colored("INFO", "green"),":\t  Loading for Paraphrasing Model.")
        paraphraser_model_name = "tuner007/pegasus_paraphrase"
        self.tokenizer = PegasusTokenizer.from_pretrained(paraphraser_model_name)
        self.model = PegasusForConditionalGeneration.from_pretrained(paraphraser_model_name).to(self.device)
        self.num_beams = num_beams
        self.splitter = SentenceSplitter(language='en')


    def paraphrase_text(self, text):
        sentence_list = self.splitter.split(text)
        batch = self.tokenizer(sentence_list,truncation=True, padding='longest', max_length=100, return_tensors="pt").to(self.device)
        translated = self.model.generate(**batch, max_length=60, num_beams=self.num_beams, num_return_sequences=1, temperature=1.5)
        tgt_text = self.tokenizer.batch_decode(translated, skip_special_tokens=True)

        paraphrased_text = " ".join(tgt_text)
        return paraphrased_text

