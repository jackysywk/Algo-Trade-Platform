from app import app
from app.models.ib_interface import disconnect_from_ib

if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", port=8080)
    except Exception as e:
        print(f"An exception occurred: {e}")
    finally:
        disconnect_from_ib()
        print("Disconnected from Interactive Brokers.")