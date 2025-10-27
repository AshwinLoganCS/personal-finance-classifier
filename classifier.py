"""
Transaction categorization module with rule-based keyword matching classifier.
"""

import re
from typing import List, Dict


# Define category keywords for rule-based classification
CATEGORY_KEYWORDS = {
    'Food & Dining': [
        'restaurant', 'cafe', 'coffee', 'starbucks', 'dunkin', 'mcdonald',
        'burger', 'pizza', 'chipotle', 'subway', 'taco', 'doordash',
        'ubereats', 'grubhub', 'postmates', 'seamless', 'delivery',
        'diner', 'bistro', 'grill', 'bar', 'pub', 'kitchen', 'food',
        'dining', 'eatery', 'panera', 'chick-fil-a', 'chick fil a', 'wendys', 'kfc',
        'panda express', 'taco bell', 'coffee hut', 'dairy queen',
        'in n out', 'domino', 'yogurtland', 'coldstone', 'ice cream',
        'wingstop', 'cajun', 'burrito', 'snack', 'salt and straw',
        'koja kitchen', 'purple kow', 'yogurt park', 'mochiholic',
        'bricks cafe', 'sweet spot', 'matcha cafe', 'ice monster',
        'angry chickz', 'campus burgers', 'too good to go'
    ],
    'Groceries': [
        'grocery', 'supermarket', 'whole foods', 'trader joe', 'trader jo',
        'safeway', 'kroger', 'walmart', 'target', 'costco', 'sam\'s club', 'aldi',
        'publix', 'wegmans', 'heb', 'market', 'fresh', 'food lion',
        'giant eagle', 'stop & shop', 'harris teeter', 'sprouts',
        'dollar tree', 'dollartre'
    ],
    'Transportation': [
        'uber', 'lyft', 'taxi', 'cab', 'transit', 'subway', 'metro',
        'bus', 'train', 'parking', 'gas', 'fuel', 'shell', 'exxon',
        'chevron', 'bp', 'mobil', 'citgo', 'speedway', 'wawa',
        'car wash', 'auto', 'vehicle', 'dmv', 'registration', 'toll',
        'sokwik'
    ],
    'Entertainment': [
        'movie', 'cinema', 'theater', 'theatre', 'netflix', 'hulu',
        'spotify', 'apple music', 'disney', 'hbo',
        'youtube', 'twitch', 'game', 'gaming', 'steam', 'playstation',
        'xbox', 'nintendo', 'concert', 'ticket', 'ticketmaster',
        'stubhub', 'sports event', 'gym', 'fitness', 'club', 'membership'
    ],
    'Gambling/Sports Betting': [
        'prizepicks', 'underdog', 'draftkings', 'fanduel', 'betmgm',
        'caesars', 'pointsbet', 'bet365', 'unibet', 'bovada',
        'mybookie', 'bet online', 'sports bet', 'casino', 'poker',
        'slots', 'lottery', 'scratch', 'gambling'
    ],
    'Subscriptions': [
        'whop', 'patreon', 'onlyfans', 'substack', 'chatgpt', 'openai',
        'adobe', 'office 365', 'icloud', 'dropbox', 'google one',
        'youtube premium', 'spotify premium', 'apple one', 'microsoft 365',
        'creative cloud', 'zoom', 'slack', 'notion', 'canva',
        'grammarly', 'medium', 'scribd', 'prime video', 'walter ai',
        'agent eo premium', 'worldfinancialgroup', 'amazon prime',
        'apple.com bill', 'apple com bill', 'apple bill'
    ],
    'Transfers': [
        'apple cash', 'apple pay balance', 'venmo', 'zelle', 'paypal',
        'cash app', 'google pay', 'facebook pay', 'transfer to',
        'transfer from', 'pmnt sent', 'pmnt received', 'p2p transfer',
        'peer to peer', 'balance add', 'balance transfer', 'pc transfer',
        'ppd', 'cashout', 'direct pay', 'direct deposit'
    ],
    'Shopping': [
        'amazon', 'ebay', 'etsy', 'shop', 'store', 'mall', 'retail',
        'best buy', 'apple store', 'nike', 'adidas', 'macy', 'nordstrom',
        'gap', 'zara', 'h&m', 'forever 21', 'old navy', 'tj maxx',
        'marshalls', 'ross', 'kohls', 'jcpenney', 'sephora', 'ulta',
        'home depot', 'lowes', 'ikea', 'furniture', 'clothing', 'apparel',
        'cscsw', 'temu', 'shein', 'wish', 'aliexpress', 'wayfair',
        'fashionnova', 'tiktok shop', 'shop miss a'
    ],
    'Bills & Utilities': [
        'electric', 'electricity', 'power', 'gas company', 'water',
        'internet', 'cable', 'phone', 'mobile', 'verizon', 'at&t',
        't-mobile', 'sprint', 'comcast', 'xfinity', 'spectrum',
        'utility', 'bill payment', 'insurance', 'rent', 'mortgage',
        'loan', 'credit card payment', 'bank fee'
    ],
    'Health': [
        'pharmacy', 'cvs', 'walgreens', 'rite aid', 'medical', 'hospital',
        'doctor', 'clinic', 'health', 'dental', 'dentist', 'vision',
        'optometry', 'prescription', 'medicine', 'wellness', 'therapy',
        'counseling', 'urgent care', 'emergency', 'lab', 'test'
    ],
    'Income': [
        'salary', 'payroll', 'deposit', 'direct deposit', 'payment received',
        'refund', 'reimbursement', 'bonus', 'dividend',
        'interest', 'cashback', 'reward', 'credit via trust'
    ]
}


class RuleBasedClassifier:
    """
    Rule-based transaction classifier using keyword matching.
    """
    
    def __init__(self):
        self.categories = CATEGORY_KEYWORDS
    
    def classify(self, description: str, amount: float) -> str:
        """
        Classify a transaction based on its description and amount.
        
        Args:
            description (str): Transaction description
            amount (float): Transaction amount
            
        Returns:
            str: Category name
        """
        # If positive amount, likely income
        if amount > 0:
            return 'Income'
        
        # Normalize description for matching
        description_lower = description.lower()
        
        # Score each category based on keyword matches
        category_scores = {}
        
        for category, keywords in self.categories.items():
            score = 0
            for keyword in keywords:
                if keyword.lower() in description_lower:
                    # Longer keyword matches get higher scores
                    score += len(keyword)
            category_scores[category] = score
        
        # Get category with highest score
        if category_scores:
            best_category = max(category_scores, key=category_scores.get)
            if category_scores[best_category] > 0:
                return best_category
        
        # Default to 'Other' if no match found
        return 'Other'
    
    def classify_batch(self, descriptions: List[str], amounts: List[float]) -> List[str]:
        """
        Classify multiple transactions at once.
        
        Args:
            descriptions (List[str]): List of transaction descriptions
            amounts (List[float]): List of transaction amounts
            
        Returns:
            List[str]: List of category names
        """
        return [self.classify(desc, amt) for desc, amt in zip(descriptions, amounts)]


def get_classifier():
    """
    Get the rule-based transaction classifier.
    
    Returns:
        RuleBasedClassifier: Instance of the rule-based classifier
    """
    return RuleBasedClassifier()


def get_all_categories() -> List[str]:
    """
    Get list of all available categories.
    
    Returns:
        List[str]: List of category names
    """
    return list(CATEGORY_KEYWORDS.keys()) + ['Other']

