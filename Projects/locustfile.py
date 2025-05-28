import os
import uuid
import logging
from locust import HttpUser, task, between
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ApiUser(HttpUser):
    wait_time = between(1, 3)    
    host = os.getenv("BASE_URL", "http://127.0.0.1:8000")
    """User class for API load testing with Locust."""
    timeout_duration = 90
    DEBUG_MODE = os.getenv("DEBUG_MODE", "True") == "True"
    api_key = os.getenv("API_KEY")
    item_id = None  # To store dynamically generated item ID

    def on_start(self):
        """Initialize resources or variables before the test starts."""
        self.item_id = str(uuid.uuid4())[:8]  # Generate a unique item ID

    @task
    def run_scenario(self):
        """Run the sequence of operations."""        
        self.create_item()
        self.retrieve_item()
        self.listar_item()
        self.update_item()
        #self.delete_pet()

    def create_item(self):
        """Create a new item."""
        url = f"{self.host}/items"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "api_key": self.api_key,
        }
        payload = {
            "id": self.item_id,
            "name": "Fluffy",           
        }

        with self.client.post(
            url,
            headers=headers,
            json=payload,
            name="Create Item",
            catch_response=True,
            timeout=self.timeout_duration,
        ) as response:
            if response.status_code in [200, 201]:
                response.success()
                if self.DEBUG_MODE:
                    logging.info(f"Item created successfully: {response.text}")
            else:
                response.failure(f"Failed to create item: {response.status_code}")
                if self.DEBUG_MODE:
                    logging.error(f"Request URL: {url}, Response: {response.text}")

    def retrieve_item(self):
        """Retrieve the newly created item."""
        url = f"{self.host}/items/{self.item_id}"
        headers = {
            "Accept": "application/json",
            "api_key": self.api_key,
        }
        payload = {
            "id": self.item_id            
        }

        with self.client.get(
            url,
            headers=headers,
            name="Retrieve item",
            catch_response=True,
            timeout=self.timeout_duration,
        ) as response:
            if response.status_code == 200:
                response.success()
                if self.DEBUG_MODE:
                    logging.info(f"Item retrieved successfully: {response.text}")
            else:
                response.failure(f"Failed to retrieve item: {response.status_code}")
                if self.DEBUG_MODE:
                    logging.error(f"Request URL: {url}, Response: {response.text}")

    def update_item(self):
        """Update the item."""
        url = f"{self.host}/item/{self.item_id}"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "api_key": self.api_key,
        }
        payload = {
            "id": self.item_id,
            "name": "UpdatedFluffy",            
        }

        with self.client.put(
            url,
            headers=headers,
            json=payload,
            name="Update Item",
            catch_response=True,
            timeout=self.timeout_duration,
        ) as response:
            if response.status_code in [200, 201]:
                response.success()
                if self.DEBUG_MODE:
                    logging.info(f"Item updated successfully: {response.text}")
            else:
                response.failure(f"Failed to update item: {response.status_code}")
                if self.DEBUG_MODE:
                    logging.error(f"Request URL: {url}, Response: {response.text}")

    def delete_item(self):
        """Delete the item."""
        url = f"{self.host}/item/{self.item_id}"
        headers = {
            "Accept": "application/json",
            "api_key": self.api_key,
        }

        with self.client.delete(
            url,
            headers=headers,
            name="Delete Item",
            catch_response=True,
            timeout=self.timeout_duration,
        ) as response:
            if response.status_code in [200, 204]:
                response.success()
                if self.DEBUG_MODE:
                    logging.info(f"Item deleted successfully: {response.text}")
            else:
                response.failure(f"Failed to delete item: {response.status_code}")
                if self.DEBUG_MODE:
                    logging.error(f"Request URL: {url}, Response: {response.text}")

    def listar_item(self):
            """Listar Itens"""
            url = f"{self.host}/items/"
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "api_key": self.api_key,
            }

            with self.client.get(
                url,
                headers=headers,                
                name="Listar Items",
                catch_response=True,
                timeout=self.timeout_duration,
            ) as response:
                if response.status_code in [200, 201]:
                    response.success()
                    if self.DEBUG_MODE:
                        logging.info(f"Item listed successfully: {response.text}")
                else:
                    response.failure(f"Failed to list item: {response.status_code}")
                    if self.DEBUG_MODE:
                        logging.error(f"Request URL: {url}, Response: {response.text}")

    def on_stop(self):
        """Clean up resources after the test ends."""
        logging.info("Test completed. Cleaning up resources.")