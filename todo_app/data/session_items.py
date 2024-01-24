from flask import session


class SessionItems:
    def __init__(self):
        self._DEFAULT_ITEMS = [
            { 'id': 1, 'status': 'Not Started', 'title': 'List saved todo items' },
            { 'id': 2, 'status': 'Not Started', 'title': 'Allow new items to be added' }
        ]

    def get_items(self):
        """
        Fetches all saved items from the session.

        Returns:
            list: The list of saved items.
        """
        return session.get('items', self._DEFAULT_ITEMS.copy())


    def get_item(self, id):
        """
        Fetches the saved item with the specified ID.

        Args:
            id: The ID of the item.

        Returns:
            item: The saved item, or None if no items match the specified ID.
        """
        items = self.get_items()
        return next((item for item in items if item['id'] == int(id)), None)


    def add_item(self, title):
        """
        Adds a new item with the specified title to the session.

        Args:
            title: The title of the item.

        Returns:
            item: The saved item.
        """
        items = self.get_items()

        # Determine the ID for the item based on that of the previously added item
        id = items[-1]['id'] + 1 if items else 0

        item = { 'id': id, 'title': title, 'status': 'Not Started' }

        # Add the item to the list
        items.append(item)
        session['items'] = items

        return item
    
    def delete_item(self, id):
        """
        Deletes an item with the specified id to the session.

        Args:
            id: The id of the item.

        """
        id = int(id)
        items = self.get_items()
        deleted = False
        items.remove(items[id-1])
        # Drop ID of following items by 1
        for item in items:
            if item['id'] > id:
                item['id'] = int(item['id']) - 1

        session['items'] = items

        return items


    def save_item(self, item):
        """
        Updates an existing item in the session. If no existing item matches the ID of the specified item, nothing is saved.

        Args:
            item: The item to save.
        """
        existing_items = self.get_items()
        updated_items = [item if item['id'] == existing_item['id'] else existing_item for existing_item in existing_items]

        session['items'] = updated_items

        return item
