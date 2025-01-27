from FlagEmbedding import BGEM3FlagModel
import pyarrow as pa
import numpy as np

model = BGEM3FlagModel('BAAI/bge-m3',  use_fp16=True, device='cuda') 

def embed(document: str):
    """Returns dense vector embedding of a document"""
    return model.encode(document)["dense_vecs"]