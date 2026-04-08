import uuid
from datetime import timezone, datetime

from pymongo import DESCENDING
from typing import Dict, Optional, Any

from db.mongo import get_collection

conversations = get_collection("conversations")
conversations.create_index([("last_interacted", DESCENDING)])

def now_utc():
    return datetime.now(timezone.utc)

def create_new_conv_id()-> str:
    return str(uuid.uuid4())

def create_new_conversation(title: str,role: str, content: Optional[str] = None) -> str:
    conv_id = create_new_conv_id()
    time = now_utc()
    doc ={
        "_id": conv_id,
        "title": title,
        "messages":[],
        "last_interacted" : time
    }

    if role and content:
        doc["messages"].append({
            "role": role,
            "content": content,
            "ts" : time
        })
    conversations.insert_one(doc)
    return conv_id

def add_message(conv_id: str, role: str, content: str) -> bool:
    time = now_utc()
    res = conversations.update_one(
        {"_id": conv_id},
        {"$push": {"messages": {"role": role, "content": content}},
        "$set": {"last_interacted": time}
        })
    return res.matched_count ==1

def get_conversation(conv_id: str) -> Optional[Dict[str,Any]]:
    ts = now_utc()
    doc = conversations.find_one_and_update(
        {"_id": conv_id},
        {"$set": {"last_interacted": ts}},
        return_document=True
    )
    return doc

def get_all_conversations() -> Dict[str,str]:
    cursor = conversations.find({}, {"title": 1}).sort("last_interacted", DESCENDING)
    return {doc["_id"]: doc["title"] for doc in cursor}



# --- Example usage ---

# For a new conversation (with the first message):
#conv_id = create_new_conversation(title="Intro to Deep Learning", role="user", content="What is DL?")
#add_message(conv_id, "assistant", "Answer for DL query")
#print(get_conversation(conv_id))
#print(get_all_conversations())
#
# # For an existing conversation:
# add_message(conv_id, "user", "What is ML?")
# add_message(conv_id, "assistant", "Answer for ML query")
# print(get_conversation(conv_id))
# print(get_all_conversations())
#
# # # For a new conversation (with a different title and first message):
# conv_id2 = create_new_conversation(title="Intro to Generative AI", role="user", content="What is Generative AI?")
# add_message(conv_id2, "assistant", "Answer for Generative AI query")
# print(get_conversation(conv_id2))
# print(get_all_conversations())