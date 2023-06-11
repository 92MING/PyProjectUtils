# -*- coding: utf-8 -*-
'''常用的AI工具。使用前，需先使用"addAPIKey"添加密鑰。可添加多個，並在exceed quota等情況時自動切換。'''

import tiktoken
import numpy as np
from openai.embeddings_utils import cosine_similarity as _cosine_similarity
from openai.error import *
from ..utils.GlobalValueUtils import *
from typing import Iterable, Union

_enc = GetOrAddGlobalValue("_OPENAI_ENCODING", tiktoken.get_encoding('cl100k_base'))
_apiKeys:set = GetOrAddGlobalValue("_OPENAI_API_KEYS", set())

class NoAPIKeyError(Exception):
    pass

def errorHandler(func):
    '''
    處理OpenAI的error，如果是exceed quota，則自動切換API密鑰。
    '''
    def wrapper(*args, **kwargs):
        while len(_apiKeys) > 0:
            try:
                return func(*args, **kwargs)
            except AuthenticationError:
                # wrong api key
                _apiKeys.pop()
            except RateLimitError:
                # exceed quota
                _apiKeys.pop()
            except OpenAIError:
                # other error, try again
                pass
        raise NoAPIKeyError
    return wrapper

def addAPIKey(apiKey:Union[str, Iterable[str]]):
    '''
    添加API密鑰到一個全局的set。可添加多個，並在exceed quota等情況時自動切換。
    調用OpenAI的function都必須添加api。
    '''
    apikeys = apiKey if isinstance(apiKey, Iterable) else [apiKey]
    global _apiKeys
    for apiKey in apikeys:
        _apiKeys.add(apiKey)

def get_tokens(text:str)->list:
    '''Get tokens from text'''
    return _enc.encode(text)

def count_tokens(text:str)->int:
    '''Count tokens from text'''
    return len(get_tokens(text))

@errorHandler
def get_embedding_vector(text:str)->np.ndarray:
    '''Get embedding vector from text'''
    v = openai.Embedding.create(input=[text], model='text-embedding-ada-002')['data'][0]['embedding']
    return np.array(v)

@errorHandler
def get_completion(prompt, temperature=1, frequency_penalty=0, presence_penalty=0)->str:
    '''
    :param prompt: prompt text
    :param temperature: higher->more random, lower->more deterministic [0, 2]
    :param frequency_penalty: higher->less repetition, lower->more repetition [-2, 2]
    :param presence_penalty: higher->encourage model to talk about new topics, lower->encourage model to repeat itself [-2, 2]
    :return:
    '''
    return openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=temperature,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
    )['choices'][0]['text']

@errorHandler
def get_chat(messages, roles=None, temperature=0.5, frequency_penalty=0, presence_penalty=0)->str:
    '''
    :param messages: list of messages(if only 1, then can be str), e.g. ["Hello, who are you?", "I am doing great. How about you?"]
    :param roles: list of roles(if only 1, then can be str), e.g. ["system", "assistant"], if None, then all roles are "user"
    :param temperature: higher->more random, lower->more deterministic [0, 2]
    :param frequency_penalty: higher->less repetition, lower->more repetition [-2, 2]
    :param presence_penalty: higher->encourage model to talk about new topics, lower->encourage model to repeat itself [-2, 2]
    '''
    if isinstance(roles, str):
        roles = [roles]
    if isinstance(messages, str):
        messages = [messages]
    if roles is None:
        roles = ['user'] * len(messages)
    elif len(roles) != len(messages):
        raise ValueError('roles and messages must have the same length')
    try:
        return openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": role, "content": message} for role, message in zip(roles, messages)],
            temperature=temperature,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
        )['choices'][0]['message']['content']
    except AuthenticationError:
        print('AuthenticationError: No API key provided. Please use "addAPIKey" to add an API key.')

def normalize(vector):
    return vector / np.linalg.norm(vector)

def cosine_similarity(v1, v2):
    '''調用openai.embeddings_utils.cosine_similarity'''
    return _cosine_similarity(v1, v2)

__all__ = ['addAPIKey', 'get_tokens', 'count_tokens', 'get_embedding_vector', 'get_completion', 'get_chat', 'normalize', 'cosine_similarity']
