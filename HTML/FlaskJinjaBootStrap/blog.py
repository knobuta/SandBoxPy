import requests

blog_url = "https://api.npoint.io/674f5423f73deab1e9a7"

class Blog:

    def __init__(self):
        """
        Constructor to initialize the Blog class and fetch blog data from the API.
        Attributes:
        - response (requests.Response): The response object from the API request.
        """
        self.response = requests.get(blog_url)

    def get_blog_json(self):
        """
        Method to retrieve all blog posts from the API response.
        Returns:
            list: A list of blog posts in JSON format.
        """
        #print(self.response.json())  # For debugging
        return self.response.json()