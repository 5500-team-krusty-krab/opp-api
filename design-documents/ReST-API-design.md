# ReST API design

`POST /api/signup?email=&password=`
| Request Field | Field Type | Field Description |
| ------------- | ---------- | ----------------------------------- |
| email | String | user's email address |
| password | String | user's password |

sample response

```
{
    "email": "testuser@email.com",
    "success": true
}
```

Status codes:

- 200 / normal
- 460 / email address occupied
- 461 / invalid email format
- 462 / invalid password

`PUT /api/login?email=&password=`
| Request Field | Field Type | Field Description |
| ------------- | ---------- | ----------------------------------- |
| email | String | user's email address |
| password | String | user's password |

sample response

```
{
    "email": "testuser@email.com",
    "success": true,
    "access_token": "xxxxxxxxxx"
}
```

Status codes:

- 200 / normal
- 460 / incorrect email/password

`POST /api/purchase?ard_type=&card_number=&expiry_date&cvv=&name=&account_type&amount=`
| Request Field | Field Type | Field Description |
| ------------- | ---------- | ----------------------------------- |
| card_type | String | card type enum: credit/debit |
| card_number | String | card number |
| expiry_date | String | expiry month and expiry year |
| cvv | int | Card Verification Value |
| name | String | card holder's name|
| account_type | String | account type enum: debit/chequing |
| amount | int | amount to process in cents |

sample response

```
{
    "success": true,
    "card_type": "DEBIT",
    "card_number": "0000-0000-0000-0000",
    "amount": 9999 //$99.99
    "status": "processed"
}
```

Status codes:

- 200 / normal
- 401 / unauthorized access
- 460 / invalid card type
- 461 / invalid card number
- 462 / credit card validation failed
- 463 / debit card insufficient amount

`GET /api/balance?start=&end=`
| Request Field | Field Type | Field Description |
| ------------- | ---------- | ----------------------------------- |
| start | Date | start date (optional) |
| end | Date | end date (optional) |

sample response

```
{
    "balance": 9999 //$99.99
}
```

Status codes:

- 200 / normal
- 401 / unauthorized access
- 460 / invalid time period

`GET /api/transactions?start=&end=`
| Request Field | Field Type | Field Description |
| ------------- | ---------- | ----------------------------------- |
| start | Date | start date (optional) |
| end | Date | end date (optional) |

sample response

```
{
    "transactions": [
        {
            "date": "01/01/2023",
            "amount": 9999 //$99.99
            "card_type": "CREDIT",
            "card_number": "0000-0000-0000-0000"
        }
    ]
}
```

Status codes:

- 200 / normal
- 401 / unauthorized access
- 460 / invalid time period

`GET /api/accounts-receivables`

sample response

```
{
    "accounts_receivables": [
        {
            "date": "01/01/2023",
            "balance": 9999 //$99.99,
            "customer": "ABC company",
            "description": "cleaning service"
        }
    ]
}
```

Status codes:

- 200 / normal
- 401 / unauthorized access
