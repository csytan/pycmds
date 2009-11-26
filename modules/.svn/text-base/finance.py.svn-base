import urllib2
import pycmds

_RATES = {}

class Currency(str):
    currencies = {
        'Maltese Lira (MTL)': 'MTL', 
        'Ukraine Hryvnia (UAH)': 'UAH', 
        'Rwanda Franc (RWF)': 'RWF', 
        'Mauritania Ougulya (MRO)': 'MRO', 
        'Ugandan Shilling (UGX)': 'UGX', 
        'Swedish Krona (SEK)': 'SEK', 
        'Palladium Ounces (XPD)': 'XPD', 
        'Moroccan Dirham (MAD)': 'MAD', 
        'Mauritius Rupee (MUR)': 'MUR', 
        'Lesotho Loti (LSL)': 'LSL', 
        'Lebanese Pound (LBP)': 'LBP', 
        'Bermuda Dollar (BMD)': 'BMD', 
        'Cambodia Riel (KHR)': 'KHR', 
        'Singapore Dollar (SGD)': 'SGD', 
        'Aluminium Ounces (XAL)': 'XAL', 
        'New Turkish Lira (TRY)': 'TRY', 
        'Latvian Lat (LVL)': 'LVL', 
        'Malaysian Ringgit (MYR)': 'MYR', 
        'Macau Pataca (MOP)': 'MOP', 
        'Thai Baht (THB)': 'THB', 
        'Liberian Dollar (LRD)': 'LRD', 
        'Paraguayan Guarani (PYG)': 'PYG', 
        'Chinese Yuan (CNY)': 'CNY', 
        'Panama Balboa (PAB)': 'PAB', 
        'Haiti Gourde (HTG)': 'HTG', 
        'Iraqi Dinar (IQD)': 'IQD', 
        'Vanuatu Vatu (VUV)': 'VUV', 
        'Swiss Franc (CHF)': 'CHF', 
        'Argentine Peso (ARS)': 'ARS', 
        'Guatemala Quetzal (GTQ)': 'GTQ', 
        'Japanese Yen (JPY)': 'JPY', 
        'Hungarian Forint (HUF)': 'HUF', 
        'Vietnam Dong (VND)': 'VND', 
        'Bahraini Dinar (BHD)': 'BHD', 
        'Copper Pounds (XCP)': 'XCP', 
        'Zambian Kwacha (ZMK)': 'ZMK', 
        'Aruba Florin (AWG)': 'AWG', 
        'Barbados Dollar (BBD)': 'BBD', 
        'Estonian Kroon (EEK)': 'EEK', 
        'Bolivian Boliviano (BOB)': 'BOB', 
        'Libyan Dinar (LYD)': 'LYD', 
        'Dijibouti Franc (DJF)': 'DJF',
        'Philippine Peso (PHP)': 'PHP', 
        'Samoa Tala (WST)': 'WST', 
        'Omani Rial (OMR)': 'OMR', 
        'Cuban Peso (CUP)': 'CUP', 
        'Mongolian Tugrik (MNT)': 'MNT', 
        'Platinum Ounces (XPT)': 'XPT', 
        'Danish Krone (DKK)': 'DKK', 
        'Tunisian Dinar (TND)': 'TND', 
        'Gambian Dalasi (GMD)': 'GMD', 
        'U.S. Dollar (USD)': 'USD', 
        'Hong Kong Dollar (HKD)': 'HKD', 
        'Gibraltar Pound (GIP)': 'GIP', 
        'Brazilian Real (BRL)': 'BRL', 
        'Tanzanian Shilling (TZS)': 'TZS', 
        'Guyana Dollar (GYD)': 'GYD', 
        'Belarus Ruble (BYR)': 'BYR', 
        'Swaziland Lilageni (SZL)': 'SZL', 
        'Bangladesh Taka (BDT)': 'BDT', 
        'Costa Rica Colon (CRC)': 'CRC', 
        'Malawi Kwacha (MWK)': 'MWK', 
        'Algerian Dinar (DZD)': 'DZD', 
        'Kenyan Shilling (KES)': 'KES', 
        'Venezuelan Bolivar (VEB)': 'VEB', 
        'Namibian Dollar (NAD)': 'NAD', 
        'Bulgarian Lev (BGN)': 'BGN', 
        'Myanmar Kyat (MMK)': 'MMK', 
        'Uruguayan New Peso (UYU)': 'UYU', 
        'Colombian Peso (COP)': 'COP', 
        'Gold Ounces (XAU)': 'XAU', 
        'Croatian Kuna (HRK)': 'HRK', 
        'Russian Rouble (RUB)': 'RUB', 
        'East Caribbean Dollar (XCD)': 'XCD', 
        'Albanian Lek (ALL)': 'ALL', 
        'Slovak Koruna (SKK)': 'SKK', 
        'Cyprus Pound (CYP)': 'CYP', 
        'Ethiopian Birr (ETB)': 'ETB', 
        'Yemen Riyal (YER)': 'YER', 
        'Sierra Leone Leone (SLL)': 'SLL', 
        'Guinea Franc (GNF)': 'GNF', 
        'Fiji Dollar (FJD)': 'FJD', 
        'Israeli Shekel (ILS)': 'ILS', 
        'Nigerian Naira (NGN)': 'NGN', 
        'Zimbabwe Dollar (ZWD)': 'ZWD', 
        'Chilean Peso (CLP)': 'CLP', 
        'Brunei Dollar (BND)': 'BND', 
        'Taiwan Dollar (TWD)': 'TWD', 
        'Macedonian Denar (MKD)': 'MKD', 
        'Silver Ounces (XAG)': 'XAG', 
        'Neth Antilles Guilder (ANG)': 'ANG', 
        'Syrian Pound (SYP)': 'SYP', 
        'Dominican Peso (DOP)': 'DOP', 
        'Falkland Islands Pound (FKP)': 'FKP', 
        'Polish Zloty (PLN)': 'PLN', 
        'Indonesian Rupiah (IDR)': 'IDR', 
        'Honduras Lempira (HNL)': 'HNL', 
        'Romanian New Leu (RON)': 'RON', 
        'Lithuanian Lita (LTL)': 'LTL', 
        'Egyptian Pound (EGP)': 'EGP', 
        'Nepalese Rupee (NPR)': 'NPR', 
        'British Pound (GBP)': 'GBP', 
        'Peruvian Nuevo Sol (PEN)': 'PEN', 
        'Iran Rial (IRR)': 'IRR', 
        'Papua New Guinea Kina (PGK)': 'PGK', 
        'Qatar Rial (QAR)': 'QAR', 
        "Tonga Pa'anga (TOP)": 'TOP', 
        'Euro (EUR)': 'EUR', 
        'Pakistani Rupee (PKR)': 'PKR', 
        'Ecuador Sucre (ECS)': 'ECS', 
        'St Helena Pound (SHP)': 'SHP', 
        'South African Rand (ZAR)': 'ZAR', 
        'Botswana Pula (BWP)': 'BWP', 
        'Kuwaiti Dinar (KWD)': 'KWD', 
        'Bhutan Ngultrum (BTN)': 'BTN', 
        'Cape Verde Escudo (CVE)': 'CVE', 
        'CFA Franc (BEAC) (XAF)': 'XAF', 
        'Saudi Arabian Riyal (SAR)': 'SAR', 
        'New Zealand Dollar (NZD)': 'NZD', 
        'Norwegian Krone (NOK)': 'NOK', 
        'Solomon Islands Dollar (SBD)': 'SBD', 
        'Bahamian Dollar (BSD)': 'BSD', 
        'Seychelles Rupee (SCR)': 'SCR', 
        'Australian Dollar (AUD)': 'AUD', 
        'Eritrea Nakfa (ERN)': 'ERN', 
        'Iceland Krona (ISK)': 'ISK', 
        'Comoros Franc (KMF)': 'KMF', 
        'Nicaragua Cordoba (NIO)': 'NIO', 
        'Sri Lanka Rupee (LKR)': 'LKR', 
        'Lao Kip (LAK)': 'LAK', 
        'Mexican Peso (MXN)': 'MXN', 
        'Jamaican Dollar (JMD)': 'JMD', 
        'Kazakhstan Tenge (KZT)': 'KZT', 
        'Slovenian Tolar (SIT)': 'SIT', 
        'Indian Rupee (INR)': 'INR', 
        'Sudanese Dinar (SDD)': 'SDD', 
        'UAE Dirham (AED)': 'AED', 
        'Czech Koruna (CZK)': 'CZK', 
        'El Salvador Colon (SVC)': 'SVC', 
        'Canadian Dollar (CAD)': 'CAD', 
        'Korean Won (KRW)': 'KRW', 
        'Moldovan Leu (MDL)': 'MDL', 
        'North Korean Won (KPW)': 'KPW', 
        'Sao Tome Dobra (STD)': 'STD', 
        'Ghanian Cedi (GHC)': 'GHC', 
        'Belize Dollar (BZD)': 'BZD', 
        'Trinidad&amp;Tobago Dollar (TTD)': 'TTD', 
        'Maldives Rufiyaa (MVR)': 'MVR', 
        'Pacific Franc (XPF)': 'XPF', 
        'CFA Franc (BCEAO) (XOF)': 'XOF', 
        'Burundi Franc (BIF)': 'BIF', 
        'Somali Shilling (SOS)': 'SOS', 
        'Cayman Islands Dollar (KYD)': 'KYD', 
        'Jordanian Dinar (JOD)': 'JOD'
    }
    
    def __init__(self, string):
        if string in self.currencies:
            self.name = string
            self.symbol = self.currencies[string]
            return
            
        string = string.lower()
        for currency in self.currencies:
            if string == currency.lower():
                self.name = currency
                self.symbol = self.currencies[currency]
                return
            
        raise TypeError
    
    @classmethod
    def suggest(cls, prefix):
        suggestions = []
        for currency in cls.currencies:
            if currency.lower().startswith(prefix):
                suggestions.append(currency)
        return suggestions

def get_rate(symbols):
    rate = _RATES.get(symbols)
    if rate:
        return rate
        
    csv = urllib2.urlopen("http://download.finance.yahoo.com/d/quotes.csv?s=" + \
            symbols + "=X&f=sl1d1t1ba&e=.csv").read()
    rate = float(csv.split(',')[1])
    _RATES[symbols] = rate
    return rate

@pycmds.cmd("currency convert [amount] from [currency A] to [currency B]", float, Currency, Currency)
def convert(amount, currencyA, currencyB):
    symbols = currencyA.symbol + currencyB.symbol
    rate = get_rate(symbols)
    return str(amount * rate) + ' ' + currencyB.name + '<br>' + \
            'Exchange rates provided by <a href="http://finance.yahoo.com/">Yahoo! Finance</a>.'