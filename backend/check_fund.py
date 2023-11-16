import requests
from typing import Tuple

CHECK_FUNDS_AND_FRAUD_URL = "https://223didiouo3hh4krxhm4n4gv7y0pfzxk.lambda-url.us-west-2.on.aws"

def validate_card(card_number: str, card_type: str, amount: float) -> Tuple[bool, str]:
    """
    Validate a credit or debit card number using a third-party API for checking funds and fraud.
    
    :param card_number: The card number to validate.
    :param card_type: The type of the card (either 'credit' or 'debit').
    :param amount: The transaction amount for fund validation.
    :return: A tuple containing a boolean indicating success and a message.
    """
    response = requests.post(
        CHECK_FUNDS_AND_FRAUD_URL,
        json={"card_number": card_number, "amt": amount},
        headers={'Content-Type': 'application/json'}
    )

    if response.status_code != 200:
        return False, f"Failed to validate card: {response.text}"

    data = response.json()

    if data.get("success") != "true":
        return False, data.get('msg', 'card number has sufficient funds and is not fradulent')

    if card_type == 'debit':
        return True, 'Successfully processed'
    elif card_type == 'credit':
        return True, 'Transaction is in pending status'
    else:
        return False, 'Invalid card type'
