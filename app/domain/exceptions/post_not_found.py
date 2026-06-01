class PostNotFoundException(Exception):
    def __init__(self, post_id: int):
        self.message = f"Post with id {post_id} not found"
        super().__init__(self.message)
