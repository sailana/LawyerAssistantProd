import firebase_admin
from firebase_admin import firestore

class FirestoreClient:
	def __init__(self, project_id):
		firebase_admin.initialize_app(options={"projectId": project_id})
		self.client = firestore.client()

	def get_collection(self, collection_name):
		return self.client.collection(collection_name)


client = FirestoreClient(project_id="superb-blend-391516")
collection = client.get_collection(collection_name="allowed_users")

data = collection.document.get().to_dict()
print(data)