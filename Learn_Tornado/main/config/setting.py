import json
from ..src.code.utils.constants import Constants

from ..src.code.services.authorization import TokenDetail

def read_configuration():
    config_file = Constants.Config.LOCATION+'\\'+Constants.Config.FILE_NAME
    print(f'\n\nReading configuration from {config_file} ...')

    with open(config_file, 'r') as file:
        data = json.load(file)

    return data


def get_token_detail(config):
    token_key = Constants.Config.Key.TOKEN
    Token = Constants.Config.Token
    
    if token_key in config:
        print('\n\n---------- Getting token details ----------')
        token = config[token_key]
        token_detail = TokenDetail

        if Token.PRIVATE_KEY in token:
            token_detail.private_key = token[Token.PRIVATE_KEY]
        else:
            raise ImportError(f'Configuration not found for token private key')
        
        if Token.EXPIRE_DURATION in token:
            token_detail.expire_duration = token[Token.EXPIRE_DURATION]
        else:
            print(f'Configuration not found for token expire duration -> Putting {Token.DEFAULT_EXPIRE_DURATION} hours as default')
            token_detail.expire_duration = Token.DEFAULT_EXPIRE_DURATION
        
        if Token.ALGORITHM in token:
            token_detail.algorithm = token[Token.ALGORITHM]
        else:
            print(f'Configuration not found for token algorithm -> Putting {Token.DEFAULT_ALGORITHM} as default')
            token_detail.algorithm = Token.DEFAULT_ALGORITHM
    
        return token_detail
    else:
        raise ConnectionError(f'Configuration not found for token generation')