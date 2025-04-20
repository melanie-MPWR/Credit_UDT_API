import random
from pprint import pprint
from typing import List, Dict, Any


# Account Factory class
class AccountFactory:

    def __init__(self, seed: int = None):
        """Initialize the factory with an optional random seed for reproducibility."""
        if seed is not None:
            random.seed(seed)

    @staticmethod
    def create_random_balance(include_limit=True) -> dict:
        """Create a random balance object"""
        current = round(random.uniform(100, 10000), 2)
        available = round(current * random.uniform(0.7, 1.0), 2) if random.random() > 0.1 else None

        balance_data = {
            'current': current,
            'available': available,
            'iso_currency_code': random.choice(['USD', 'EUR', 'GBP', 'CAD', 'JPY']),
            'unofficial_currency_code': None
        }

        # Add limit for credit accounts
        if include_limit:
            balance_data['limit'] = round(random.uniform(5000, 20000), 2)
        else:
            balance_data['limit'] = None

        return balance_data

    @staticmethod
    def generate_account(account_id=None) -> Dict[str, Any]:
        """Create a random account object"""
        account_types = {
            'depository': ['checking', 'savings', 'hsa', 'cd', 'money market'],
            'credit': ['credit card', 'line of credit'],
            'loan': ['mortgage', 'student', 'auto', 'personal'],
            'investment': ['brokerage', '401k', 'ira', 'roth'],
            'other': ['cash management', 'keogh', 'mutual fund', 'prepaid']
        }

        # Select random type and subtype
        acc_type = random.choice(list(account_types.keys()))
        acc_subtype = random.choice(account_types[acc_type])

        # Create random holder category
        holder_category = random.choice(['personal', 'business', None]) if random.random() > 0.3 else None

        # Determine if account should have a limit (credit accounts)
        include_limit = acc_type == 'credit'

        # Create balance object
        balance_data = AccountFactory.create_random_balance(include_limit)

        # Generate account_id if not provided
        if not account_id:
            account_id = f"acc_{random.randint(10000000, 99999999)}"

        # Create the account data
        account = {
            'account_id': account_id,
            'balances': balance_data,
            'holder_category': holder_category,
            'mask': f"{random.randint(1000, 9999)}",
            'name': f"{acc_subtype.title()} Account",
            'official_name': f"Official {acc_subtype.title()} Account" if random.random() > 0.5 else None,
            'subtype': acc_subtype,
            'type': acc_type
        }

        # Create the account object
        return account

    def create_accounts(self, count: int) -> List[Dict[str, Any]]:
        """Create multiple random accounts"""
        return [AccountFactory.generate_account() for _ in range(count)]



def generate_accounts(count: int, seed: int = None) -> List[Dict[str, Any]]:
    """
    Generate a specified number of random account objects.

    Args:
        count: Number of transactions to generate
        seed: Optional random seed for reproducibility

    Returns:
        List of transaction objects
    """
    factory = AccountFactory(seed)
    return factory.create_accounts(count)