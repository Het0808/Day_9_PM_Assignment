# ============================================================
#  product_analytics.py
#  E-Commerce Product Analytics Tool
#  Uses: namedtuple, sets, set operations, comprehensions
# ============================================================

from collections import namedtuple

# ─────────────────────────────────────────────────────────────
# 1️⃣  NAMED TUPLE — Product
# ─────────────────────────────────────────────────────────────
Product = namedtuple("Product", ["id", "name", "category", "price"])


# ─────────────────────────────────────────────────────────────
# 2️⃣  PRODUCT CATALOG  (15 products across 4 categories)
# ─────────────────────────────────────────────────────────────
catalog = [
    # Electronics (4)
    Product(1,  "Laptop",             "Electronics",  75000),
    Product(2,  "Smartphone",         "Electronics",  45000),
    Product(3,  "Wireless Earbuds",   "Electronics",   3500),
    Product(4,  "Smart Watch",        "Electronics",  12000),

    # Clothing (4)
    Product(5,  "Denim Jacket",       "Clothing",      2500),
    Product(6,  "Running Shoes",      "Clothing",      4000),
    Product(7,  "Casual T-Shirt",     "Clothing",       800),
    Product(8,  "Formal Trousers",    "Clothing",      1800),

    # Books (4)
    Product(9,  "Clean Code",         "Books",          650),
    Product(10, "Python Crash Course","Books",          550),
    Product(11, "Atomic Habits",      "Books",          499),
    Product(12, "Deep Work",          "Books",          420),

    # Home (3)
    Product(13, "Air Purifier",       "Home",          8000),
    Product(14, "LED Desk Lamp",      "Home",          1200),
    Product(15, "Coffee Maker",       "Home",          3500),
]

# Convenience look-up by id
catalog_by_id = {p.id: p for p in catalog}


# ─────────────────────────────────────────────────────────────
# 3️⃣  CUSTOMER CARTS  (5 carts, each a set of Product tuples)
# ─────────────────────────────────────────────────────────────
p = catalog_by_id   # short alias

customer_1_cart = {p[1], p[3], p[7], p[9],  p[14]}   # Laptop, Watch, T-Shirt, Clean Code, Lamp
customer_2_cart = {p[1], p[2], p[9], p[10], p[13]}   # Laptop, Phone, Clean Code, Python CC, Purifier
customer_3_cart = {p[1], p[5], p[9], p[11], p[15]}   # Laptop, Jacket, Clean Code, Atomic Habits, Coffee
customer_4_cart = {p[1], p[6], p[9], p[12], p[14]}   # Laptop, Shoes, Clean Code, Deep Work, Lamp
customer_5_cart = {p[1], p[4], p[9], p[10], p[13]}   # Laptop, Earbuds, Clean Code, Python CC, Purifier

all_carts = [
    customer_1_cart,
    customer_2_cart,
    customer_3_cart,
    customer_4_cart,
    customer_5_cart,
]


# ─────────────────────────────────────────────────────────────
# 4️⃣  SHOPPING BEHAVIOUR ANALYSIS
# ─────────────────────────────────────────────────────────────

# (a) Bestsellers — products in ALL carts  (intersection)
def get_bestsellers(carts: list[set]) -> set:
    """Products that every customer bought."""
    result = carts[0].copy()
    for cart in carts[1:]:
        result &= cart          # set intersection
    return result


# (b) Catalog Reach — products in ANY cart  (union)
def get_catalog_reach(carts: list[set]) -> set:
    """All products that at least one customer bought."""
    result = set()
    for cart in carts:
        result |= cart          # set union
    return result


# (c) Exclusive Purchases — only customer_1 bought  (difference)
def get_exclusive_purchases(customer_cart: set, other_carts: list[set]) -> set:
    """Products bought by this customer and nobody else."""
    others_union = set()
    for cart in other_carts:
        others_union |= cart
    return customer_cart - others_union   # set difference


# ─────────────────────────────────────────────────────────────
# 5️⃣  PRODUCT RECOMMENDATION
# ─────────────────────────────────────────────────────────────

def recommend_products(customer_cart: set, all_carts: list[set]) -> set:
    """
    Suggest products other customers bought that this customer hasn't.
    Uses set difference: (union of all other carts) - customer_cart
    """
    others_union: set = set()
    for cart in all_carts:
        if cart is not customer_cart:
            others_union |= cart
    return others_union - customer_cart   # set difference


# ─────────────────────────────────────────────────────────────
# 6️⃣  CATEGORY SUMMARY
# ─────────────────────────────────────────────────────────────

def category_summary() -> dict[str, set]:
    """
    Returns a dict mapping each category to the set of product names in it.
    Uses set comprehension.
    """
    categories = {p.category for p in catalog}          # unique categories
    return {
        cat: {p.name for p in catalog if p.category == cat}
        for cat in categories
    }


# ─────────────────────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────────────────────

def names(product_set: set) -> list[str]:
    """Return sorted product names from a set of Product tuples."""
    return sorted(p.name for p in product_set)


def divider(title: str) -> None:
    width = 55
    print(f"\n{'─' * width}")
    print(f"  {title}")
    print(f"{'─' * width}")


# ─────────────────────────────────────────────────────────────
#  DEMO / MAIN
# ─────────────────────────────────────────────────────────────

def main() -> None:

    divider("📦 PRODUCT CATALOG")
    for prod in catalog:
        print(f"  [{prod.id:>2}] {prod.name:<22} | {prod.category:<11} | ₹{prod.price:>7,}")

    divider("🛒 CUSTOMER CARTS")
    for i, cart in enumerate(all_carts, 1):
        print(f"  Customer {i}: {names(cart)}")

    # ── 4a  Bestsellers ──────────────────────────────────────
    divider("🏆 4a) BESTSELLERS  (in ALL carts — intersection)")
    bestsellers = get_bestsellers(all_carts)
    print(f"  {names(bestsellers)}")

    # ── 4b  Catalog Reach ────────────────────────────────────
    divider("🌐 4b) CATALOG REACH  (in ANY cart — union)")
    reach = get_catalog_reach(all_carts)
    print(f"  {names(reach)}")
    print(f"  Total products sold: {len(reach)} / {len(catalog)}")

    # ── 4c  Exclusive Purchases ──────────────────────────────
    divider("🔒 4c) EXCLUSIVE PURCHASES  (Customer 1 only — difference)")
    other_carts = all_carts[1:]
    exclusives = get_exclusive_purchases(customer_1_cart, other_carts)
    if exclusives:
        print(f"  {names(exclusives)}")
    else:
        print("  (none — all of Customer 1's items were bought by others too)")

    # ── 5  Recommendations ──────────────────────────────────
    divider("💡 5) RECOMMENDATIONS for Customer 1")
    recs = recommend_products(customer_1_cart, all_carts)
    print(f"  {names(recs)}")

    # ── 6  Category Summary ──────────────────────────────────
    divider("📊 6) CATEGORY SUMMARY")
    summary = category_summary()
    for cat in sorted(summary):
        print(f"  {cat:<12}: {sorted(summary[cat])}")

    print(f"\n{'─' * 55}\n")


if __name__ == "__main__":
    main()
