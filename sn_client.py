import os
import httpx
from dotenv import load_dotenv

load_dotenv()

INSTANCE = os.getenv("SN_INSTANCE")
USER = os.getenv("SN_USERNAME")
PASSWORD = os.getenv("SN_PASSWORD")


class ServiceNowClient:

    def __init__(self):
        self.auth = (USER, PASSWORD)

    async def get_incidents(self, limit=10):

        url = (
            f"{INSTANCE}/api/now/table/incident"
            f"?sysparm_limit={limit}"
        )

        async with httpx.AsyncClient() as client:
            response = await client.get(
                url,
                auth=self.auth,
                headers={"Accept": "application/json"}
            )

        response.raise_for_status()

        return response.json()["result"]

    async def get_incident(self, incident_number):

        url = (
            f"{INSTANCE}/api/now/table/incident"
            f"?sysparm_query=number={incident_number}&sysparm_display_value=true"
        )

        async with httpx.AsyncClient() as client:
            response = await client.get(
                url,
                auth=self.auth
            )

        response.raise_for_status()

        result = response.json()["result"]
        print(f"get_incident result: {result[0] if result else None}")
        return result[0] if result else None

    async def create_incident(
        self,
        short_description,
        description=""
    ):

        url = f"{INSTANCE}/api/now/table/incident"

        payload = {
            "short_description": short_description,
            "description": description
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                auth=self.auth,
                json=payload
            )

        response.raise_for_status()

        return response.json()["result"]

    async def search_kb(self, keyword):

        url = (
            f"{INSTANCE}/api/now/table/kb_knowledge"
            f"?sysparm_query=short_descriptionLIKE{keyword}"
        )

        async with httpx.AsyncClient() as client:
            response = await client.get(
                url,
                auth=self.auth
            )

        response.raise_for_status()

        return response.json()["result"]

    async def get_change_requests(self):

        url = (
            f"{INSTANCE}/api/now/table/change_request"
            f"?sysparm_limit=20"
        )

        async with httpx.AsyncClient() as client:
            response = await client.get(
                url,
                auth=self.auth
            )

        response.raise_for_status()

        return response.json()["result"]