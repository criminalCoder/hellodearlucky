import pymongo, os
from config import DB_URI, DB_NAME

dbclient = pymongo.MongoClient(DB_URI)
database = dbclient[DB_NAME]
user_data = database['users']
admin_data = database["admins"]



async def present_user(user_id : int):
    found = user_data.find_one({'_id': user_id})
    return bool(found)

async def add_user(user_id: int):
    user_data.insert_one({'_id': user_id})
    return

async def full_userbase():
    user_docs = user_data.find()
    user_ids = []
    for doc in user_docs:
        user_ids.append(doc['_id'])
        
    return user_ids

async def del_user(user_id: int):
    user_data.delete_one({'_id': user_id})
    return

# ====================================================================
#                   Admin ID Management
# ====================================================================
async def get_admin_ids():
    """
    Fetch the list of all admin IDs stored in the database.
    Returns an empty list if no admin IDs exist.
    """
    record = admin_data.find_one({"type": "admin_list"})
    return record.get("admin_ids", []) if record else []

async def add_admin_id(admin_id: int):
    """
    Add an admin ID to the admin list. Avoids duplicates using $addToSet.
    """
    admin_data.update_one(
        {"type": "admin_list"},
        {"$addToSet": {"admin_ids": admin_id}},  # Avoid duplicates
        upsert=True  # Create the document if it doesn't exist
    )

async def remove_admin_id(admin_id: int):
    """
    Remove an admin ID from the list.
    """
    admin_data.update_one(
        {"type": "admin_list"},
        {"$pull": {"admin_ids": admin_id}}  # Remove the admin ID
    )   
# ====================================================================
# ====================================================================
