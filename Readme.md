Python Environment Setup and Django API Interaction

1. Setting up Python 3.11 on your Desktop
   Download and Install Python 3.11:

Download the Python 3.11 installer from the official website: Python Downloads

During installation, make sure to select the option to Add Python to PATH.

Install Python in the directory C:/Python311 (or choose your preferred installation directory).

2. Install Python Extension in VSCode
   Open VSCode.

Go to the Extensions view by clicking the square icon on the sidebar or pressing Ctrl+Shift+X.

Search for the Python extension by Microsoft and click Install.

3. Create a Virtual Environment
   Open VSCode and press Ctrl+Shift+P.

Type and select Python: Select Interpreter.

Choose Create a new virtual environment or select an existing one if available (if you already have a .venv in your project directory, you can activate it).

Choose a location for the .venv folder (usually in the root directory of your project).

4. Install Required Dependencies
   Navigate to the folder that contains your manage.py and requirements.txt files in your terminal (use cd command to change the directory).

Install the required packages by running the following command:

bash
Copy
pip install -r requirements.txt 5. Apply Migrations
Run the following commands to apply database migrations:

bash
Copy
python manage.py makemigrations
python manage.py migrate 6. Start the Django Development Server
Start the development server by running:

bash
Copy
python manage.py runserver
Your Django app should now be running on http://127.0.0.1:8000/.

API Requests Using cURL For Get, Update, delete , Post all are same api just change the keywords

1. POST Request to Add a Landlord
   To add a new landlord, you can send a POST request with the following cURL command:

bash
Copy
curl -X POST http://127.0.0.1:8000/api/landlords/ \
 -H "Content-Type: application/json" \
 -d '{
"username": "JohnDoe",
"email": "johndoe@example.com",
"mobile_number": "1234567890",
"is_active": true
}'

2. POST Request to Add a Property
   To add a new property associated with the landlord, you can send another POST request with the following cURL command:

bash
Copy
curl -X POST http://127.0.0.1:8000/api/properties/ \
 -H "Content-Type: application/json" \
 -d '{
"landlord": 1,
"address": "123 Main Street",
"property_name": "Sunset Apartments",
"is_active": true
}' 3. Troubleshooting Missing Columns
If the above cURL requests return an error indicating a missing field, you can check your Django models to ensure that the fields being used in the request exist in the models.py file. Specifically, check for the fields in the Landlord and Property models located in the myapp folder.

# For the Property Home page in which you will send the property id and month and you will the data room, payment, electricity

4. curl -X GET "http://127.0.0.1:8000/api/property-details/1/3/" \
    -H "Content-Type: application/json"
