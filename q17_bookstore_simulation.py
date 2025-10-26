import numpy as np

# Financial parameters
BOOK_COST = 15
SELLING_PRICE = 25
RETURN_VALUE = 5
PROFIT_PER_SALE = SELLING_PRICE - BOOK_COST  # $10
LOSS_PER_UNSOLD = BOOK_COST - RETURN_VALUE  # $10
LOST_PROFIT_PER_BOOK = PROFIT_PER_SALE  # $10

# Day type probabilities
DAY_TYPE_PROBS = {
    'High': 0.4,
    'Medium': 0.3,
    'Low': 0.3
}

# Demand distributions for each day type
DEMAND_DISTRIBUTIONS = {
    'High': {
        50: 0.05,
        60: 0.07,
        70: 0.1,
        80: 0.2,
        90: 0.3,
        100: 0.15,
        110: 0.13
    },
    'Medium': {
        50: 0.12,
        60: 0.16,
        70: 0.3,
        80: 0.2,
        90: 0.08,
        100: 0.06,
        110: 0.08
    },
    'Low': {
        50: 0.3,
        60: 0.2,
        70: 0.06,
        80: 0.12,
        90: 0.13,
        100: 0.09,
        110: 0.1
    }
}


def sample_day_type(rng):
    """Sample a day type based on probabilities."""
    day_types = list(DAY_TYPE_PROBS.keys())
    probs = list(DAY_TYPE_PROBS.values())
    return rng.choice(day_types, p=probs)


def sample_demand(day_type, rng):
    """Sample demand quantity for a given day type."""
    demands = list(DEMAND_DISTRIBUTIONS[day_type].keys())
    probs = list(DEMAND_DISTRIBUTIONS[day_type].values())
    return rng.choice(demands, p=probs)


def calculate_profit(stock, demand):
    """
    Calculate profit for a given stock level and demand.
    
    Returns:
        dict with detailed breakdown
    """
    # Books sold is minimum of stock and demand
    sold = min(stock, demand)
    
    # Unsold books (if stock > demand)
    unsold = max(0, stock - demand)
    
    # Lost sales (if demand > stock)
    lost_sales = max(0, demand - stock)
    
    # Financial calculations
    revenue = sold * SELLING_PRICE
    cost = stock * BOOK_COST
    return_value = unsold * RETURN_VALUE
    lost_profit = lost_sales * LOST_PROFIT_PER_BOOK
    
    # Total profit = Revenue - Cost + Return - Lost Profit
    profit = revenue - cost + return_value - lost_profit
    
    return {
        'sold': sold,
        'unsold': unsold,
        'lost_sales': lost_sales,
        'revenue': revenue,
        'cost': cost,
        'return_value': return_value,
        'lost_profit': lost_profit,
        'profit': profit
    }


def run_bookstore_simulation(stock_quantity, num_days, random_seed=None):
    """
    Run the bookstore simulation for a given number of days.
    
    Parameters:
        stock_quantity: Number of books to stock each day
        num_days: Number of days to simulate
        random_seed: Random seed for reproducibility
    
    Returns:
        Dictionary with simulation results
    """
    rng = np.random.default_rng(random_seed)
    
    daily_results = []
    total_profit = 0
    
    for day in range(1, num_days + 1):
        # Determine day type
        day_type = sample_day_type(rng)
        
        # Sample demand for this day
        demand = sample_demand(day_type, rng)
        
        # Calculate profit for this day
        day_profit = calculate_profit(stock_quantity, demand)
        
        # Store daily results
        daily_results.append({
            'day': day,
            'day_type': day_type,
            'demand': demand,
            'sold': day_profit['sold'],
            'unsold': day_profit['unsold'],
            'lost_sales': day_profit['lost_sales'],
            'revenue': day_profit['revenue'],
            'cost': day_profit['cost'],
            'return_value': day_profit['return_value'],
            'lost_profit': day_profit['lost_profit'],
            'profit': day_profit['profit']
        })
        
        total_profit += day_profit['profit']
    
    # Calculate summary statistics
    avg_demand = np.mean([d['demand'] for d in daily_results])
    avg_sold = np.mean([d['sold'] for d in daily_results])
    avg_unsold = np.mean([d['unsold'] for d in daily_results])
    avg_lost_sales = np.mean([d['lost_sales'] for d in daily_results])
    avg_profit_per_day = total_profit / num_days
    
    return {
        'stock_quantity': stock_quantity,
        'num_days': num_days,
        'total_profit': total_profit,
        'avg_profit_per_day': avg_profit_per_day,
        'avg_demand': avg_demand,
        'avg_sold': avg_sold,
        'avg_unsold': avg_unsold,
        'avg_lost_sales': avg_lost_sales,
        'daily_results': daily_results
    }