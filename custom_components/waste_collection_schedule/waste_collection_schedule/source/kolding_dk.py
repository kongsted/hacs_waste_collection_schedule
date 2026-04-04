from datetime import datetime

import requests
from waste_collection_schedule import Collection  # type: ignore[attr-defined]

TITLE = "Kolding Kommune"
DESCRIPTION = "Source for Kolding Kommune waste collection schedule"
URL = "https://kolding.dk"
TEST_CASES = {
    "TestCase1": {
        "id": "00006ac8-0002-0001-4164-647265737320",
    },
    "TestCase2": {
        "id": "00008d18-0002-0001-4164-647265737320",
    },
    "TestCase3": {
        "id": "00006643-0002-0001-4164-647265737320",
    },
}

ICON_MAP = {
    "REST-MAD": "mdi:trash-can",
    "PAP-PAPIR": "mdi:newspaper",
    "PLAST-GLAS-METAL": "mdi:recycle",
    "TEKSTIL": "mdi:recycle",
    "MADAFFALD": "mdi:food",
    "RESTAFFALD": "mdi:trash-can",
    "FARLIGT-AFFALD": "mdi:biohazard",
}

HOW_TO_GET_ARGUMENTS_DESCRIPTION = {
    "en": """
    To get your UUID (Geolocation) ID:
    1. Go to the www.kolding.dk/mitaffald.
    2. or go directly to : https://kolding.infovision.dk/public/selectaddress
    3. Search for your address.
    4. You will find your ID in URL i.e. : https://kolding.infovision.dk/public/address/00007b8d-0002-0001-4164-647265737320
    5. The ID should be a UUID format like: `00007b8d-0002-0001-4164-647265737320`
    """,
}


class Source:
    def __init__(self, id: str):
        self._id = id
        self._api_url = f"https://koldingivapi.infovision.dk/api/publiccitizen/container/address/active/{self._id}"

    def fetch(self):
        headers = {
            "accept": "application/json, text/plain, */*",
            "publicaccesstoken": "__NetDialogCitizenPublicAccessToken__",
            "User-Agent": "Mozilla/5.0",
        }

        response = requests.get(self._api_url, headers=headers)
        response.raise_for_status()
        containers = response.json()

        entries = []

        for container in containers:
            name = container.get("containerType", {}).get(
                "description", "Ukendt beholder"
            )
            collect_dates = container.get("collectDates", [])

            # Renodjurs-style matching logic - most specific first
            lower_name = name.lower()
            fraktion = "Ukendt"
            icon = None

            if "farligt affald" in lower_name or "miljøkasse" in lower_name:
                fraktion = "Farligt affald"
                icon = ICON_MAP.get("FARLIGT-AFFALD")
            elif "rest" in lower_name and "mad" in lower_name:
                fraktion = "Rest- og Madaffald"
                icon = ICON_MAP.get("REST-MAD")
            elif "drikkekarton" in lower_name and "plast" in lower_name:
                fraktion = "Plast og mad- og drikkekartoner"
                icon = ICON_MAP.get("PLAST-GLAS-METAL")
            elif "metal" in lower_name and "papir" in lower_name:
                fraktion = "Pap/papir og glas/metal"
                icon = ICON_MAP.get("PLAST-GLAS-METAL")
            elif "tekstil" in lower_name:
                fraktion = "Tekstilaffaldspose"
                icon = ICON_MAP.get("TEKSTIL")

            for date_int in collect_dates:
                date_str = str(date_int)
                pickup_date = datetime.strptime(date_str, "%Y%m%d").date()

                entries.append(
                    Collection(
                        date=pickup_date,
                        t=fraktion,
                        icon=icon,
                    )
                )

        return entries