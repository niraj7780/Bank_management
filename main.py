from menu import start
from database import Database

try:
    start()

except KeyboardInterrupt:

    print("\n\nProgram terminated by user.")

except Exception as e:

    print("\nUnexpected Error:", e)

finally:

    try:
        db = Database()
        db.close()
    except:
        pass

    print("Application Closed.")