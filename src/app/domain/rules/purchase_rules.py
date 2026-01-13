
MAX_PURCHASES = 5

def check_max_purchases(current_count: int):

     # Проверяет, что количество покупок не превышает лимит
    if current_count >= MAX_PURCHASES:
        raise ValueError(f"Cannot add more than {MAX_PURCHASES} purchases")
