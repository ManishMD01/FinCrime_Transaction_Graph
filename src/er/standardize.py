"""
Data Standardization Module
Parses, cleans, and normalizes customer profile fields.
"""

import re
from typing import Dict, Any, Optional
import pandas as pd
import jellyfish


class DataStandardizer:
    """Standardizes customer profile data for entity resolution."""
    
    def __init__(self):
        self.phone_pattern = re.compile(r'[^0-9+]')
        self.email_pattern = re.compile(r'[^a-z0-9@._-]')
        self.name_suffixes = {'jr', 'sr', 'ii', 'iii', 'iv', 'v', 'md', 'phd'}
        self.name_prefixes = {'mr', 'mrs', 'ms', 'miss', 'dr'}
    
    def standardize_name(self, name: str) -> Dict[str, str]:
        """Tokenize and normalize names."""
        if pd.isna(name) or name == '':
            return {
                'first_name': '',
                'last_name': '',
                'middle_name': '',
                'full_name_clean': '',
                'soundex': '',
                'metaphone': ''
            }
        
        # Convert to lowercase and remove extra whitespace
        name_clean = re.sub(r'\s+', ' ', str(name).lower().strip())
        
        # Remove punctuation
        name_clean = re.sub(r'[^\w\s]', ' ', name_clean)
        
        # Split into tokens
        tokens = [t for t in name_clean.split() if t]
        
        # Remove prefixes/suffixes
        tokens = [t for t in tokens if t not in self.name_prefixes and t not in self.name_suffixes]
        
        if not tokens:
            return {
                'first_name': '',
                'last_name': '',
                'middle_name': '',
                'full_name_clean': '',
                'soundex': '',
                'metaphone': ''
            }
        
        first_name = tokens[0]
        last_name = tokens[-1] if len(tokens) > 1 else ''
        middle_name = ' '.join(tokens[1:-1]) if len(tokens) > 2 else ''
        
        full_name_clean = ' '.join(tokens)
        
        # Generate phonetic codes
        try:
            soundex_code = jellyfish.soundex(full_name_clean)
        except:
            soundex_code = ''
        
        try:
            metaphone_code = jellyfish.metaphone(full_name_clean)
        except:
            metaphone_code = ''
        
        return {
            'first_name': first_name,
            'last_name': last_name,
            'middle_name': middle_name,
            'full_name_clean': full_name_clean,
            'soundex': soundex_code,
            'metaphone': metaphone_code
        }
    
    def standardize_address(self, address: str) -> Dict[str, str]:
        """Standardize addresses using common abbreviations."""
        if pd.isna(address) or address == '':
            return {
                'address_clean': '',
                'street_number': '',
                'street_name': '',
                'street_type': '',
                'unit': ''
            }
        
        addr_clean = str(address).lower().strip()
        addr_clean = re.sub(r'\s+', ' ', addr_clean)
        
        # Standardize common abbreviations
        replacements = {
            r'\bstreet\b': 'st',
            r'\bavenue\b': 'ave',
            r'\bboulevard\b': 'blvd',
            r'\bdrive\b': 'dr',
            r'\blane\b': 'ln',
            r'\broad\b': 'rd',
            r'\bcourt\b': 'ct',
            r'\bplace\b': 'pl',
            r'\bsuite\b': 'ste',
            r'\bapartment\b': 'apt',
            r'\bbuilding\b': 'bldg',
            r'\bnorth\b': 'n',
            r'\bsouth\b': 's',
            r'\beast\b': 'e',
            r'\bwest\b': 'w',
        }
        
        for pattern, repl in replacements.items():
            addr_clean = re.sub(pattern, repl, addr_clean)
        
        # Extract components
        tokens = addr_clean.split()
        street_number = tokens[0] if tokens and tokens[0].isdigit() else ''
        street_type = ''
        for t in tokens:
            if t in ['st', 'ave', 'blvd', 'dr', 'ln', 'rd', 'ct', 'pl']:
                street_type = t
                break
        
        # Street name (between number and type, simplified)
        street_name = ' '.join([t for t in tokens[1:-1] if t not in ['st', 'ave', 'blvd', 'dr', 'ln', 'rd', 'ct', 'pl', 'apt', 'ste', '#']])
        
        return {
            'address_clean': addr_clean,
            'street_number': street_number,
            'street_name': street_name,
            'street_type': street_type,
            'unit': ''
        }
    
    def standardize_phone(self, phone: str) -> str:
        """Standardize phone numbers to E.164-like format."""
        if pd.isna(phone) or phone == '':
            return ''
        
        # Remove all non-digit characters except +
        cleaned = self.phone_pattern.sub('', str(phone))
        # Remove leading + if present, keep digits
        cleaned = cleaned.lstrip('+')
        
        # Return last 10 digits for US numbers (or full if different length)
        if len(cleaned) >= 10:
            return cleaned[-10:]
        return cleaned
    
    def standardize_email(self, email: str) -> str:
        """Standardize email addresses."""
        if pd.isna(email) or email == '':
            return ''
        
        email_clean = str(email).lower().strip()
        # Remove dots from local part for gmail-like normalization (optional)
        if '@' in email_clean:
            local, domain = email_clean.split('@')
            # Common normalization - remove dots from gmail
            if domain in ['gmail.com', 'googlemail.com']:
                local = local.replace('.', '')
                domain = 'gmail.com'
            email_clean = f"{local}@{domain}"
        
        return email_clean
    
    def standardize_ssn(self, ssn: str) -> str:
        """Standardize SSN/National ID."""
        if pd.isna(ssn) or ssn == '':
            return ''
        # Remove all non-digit characters
        cleaned = re.sub(r'[^0-9]', '', str(ssn))
        return cleaned
    
    def standardize_all(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply all standardizations to a customer dataframe."""
        df_std = df.copy()
        
        # Standardize names
        name_results = df_std['name'].apply(self.standardize_name)
        df_std['first_name'] = [r['first_name'] for r in name_results]
        df_std['last_name'] = [r['last_name'] for r in name_results]
        df_std['full_name_clean'] = [r['full_name_clean'] for r in name_results]
        df_std['soundex'] = [r['soundex'] for r in name_results]
        df_std['metaphone'] = [r['metaphone'] for r in name_results]
        
        # Standardize addresses
        addr_results = df_std['address'].apply(self.standardize_address)
        df_std['address_clean'] = [r['address_clean'] for r in addr_results]
        df_std['street_number'] = [r['street_number'] for r in addr_results]
        df_std['street_name'] = [r['street_name'] for r in addr_results]
        
        # Standardize other fields
        df_std['phone_std'] = df_std['phone'].apply(self.standardize_phone)
        df_std['email_std'] = df_std['email'].apply(self.standardize_email)
        df_std['ssn_std'] = df_std['ssn'].apply(self.standardize_ssn)
        
        # Standardize zip code
        df_std['zip_std'] = df_std['zip'].astype(str).str.extract(r'(\d{5})')[0].fillna('')
        
        return df_std
