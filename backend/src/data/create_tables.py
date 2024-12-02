# File này tạo cấu trúc cơ sở dữ liệu
try:
    from database import Base, engine  # Base defines the database schema - Base định nghĩa schema cơ sở dữ liệu
    from data_models import Restaurant, Foods  # These are the table definitions - Đây là các định nghĩa bảng
except:
    from .database import Base, engine
    from .data_models import Restaurant, Foods


def main():
    # This creates all tables defined in data_models.py - Tạo tất cả các bảng đã được định nghĩa trong data_models.py
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")


if __name__ == "__main__":
    main()
