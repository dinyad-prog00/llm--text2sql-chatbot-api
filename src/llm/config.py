from langchain_core.prompts import PromptTemplate


def get_device_map(nb_gpu_layer):

    device_map = {
        'model.embed_tokens': 0,
        'model.norm': 'cpu',
        'lm_head': 'cpu'
    }
    for l in range(32):
        if l < nb_gpu_layer:
            device_map[f"model.layers.{l}"] = 0
        else:
            device_map[f"model.layers.{l}"] = 'cpu'

    return device_map



