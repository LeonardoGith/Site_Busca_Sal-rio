import unittest
import json
from my_flask_app import app  # Import your Flask app (use your actual filename)

class TestUserAPI(unittest.TestCase):
    def setUp(self):
        # Create a test client for the Flask app
        self.client = app.test_client()
        self.client.testing = True

    def test_get_all_users(self):
        # Send a GET request to the /api/usuarios endpoint
        response = self.client.get('/api/usuarios')
        self.assertEqual(response.status_code, 200)
        # Ensure the response is in JSON format
        self.assertEqual(response.content_type, "application/json")
        # Check that the response data is a list
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_add_user(self):
        # Send a POST request to the /api/usuarios endpoint
        new_user = {
            "nome": "John Doe",
            "email": "johndoe@example.com"
        }
        response = self.client.post(
            '/api/usuarios',
            data=json.dumps(new_user),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        # Check that the message returned is correct
        data = json.loads(response.data)
        self.assertIn("message", data)
        self.assertEqual(data["message"], "Usuário adicionado com sucesso!")

    def test_update_user(self):
        # Send a PUT request to update a user
        updated_user = {
            "nome": "John Doe Updated",
            "email": "johnupdated@example.com"
        }
        response = self.client.put(
            '/api/usuarios/1',  # Replace with a valid user ID from your database
            data=json.dumps(updated_user),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        # Check that the message returned is correct
        data = json.loads(response.data)
        self.assertIn("message", data)
        self.assertEqual(data["message"], "Usuário atualizado com sucesso!")

    def test_delete_user(self):
        # Send a DELETE request to delete a user
        response = self.client.delete('/api/usuarios/1')  # Replace with a valid user ID from your database
        self.assertIn(response.status_code, [200, 404])  # Ensure 200 or 404 is returned based on if the user exists
        # Check that the message returned is correct
        data = json.loads(response.data)
        if response.status_code == 200:
            self.assertEqual(data["message"], "Usuário excluído com sucesso!")
        elif response.status_code == 404:
            self.assertEqual(data["message"], "Usuário não encontrado.")

if __name__ == '__main__':
    unittest.main()
