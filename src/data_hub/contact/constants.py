import os

item_attributes = [
    {"FieldName": "USASLINES", "FieldValue": 3},
    {"FieldName": "USAS1CO", "FieldValue": 3719},
    {"FieldName": "USAS1PCA", "FieldValue": 19001},
    {"FieldName": "USAS1TCODE", "FieldValue": 195},
    {"FieldName": "USAS2CO", "FieldValue": 3879},
    {"FieldName": "USAS2PCA", "FieldValue": "07768"},
    {"FieldName": "USAS2TCODE", "FieldValue": 179},
    {"FieldName": "USAS3CO", "FieldValue": 7219},
    {"FieldName": "USAS3TCODE", "FieldValue": 265},
    {"FieldName": "USAS3PCA", "FieldValue": "07768"},
]

payload_valid_test = {
    "accountid": os.environ.get("FISERV_DEV_ACCOUNT_ID"),
    "companycode": os.environ.get("FISERV_COMPANY_CODE"),
    "currencycode": "USD",
    "customerid": os.environ.get("FISERV_CUSTOMER_ID"),
    "userid": os.environ.get("FISERV_USER_ID"),
    "savepaymentmethod": "N",
    "saveatcustomer": "N",
    "displaycardssavedatcustomer": "N",
    "redirecturl": "https://example.com/checkout/confirm",
    "cancelredirecturl": "https://example.com/checkout/cancel",
    "orderid": "1234",
    "reference": "UPI",
    "purchaseorder": "1234",
    "type": "C",
    "transactionType": "S",
    "transactionamount": 11.00,
    "paymentmethod": "CC",
    "cof": "C",
    "cofscheduled": "N",
    "ecomind": "E",
    "customer": {
        "customername": "Test",
        "addressline1": "123 Main St",
        "addressline2": "",
        "city": "Houston",
        "state": "TX",
        "zipcode": "77070",
        "country": "US",
        "phone": "713-111-9999",
        "email": "test@twdb.texas.gov"
    },
    "payments": [
        {
            "mode": "CC",
            "merchantid": os.environ.get("FISERV_MERCHANT_ID")
        }
    ],
    "level3": [
        {
            "linenumber": "1.000",
            "productcode": "Orange001",
            "taxrate": "0",
            "quantity": "1",
            "itemdescriptor": "Orange",
            "unitcost": "3.00",
            "lineitemtotal": "3.00",
            "taxamount": "0",
            "commoditycode": "",
            "unitofmeasure": "EA"
        },
        {
            "linenumber": "2.000",
            "productcode": "Green001",
            "taxrate": "0",
            "quantity": "1",
            "itemdescriptor": "Green",
            "unitcost": "7.00",
            "lineitemtotal": "7.00",
            "taxamount": "0",
            "commoditycode": "",
            "unitofmeasure": "EA"
        },
        {
            "linenumber": "3.000",
            "productcode": "FEE",
            "taxrate": "0",
            "quantity": "1",
            "itemdescriptor": " fee**",
            "unitcost": "1.00",
            "lineitemtotal": "1.00",
            "taxamount": "0",
            "commoditycode": "",
            "unitofmeasure": "EA"
        }
    ]
}
 