class Controller:
    repository = None

    def get(self):
        return self.repository.get_data()

    def create(self, values: list):
        self.repository.insert_data(values)

    def put(self):
        pass

    def drop(self):
        pass
