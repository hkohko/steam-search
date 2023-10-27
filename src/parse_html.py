import asyncio

from bs4 import BeautifulSoup

from get_request import main


async def is_discounted(tag):
    child_price_class_attribute = "discount_block search_discount_block"
    parent_no_discount = tag.find("div", {"class": child_price_class_attribute})
    discount_percent = parent_no_discount.find("div", {"class": "discount_pct"}).text
    original_price = parent_no_discount.find(
        "div", {"class": "discount_original_price"}
    ).text
    discounted_price = parent_no_discount.find(
        "div", {"class": "discount_final_price"}
    ).text
    print(discount_percent)
    print(original_price)
    print(discounted_price)


async def parser(search: str):
    page = await main(search)
    soup = BeautifulSoup(page, "lxml")
    div = soup.find("div", {"id": "search_result_container"})
    div2 = div.find("div", {"data-panel": True, "id": True})
    if div2 is None:
        return None
    a = div2.find("a")
    store_link = a.get("href")

    parent_container = a.find("div", {"class": "responsive_search_name_combined"})
    namediv = parent_container.find("div", {"class": "col search_name ellipsis"})
    product_name = namediv.find("span", {"class": "title"}).text
    release_date = parent_container.find(
        "div", {"class": "col search_released responsive_secondrow"}
    ).text
    reviewscore = parent_container.find(
        "div", {"class": "col search_reviewscore responsive_secondrow"}
    )
    reviews = reviewscore.find("span", {"class": True, "data-tooltip-html": True})
    if reviews is not None:
        reviews = reviews.get("data-tooltip-html")
    else:
        reviews = "No review data found."
    print(product_name)
    print(release_date)
    print(store_link)
    print(reviews)

    parent_price = parent_container.find(
        "div", {"class": "col search_price_discount_combined responsive_secondrow"}
    )

    child_price = parent_price.find(
        "div",
        {
            "class": True,
            "data-price-final": True,
            "data-bundlediscount": True,
            "data-discount": True,
        },
    )
    if child_price is None:  # game is Free
        free = parent_price.find("div", {"class": "discount_final_price free"}).text
        print(free)
        return
    elif child_price.get("data-discount") != "0":  # game is discounted
        await is_discounted(parent_price)
        return
    else:  # regular price
        price = parent_price.find("div", {"class": "discount_final_price"}).text
        print(price)


if __name__ == "__main__":
    with asyncio.Runner() as runner:
        runner.run(parser("dredge"))
