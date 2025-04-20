import uuid
import random
import datetime
from typing import List, Dict, Any


class TransactionFactory:
    """Factory for generating random transaction objects similar to financial API data."""

    # Lists of sample data for generating realistic transactions
    MERCHANTS = [
        {"name": "Uber", "website": "uber.com", "logo_url": "https://plaid-merchant-logos.plaid.com/uber_1060.png",
         "entity_id": "eyg8o776k0QmNgVpAmaQj4WgzW9Qzo6O51gdd"},
        {"name": "Lyft", "website": "lyft.com", "logo_url": "https://plaid-merchant-logos.plaid.com/lyft_1234.png",
         "entity_id": "jkl8o776k0QmNgVpAmaQj4WgzW9Qzo6O51pqr"},
        {"name": "Amazon", "website": "amazon.com",
         "logo_url": "https://plaid-merchant-logos.plaid.com/amazon_2345.png",
         "entity_id": "abc8o776k0QmNgVpAmaQj4WgzW9Qzo6O51def"},
        {"name": "Walmart", "website": "walmart.com",
         "logo_url": "https://plaid-merchant-logos.plaid.com/walmart_3456.png",
         "entity_id": "ghi8o776k0QmNgVpAmaQj4WgzW9Qzo6O51jkl"},
        {"name": "Target", "website": "target.com",
         "logo_url": "https://plaid-merchant-logos.plaid.com/target_4567.png",
         "entity_id": "mno8o776k0QmNgVpAmaQj4WgzW9Qzo6O51stu"},
        {"name": "Starbucks", "website": "starbucks.com",
         "logo_url": "https://plaid-merchant-logos.plaid.com/starbucks_5678.png",
         "entity_id": "vwx8o776k0QmNgVpAmaQj4WgzW9Qzo6O51yza"},
        {"name": "Netflix", "website": "netflix.com",
         "logo_url": "https://plaid-merchant-logos.plaid.com/netflix_6789.png",
         "entity_id": "bcd8o776k0QmNgVpAmaQj4WgzW9Qzo6O51efg"},
        {"name": "Spotify", "website": "spotify.com",
         "logo_url": "https://plaid-merchant-logos.plaid.com/spotify_7890.png",
         "entity_id": "hij8o776k0QmNgVpAmaQj4WgzW9Qzo6O51klm"},
    ]

    CATEGORIES = [
        {"category": ["Travel", "Taxi"], "category_id": "22016000",
         "pf_category": {"primary": "TRANSPORTATION", "detailed": "TRANSPORTATION_TAXIS_AND_RIDE_SHARES",
                         "icon_url": "https://plaid-category-icons.plaid.com/PFC_TRANSPORTATION.png"}},
        {"category": ["Food and Drink", "Restaurants"], "category_id": "13005000",
         "pf_category": {"primary": "FOOD_AND_DRINK", "detailed": "FOOD_AND_DRINK_RESTAURANTS",
                         "icon_url": "https://plaid-category-icons.plaid.com/PFC_FOOD_AND_DRINK.png"}},
        {"category": ["Shops", "Online"], "category_id": "19025000",
         "pf_category": {"primary": "SHOPPING", "detailed": "SHOPPING_ONLINE_STORES",
                         "icon_url": "https://plaid-category-icons.plaid.com/PFC_SHOPPING.png"}},
        {"category": ["Shops", "Retail"], "category_id": "19021000",
         "pf_category": {"primary": "SHOPPING", "detailed": "SHOPPING_RETAIL_STORES",
                         "icon_url": "https://plaid-category-icons.plaid.com/PFC_SHOPPING.png"}},
        {"category": ["Food and Drink", "Coffee Shop"], "category_id": "13005043",
         "pf_category": {"primary": "FOOD_AND_DRINK", "detailed": "FOOD_AND_DRINK_COFFEE",
                         "icon_url": "https://plaid-category-icons.plaid.com/PFC_FOOD_AND_DRINK.png"}},
        {"category": ["Recreation", "Subscription"], "category_id": "17018000",
         "pf_category": {"primary": "ENTERTAINMENT", "detailed": "ENTERTAINMENT_STREAMING_SERVICES",
                         "icon_url": "https://plaid-category-icons.plaid.com/PFC_ENTERTAINMENT.png"}},
    ]

    PAYMENT_CHANNELS = ["online", "in store", "other"]
    TRANSACTION_TYPES = ["place", "special", "digital", "standard"]
    CONFIDENCE_LEVELS = ["VERY_HIGH", "HIGH", "MEDIUM", "LOW"]
    CURRENCIES = ["USD", "EUR", "GBP", "CAD"]

    def __init__(self, seed: int = None):
        """Initialize the factory with an optional random seed for reproducibility."""
        if seed is not None:
            random.seed(seed)

    @staticmethod
    def _generate_id() -> str:
        """Generate a random ID string."""
        return ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=30))

    @staticmethod
    def _generate_date(start_date: str = "2025-01-01", end_date: str = "2025-04-20") -> tuple:
        """Generate a random transaction date and authorized date."""
        start = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.datetime.strptime(end_date, "%Y-%m-%d")

        # Generate a random date between start and end
        transaction_date = start + datetime.timedelta(days=random.randint(0, (end - start).days))

        # Auth date is typically 0-2 days before transaction date
        auth_days_before = random.randint(0, 2)
        auth_date = transaction_date - datetime.timedelta(days=auth_days_before)

        return transaction_date.strftime("%Y-%m-%d"), auth_date.strftime("%Y-%m-%d")

    def _generate_amount(self) -> float:
        """Generate a random transaction amount."""
        # Generate amounts between $1 and $500 with 2 decimal places
        return round(random.uniform(1.0, 500.0), 2)

    def _select_merchant(self) -> dict:
        """Select a random merchant from the MERCHANTS list."""
        return random.choice(self.MERCHANTS)

    def _select_category(self) -> dict:
        """Select a random category from the CATEGORIES list."""
        return random.choice(self.CATEGORIES)

    def _generate_transaction_name(self, merchant_name: str) -> str:
        """Generate a transaction name based on merchant."""
        suffixes = [
            f"{merchant_name} {datetime.datetime.now().strftime('%m%d%y')} SF**POOL**",
            f"{merchant_name} {datetime.datetime.now().strftime('%m%d%y')} ONLINE",
            f"{merchant_name} {datetime.datetime.now().strftime('%m%d%y')} PURCHASE",
            f"{merchant_name} {datetime.datetime.now().strftime('%m%d%y')} PAYMENT",
            f"{merchant_name} {datetime.datetime.now().strftime('%m%d%y')} SUBSCRIPTION",
        ]
        return random.choice(suffixes)

    def create_transaction(self) -> Dict[str, Any]:
        """Create a single transaction object."""
        # Select merchant
        merchant = self._select_merchant()

        # Select category
        category_data = self._select_category()

        # Generate dates
        trans_date, auth_date = self._generate_date()

        # Create counterparty
        counterparty = {
            "name": merchant["name"],
            "type": "merchant",
            "website": merchant["website"],
            "logo_url": merchant["logo_url"],
            "entity_id": merchant["entity_id"],
            "confidence_level": random.choice(self.CONFIDENCE_LEVELS)
        }

        # Generate transaction
        transaction = {
            "account_id": self._generate_id(),
            "amount": self._generate_amount(),
            "iso_currency_code": random.choice(self.CURRENCIES),
            "category": category_data["category"],
            "category_id": category_data["category_id"],
            "date": trans_date,
            "name": self._generate_transaction_name(merchant["name"]),
            "transaction_id": self._generate_id(),
            "authorized_date": auth_date,
            "payment_channel": random.choice(self.PAYMENT_CHANNELS),
            "merchant_name": merchant["name"],
            "transaction_type": random.choice(self.TRANSACTION_TYPES),
            "logo_url": merchant["logo_url"],
            "website": merchant["website"],
            "personal_finance_category": {
                "primary": category_data["pf_category"]["primary"],
                "detailed": category_data["pf_category"]["detailed"],
                "confidence_level": random.choice(self.CONFIDENCE_LEVELS)
            },
            "personal_finance_category_icon_url": category_data["pf_category"]["icon_url"],
            "counterparties": [counterparty],
            "merchant_entity_id": merchant["entity_id"]
        }

        return transaction

    def create_transactions(self, count: int) -> List[Dict[str, Any]]:
        """Create multiple transaction objects."""
        return [self.create_transaction() for _ in range(count)]


def generate_transactions(count: int, seed: int = None) -> List[Dict[str, Any]]:
    """
    Generate a specified number of random transaction objects.

    Args:
        count: Number of transactions to generate
        seed: Optional random seed for reproducibility

    Returns:
        List of transaction objects
    """
    factory = TransactionFactory(seed)
    return factory.create_transactions(count)