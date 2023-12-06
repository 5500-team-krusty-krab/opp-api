# validate.py: Module for validating credit or debit card numbers using an external API.

import requests
from typing import Tuple

VALIDATION_URL = "https://c3jkkrjnzlvl5lxof74vldwug40pxsqo.lambda-url.us-west-2.on.aws"

def validate_card(card_number: str, card_type: str) -> Tuple[bool, str]:
    """
    Validate a credit or debit card number using a third-party API.
    
    :param card_number: The card number to validate.
    :param card_type: The type of the card (either 'credit' or 'debit').
    :return: A tuple containing a boolean indicating success and a message.
    """
    response = requests.post(
        VALIDATION_URL,
        json={"card_number": card_number},
        headers={'Content-Type': 'application/json'},
        timeout=10  # Timeout set to 10 seconds
    )

    if response.status_code != 200:
        return False, f"Failed to validate card: {response.text}"

    data = response.json()
    
    if not data.get('success'):
        return False, data.get('msg', 'Card validation failed')

    if card_type == 'debit':
        return True, 'Successfully processed'
    if card_type == 'credit':
        return True, 'It is into pending status'

    return False, 'Invalid card type'

