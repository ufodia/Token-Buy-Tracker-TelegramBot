from json import JSONDecodeError, loads
from markupsafe import string
from requests import get as getRequest
from pydantic import BaseModel, ValidationError




class Transaction(BaseModel):
    """
    group_helper configuration class
    """
    id: str
    date: int
    native_token_decimals: int
    received: list
    sent: list


class UnmarshalApi():
    def __init__(self, pancakeswap_address, contract, chain, api_key) -> None:
        self.pancakeswap_address = pancakeswap_address
        self.contract = contract
        self.chain = chain
        self.url = f"https://api.unmarshal.com/v2/{chain}/address/{self.pancakeswap_address}/transactions?page=0&pageSize=1&contract={contract}&auth_key={api_key}"

    def getTransactions(self):
        resp = getRequest(self.url)
        try:
            resp = resp.json()
            last_transaction = resp['transactions']
            if last_transaction:
                return Transaction(**dict(last_transaction[0]))
            else:
                return None
        except JSONDecodeError:
            return None 
