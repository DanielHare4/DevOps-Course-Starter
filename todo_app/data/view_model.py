class ViewModel:
    def __init__(self, items):
        self._items = items
 
    @property
    def items(self):
        return sorted(self._items, key=lambda x: x.id)
    
    @property
    def done_items(self):
        return [x for x in self._items if x.status == 'Done']

    @property
    def todo_items(self):
        return [x for x in self._items if x.status == 'To Do']
