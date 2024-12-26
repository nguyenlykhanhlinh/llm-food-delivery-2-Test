import pandas as pd
from sqlalchemy.orm import Session

from database import SessionLocal
from data_models import Restaurant, Foods


# Hàm thêm nhà hàng vào cơ sở dữ liệu
def add_restaurant(db: Session, name: str, description: str, image: str):
    restaurant = Restaurant(name=name, description=description, image=image)
    db.add(restaurant)
    db.commit()
    db.refresh(restaurant)
    return restaurant 


# Hàm thêm món ăn vào cơ sở dữ liệu
def add_food(
    db: Session, restaurant_id: int, name: str, description: str, image: str, price: int
):
    food = Foods(
        restaurant_id=restaurant_id,
        name=name,
        description=description,
        image=image,
        price=price,
    )
    db.add(food)
    db.commit()
    db.refresh(food)
    return food


def main():
    db = SessionLocal()

    # Sample data for restaurants
    restaurants = [
        {
            "name": "Nhà Hàng Chay Việt Co",
            "description": "Nhà hàng của chúng tôi chuyên cung cấp các món ăn Việt Nam, các món ăn nổi bật được yêu thích tại Việt Nam, mời bạn cùng gia đình và bạn bè thưởng thức một bữa tiệc Việt Nam đích thực.",
            "image": "/static/restaurants/CoVietnamese_Restaurant&Vegan.png",
        },
        {
            "name": "SushiLAB",
            "description": "Sushi tươi và các món ăn Nhật Bản",
            "image": "/static/restaurants/sushi_lab.png",
        },
        {
            "name": "Nhà Hàng The Eroica",
            "description": "Nhà hàng The Eroica dẫn dắt thực khách vào một hành trình ẩm thực đa tầng với thực đơn đa dạng các món ăn Á - Âu. Không gian fine-dining được thiết kế sang trọng, tinh tế và hài hòa đến từng chi tiết, hứa hẹn là điểm đến lý tưởng cho bất kỳ buổi hẹn đặc biệt nào: từ bữa tối lãng mạn cho các cặp đôi, buổi gặp mặt gia đình hoặc tiệc công ty. Bạn sẽ trải nghiệm dịch vụ ẩm thực hoàn hảo với nhiều món ăn ngon từ các đầu bếp tài năng của chúng tôi.",
            "image": "/static/restaurants/the_eroica_restaurant.png",
        },
        {
            "name": "Burger King Hàng Buồm",
            "description": "Burger cao cấp và khoai tây chiên",
            "image": "/static/restaurants/burger_king_hang_buom.png",
        },
        {
            "name": "Pizza Hub - Pizza Nướng Lò Củi & Đồ Nướng",
            "description": "Pizza nướng lò củi",
            "image": "/static/restaurants/pizza_hub_wood_fired_pizza_grills.png",
        },
        {
            "name": "Indian Spice",
            "description": "Các món cà ri và nướng truyền thống của Ấn Độ",
            "image": "/static/restaurants/indian_spice.png",
        },
        {
            "name": "Thai Delight",
            "description": "Các món Thái ngon miệng và mì",
            "image": "/static/restaurants/thai_delight.png",
        },
        {
            "name": "Chinese Wok",
            "description": "Ẩm thực Trung Hoa cổ điển và dim sum",
            "image": "/static/restaurants/chinese_wok.png",
        },
        {
            "name": "Mediterranean Grill",
            "description": "Hương vị Địa Trung Hải tươi ngon và kebab",
            "image": "/static/restaurants/mediterranean_grill.png",
        },
        {
            "name": "French Bistro",
            "description": "Ẩm thực Pháp tinh tế và bánh ngọt",
            "image": "/static/restaurants/french_bistro.png",
        },
        {
            "name": "Steakhouse",
            "description": "Bít tết cao cấp và hải sản",
            "image": "/static/restaurants/steakhouse.png",
        },
        {
            "name": "Vegan Cafe",
            "description": "Các món chay và sinh tố",
            "image": "/static/restaurants/vegan_cafe.png",
        },
        {
            "name": "Greek Taverna",
            "description": "Các món Hy Lạp cổ điển và hải sản",
            "image": "/static/restaurants/greek_taverna.png",
        },
        {
            "name": "Southern Comfort",
            "description": "Các món ăn gia đình miền Nam",
            "image": "/static/restaurants/southern_comfort.png",
        },
        {
            "name": "BBQ Shack",
            "description": "Thịt nướng và BBQ",
            "image": "/static/restaurants/bbq_shack.png",
        },
        {
            "name": "Seafood Delight",
            "description": "Hải sản tươi ngon và các món cá",
            "image": "/static/restaurants/seafood_delight.png",
        },
        {
            "name": "Veggie Heaven",
            "description": "Các món chay và thuần chay ngon miệng",
            "image": "/static/restaurants/veggie_heaven.png",
        },
        {
            "name": "Chicken Coop",
            "description": "Các món gà nướng và chiên",
            "image": "/static/restaurants/chicken_coop.png",
        },
        {
            "name": "Pasta Paradise",
            "description": "Đa dạng các món mì Ý",
            "image": "/static/restaurants/pasta_paradise.png",
        },
        {
            "name": "Bakery Bliss",
            "description": "Bánh mì và bánh ngọt tươi ngon",
            "image": "/static/restaurants/bakery_bliss.png",
        },
        {
            "name": "Salad Bar",
            "description": "Các món salad ngon và lành mạnh",
            "image": "/static/restaurants/salad_bar.png",
        },
        {
            "name": "Ramen House",
            "description": "Mì ramen và các món Nhật",
            "image": "/static/restaurants/ramen_house.png",
        },
        {
            "name": "Ice Cream Shop",
            "description": "Đa dạng các hương vị kem và món tráng miệng",
            "image": "/static/restaurants/ice_cream_shop.png",
        },
        {
            "name": "Sandwich Shop",
            "description": "Bánh mì sandwich và cuộn tươi ngon",
            "image": "/static/restaurants/sandwich_shop.png",
        },
        {
            "name": "Pancake House",
            "description": "Các loại pancake ngọt và mặn",
            "image": "/static/restaurants/pancake_house.png",
        },
        {
            "name": "Bún Chả Tạ",
            "description": "Bún chả Tạ là món ăn Việt Nam gồm thịt nướng và bún",
            "image": "/static/restaurants/bun_cha_ta.png",
        },
    ]


    # Sample data for foods
    foods = [
        # Nhà Hàng Chay Việt Co
        {
            "restaurant_id": 1,
            "name": "Nem rán",
            "description": "Nem rán hoặc nem cuốn với nhiều loại nhân như rau củ, thịt và bún.",
            "image": "/static/foods/fried_spring_rolls.png",
            "price": 70.000,
        },
        {
            "restaurant_id": 1,
            "name": "Phở bò/gà truyền thống",
            "description": "Món phở cổ điển Việt Nam với bún gạo, phục vụ cùng lựa chọn thịt bò hoặc gà.",
            "image": "/static/foods/traditional_noodle_soup_with_beef_chicken.png",
            "price": 70.000,
        },
        {
            "restaurant_id": 1,
            "name": "Bánh xèo đặc biệt",
            "description": "Bánh xèo Việt Nam làm từ bột gạo, nghệ, và nước cốt dừa, thường có nhân tôm, thịt heo và giá đỗ.",
            "image": "/static/foods/special_vietnamese_pancace_banh_xeo.png",
            "price": 100.000,
        },
        {
            "restaurant_id": 1,
            "name": "Bò hoặc heo cuốn lá lốt kèm bún tươi (6 cuốn)",
            "description": "Thịt nướng cuộn lá lốt, phục vụ cùng bún tươi và nước chấm.",
            "image": "/static/foods/beef_or_pork_rolled_with_betel_leaves_come_with_fresh_noodle_6pcs.png",
            "price": 100.000,
        },
        {
            "restaurant_id": 1,
            "name": "Gỏi hoa chuối tôm thịt",
            "description": "Gỏi hoa chuối tươi ngon với tôm, thịt gà và nước sốt chua ngọt.",
            "image": "/static/foods/banana_flower_salad_with_shrimp_chicken.png",
            "price": 110.000,
        },
        {
            "restaurant_id": 1,
            "name": "Bún chả Hà Nội truyền thống",
            "description": "Món ăn đặc trưng Hà Nội với thịt nướng, bún tươi, rau thơm và nước chấm.",
            "image": "/static/foods/hanoi_traditional_grilled_pork_with_rice_noodle_bun_cha.png",
            "price": 115.000,
        },
        {
            "restaurant_id": 1,
            "name": "Nem lụi nướng",
            "description": "Nem nướng từ thịt heo băm nhuyễn, nêm nếm với sả, phục vụ cùng rau sống và nước chấm.",
            "image": "/static/foods/fried_minced_pork_in_lemongrass_nem_lui.png",
            "price": 90.000,
        },
        {
            "restaurant_id": 1,
            "name": "Súp kem nấm và rau củ",
            "description": "Súp kem thơm ngon với nấm và rau củ.",
            "image": "/static/foods/vegetable_soup_with_cream_and_mushroom_soup.png",
            "price": 80.000,
        },
        # SushiLAB
        {
            "restaurant_id": 2,
            "name": "California Roll",
            "description": "Cuộn sushi với thịt cua, bơ và dưa chuột.",
            "image": "/static/foods/california_roll.png",
            "price": 80.000,
        },
        {
            "restaurant_id": 2,
            "name": "Spicy Tuna Roll",
            "description": "Cuộn sushi với cá ngừ cay, sốt mayo và dưa chuột.",
            "image": "/static/foods/spicy_tuna_roll.png",
            "price": 90.000,
        },
        {
            "restaurant_id": 2,
            "name": "Salmon Nigiri",
            "description": "Sushi với một lát cá hồi tươi trên cơm sushi.",
            "image": "/static/foods/salmon_nigiri.png",
            "price": 70.000,
        },
        {
            "restaurant_id": 2,
            "name": "Shrimp Tempura Roll",
            "description": "Cuộn sushi với tôm chiên tempura, bơ và dưa chuột.",
            "image": "/static/foods/shrimp_tempura_roll.png",
            "price": 100.000,
        },
        {
            "restaurant_id": 2,
            "name": "Súp Miso",
            "description": "Súp Nhật Bản truyền thống với đậu phụ và rong biển.",
            "image": "/static/foods/miso_soup.png",
            "price": 40.000,
        },
        {
            "restaurant_id": 2,
            "name": "Rượu Sake",
            "description": "Rượu gạo Nhật Bản.",
            "image": "/static/beverages/sake.png",
            "price": 60.000,
        },
        {
            "restaurant_id": 2,
            "name": "Trà xanh Nhật",
            "description": "Trà xanh Nhật Bản nóng.",
            "image": "/static/beverages/green_tea.png",
            "price": 30.000,
        },
        {
            "restaurant_id": 2,
            "name": "Rượu Mận",
            "description": "Rượu ngọt Nhật Bản làm từ mận.",
            "image": "/static/beverages/plum_wine.png",
            "price": 70.000,
        },
        # Burger King Hàng Buồm
        {
            "restaurant_id": 4,
            "name": "Burger Phô Mai Truyền Thống",
            "description": "Burger thơm ngon với phô mai, xà lách, cà chua và hành.",
            "image": "/static/foods/classic_cheeseburger.png",
            "price": 100.000,
        },
        {
            "restaurant_id": 4,
            "name": "Burger Thịt Xông Khói",
            "description": "Burger hấp dẫn với thịt xông khói, phô mai, xà lách, cà chua và hành.",
            "image": "/static/foods/bacon_burger.png",
            "price": 120.000,
        },
        {
            "restaurant_id": 4,
            "name": "Burger Nấm Phô Mai Thụy Sĩ",
            "description": "Burger ngon miệng với phô mai Thụy Sĩ và nấm xào.",
            "image": "/static/foods/mushroom_swiss_burger.png",
            "price": 110.000,
        },
        {
            "restaurant_id": 4,
            "name": "Burger Chay",
            "description": "Burger chay lành mạnh với xà lách, cà chua và hành.",
            "image": "/static/foods/veggie_burger.png",
            "price": 100.000,
        },
        {
            "restaurant_id": 4,
            "name": "Khoai Tây Chiên",
            "description": "Khoai tây chiên vàng giòn kèm tương cà.",
            "image": "/static/foods/french_fries.png",
            "price": 40.000,
        },
        # Bun Cha Ta
        {
            "restaurant_id": 1,
            "name": "Bún Chả Tạ",
            "description": "Món Bún Chả Tạ với thịt nướng và bún, kèm nước chấm chua ngọt.",
            "image": "/static/foods/bun_cha_ta.png",
            "price": 100.000,
        },
    ]


    # Populate restaurants table
    for restaurant in restaurants:
        add_restaurant(
            db, restaurant["name"], restaurant["description"], restaurant["image"]
        )

    # Populate foods table
    for food in foods:
        add_food(
            db,
            food["restaurant_id"],
            food["name"],
            food["description"],
            food["image"],
            food["price"],
        )

    print("Data populated successfully!")


if __name__ == "__main__":
    main()
