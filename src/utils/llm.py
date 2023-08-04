'''
===========================================
        Module: Open-source LLM Setup
===========================================
'''
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
from langchain.llms import CTransformers, HuggingFacePipeline
from load_Vars import *

def build_llm(llm_name):

    if llm_name == "LLAMA2":
        # Local CTransformers model
        llm = CTransformers(model=LLAMA2_MODEL_REPO_NAME,
                            model_file=LLAMA2_MODEL_BIN_FILE,
                            config={'max_new_tokens': int(LLAMA2_MAX_NEW_TOKENS),
                                    'temperature': int(LLAMA2_TEMPERATURE)}
                            )

        return llm
    elif llm_name == "LaMini-Flan-T5":
        #model and tokenizer loading
        tokenizer = AutoTokenizer.from_pretrained(LAMINI_MODEL_REPO_NAME)
        base_model = AutoModelForSeq2SeqLM.from_pretrained(checkpoint, device_map='auto', torch_dtype=torch.float32)

        pipe = pipeline(
            'text2text-generation',
            model = base_model,
            tokenizer = tokenizer,
            max_length = 512,
            do_sample=True,
            temperature = int(LAMINI_TEMPERATURE),
            top_p = 0.95
        )
        local_llm = HuggingFacePipeline(pipeline=pipe)
        
        return local_llm
    else:
        print("No model configuration found")

