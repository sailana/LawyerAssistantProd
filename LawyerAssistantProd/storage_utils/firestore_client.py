import firebase_admin
from firebase_admin import firestore
import logging
logger = logging.getLogger(__name__)

class FirestoreClient:
	def __init__(self, project_id: str = "superb-blend-391516"):
		if not firebase_admin._apps:
			firebase_admin.initialize_app(options={"projectId": project_id})
		self.client = firestore.client()

	def get_collection(self, collection_name="laborcode_ai"):
		return self.client.collection(collection_name)

	def get_allowed_users(self) -> list:
		return self.get_collection().document("allowed_users").get().to_dict()["usernames"]
	
	def add_user_to_allowed(self, username:str=""):
		if username.strip() == "":
			return
		allowed_users = self.get_allowed_users()
		if username not in allowed_users:
			allowed_users.append(username)
			logging.info(f"Adding {username} to allowed")
			self.get_collection().document("allowed_users").update({"usernames": allowed_users})
			logging.info(f"Added {username} to allowed")
	
	def remove_user_from_allowed(self, username:str=""):
		if username.strip() == "":
			return
		allowed_users = self.get_allowed_users()
		if username in allowed_users:
			allowed_users.remove(username)
			logging.info(f"Removing {username} from allowed")
			self.get_collection().document("allowed_users").update({"usernames": allowed_users})
			logging.info(f"Removed {username} from allowed")
	
	def add_chat_to_chats(self, chat_id: str, chat_metadata_with_history: dict):
		if chat_id is None or chat_id.strip() == "":
			logger.error("Chat id is empty")
			return
		logger.info("Updating chats started")
		self.get_collection().document("chats").update({chat_id: chat_metadata_with_history})
		logger.info("Updating chats completed")




# client = FirestoreClient(project_id="superb-blend-391516")
# print(client.get_allowed_users())
# client.add_user_to_allowed("test")
# print(client.get_allowed_users())
# client.remove_user_from_allowed("test")
# print(client.get_allowed_users())