from database import Database

db = Database()

managerid = db.addmanager(
    "Niraj Charpe",
    "8450022024",
    "admin",
    "admin123"
)

print("Manager Created Successfully")
print("Manager ID:", managerid)

db.close()