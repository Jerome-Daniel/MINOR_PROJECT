import numpy as np
from scipy.spatial.distance import cosine

class PersonalizedLearningModel:
    def __init__(self, resource_data, resource_links):
        self.resource_data = resource_data
        self.resource_links = resource_links

    def recommend_resources(self, math, science, english):
        # Initialize an array to store recommendations
        recommendations = []

        # Calculate the cosine similarity between user marks and resource data
        for i, resource_vector in enumerate(self.resource_data):
            similarity = cosine([math, science, english], resource_vector)
            recommendations.append((i, similarity))

        # Sort the recommendations by similarity (highest to lowest)
        recommendations.sort(key=lambda x: x[1], reverse=True)

        return recommendations[:10]  # Return the top 10 recommendations

    def get_resource_links(self, recommendations):
        resource_links = []
        for i, _ in recommendations:
            resource_links.append({
                'math_resource_link': self.resource_links[i]['math_resource_link'],
                'science_resource_link': self.resource_links[i]['science_resource_link'],
                'english_resource_link': self.resource_links[i]['english_resource_link']
            })
        return resource_links
