# Database module for progjournal.

storage = []


def storage_add(date: str, content: str):
	entry = {"date": date, "content": content}
	storage.append(entry)


def storage_get() -> list:
	return storage.copy()
