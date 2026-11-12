"""20 everyday items whose GST rate changed, from the 56th GST Council meeting.

Source: PIB press release, 3 Sep 2025 (Annexure I and II, goods).
Goods rate changes took effect on 22 Sep 2025.
"""

DOC = "56th GST Council press release (PIB, 3 Sep 2025)"
URL = "https://gstcouncil.gov.in/sites/default/files/2025-09/press_release_press_information_bureau.pdf"
EFFECTIVE = "2025-09-22"


def _rec(id_, item, category, old, new):
    return {
        "id": id_,
        "item_or_topic": item,
        "category": category,
        "old_rule": f"GST {old}",
        "new_rule": f"GST {new}",
        "effective_from": EFFECTIVE,
        "document": DOC,
        "source_url": URL,
    }


RECORDS = [
    _rec(1, "Toilet soap bars", "Personal care", "18%", "5%"),
    _rec(2, "Hair oil and shampoo", "Personal care", "18%", "5%"),
    _rec(3, "Toothpaste and dental floss", "Personal care", "18%", "5%"),
    _rec(4, "Tooth brushes", "Personal care", "18%", "5%"),
    _rec(5, "Bicycles (non-motorised)", "Household", "12%", "5%"),
    _rec(6, "Kitchenware and utensils of iron, steel, copper, aluminium", "Household", "12%", "5%"),
    _rec(7, "Umbrellas", "Household", "12%", "5%"),
    _rec(8, "Baby napkins and diapers", "Household", "12%", "5%"),
    _rec(9, "UHT milk", "Dairy and bread", "5%", "Nil"),
    _rec(10, "Paneer / chena, pre-packaged and labelled", "Dairy and bread", "5%", "Nil"),
    _rec(11, "Roti, chapathi, khakhra", "Dairy and bread", "5%", "Nil"),
    _rec(12, "Paratha, parotta and other Indian breads", "Dairy and bread", "18%", "Nil"),
    _rec(13, "Butter and ghee", "Dairy and bread", "12%", "5%"),
    _rec(14, "Namkeen and bhujia, pre-packaged", "Packaged food", "12%", "5%"),
    _rec(15, "Chocolates", "Packaged food", "18%", "5%"),
    _rec(16, "Exercise books and notebooks", "Education", "12%", "Nil"),
    _rec(17, "Pencils and crayons", "Education", "12%", "Nil"),
    _rec(18, "Erasers", "Education", "5%", "Nil"),
    _rec(19, "Air-conditioning machines", "Consumer electronics", "28%", "18%"),
    _rec(20, "Television sets", "Consumer electronics", "28%", "18%"),
]
