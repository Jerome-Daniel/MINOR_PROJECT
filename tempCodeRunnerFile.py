from flask import Flask, render_template, request
import numpy as np
from scipy.spatial.distance import cosine

app = Flask(__name__)

# Load resource data
resource_data = np.loadtxt('C:/Users/Jerome Daniel/Downloads/Research Papers/resource_data.csv', delimiter=',', skiprows=1)

# Load resource links
resource_links = np.genfromtxt('J:/resource_links.csv', delimiter=',', dtype='str', skip_header=1)

# Create the personalized learning model
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
                'math_resource_link': self.resource_links[i][0],  # Assuming math resource link is in the first column
                'science_resource_link': self.resource_links[i][1],  # Assuming science resource link is in the second column
                'english_resource_link': self.resource_links[i][2]  # Assuming English resource link is in the third column
            })
        return resource_links

model = PersonalizedLearningModel(resource_data, resource_links)
@app.route('/',methods = ['GET'])
def homepage():
    return render_template("index.html")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        math = float(request.form.get('math'))
        science = float(request.form.get('science'))
        english = float(request.form.get('english'))

        recommendations = model.recommend_resources(math, science, english)

        # Extract resource links based on the recommendation
        resource_links = model.get_resource_links(recommendations)

        # Adjust the index of recommendations to start from 1
        recommendations = [(i+1, similarity) for i, similarity in recommendations]
        
        print(resource_links)
        print(recommendations)
        return render_template('recommendations.html', recommendations=recommendations, resource_links=resource_links)
        
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
