import requests
import json
import pytest

class TestRevalida:

  @pytest.fixture(scope="class")
  def global_data(self):
    return {
      "rideId": ""
    }

  @pytest.mark.flow
  def test_book_new_ride(self, global_data):
    url = "http://127.0.0.1:3000/rides"
    payload = json.dumps({
      "riderId": "8B0A79F0-8E4E-4523-A335-2EB98305354F",
      "bookingLocation": {
        "N": "40.446",
        "W": "79.982"
      },
      "targetLocation": {
        "N": "14.6323596",
        "W": "121.0371381"
      }
    })
    response = requests.post(url, data=payload)
    global_data["rideId"] = json.loads(response.text)["rideId"]
    assert response.status_code == 200

  @pytest.mark.flow
  def test_driver_accept_ride(self, global_data):
    driverId = "dc90aeaf-db59-44c0-b4c0-19fe5dbe360d"
    rideId = global_data["rideId"]
    url = f"http://127.0.0.1:3000/drivers/{driverId}/rides/{rideId}/accept"
    payload = json.dumps({
      "acceptLocation": {
        "N": "40.446",
        "W": "79.982"
      }
    })
    response = requests.put(url, data=payload)
    responseText = json.loads(response.text)
    assert responseText["rideId"] == rideId
    assert responseText["acceptLocation"]["N"] == "40.446"
    assert responseText["acceptLocation"]["W"] == "79.982"
    assert responseText["createdAt"]

  def test_get_ride_info(self, global_data):
    rideId = global_data["rideId"]
    url = f"http://127.0.0.1:3000/rides/{rideId}"
    response = requests.get(url)
    state = json.loads(response.text)["state"]
    assert state == "pending"

  @pytest.mark.location
  def test_driver_update_location(self):
    driverId = "dc90aeaf-db59-44c0-b4c0-19fe5dbe360d"
    url = f"http://127.0.0.1:3000/drivers/{driverId}/locations"
    payload = json.dumps({
      "updatedLocation": {
        "N": "40.446",
        "W": "79.982"
      }
    })
    response = requests.put(url, data=payload)
    responseText = json.loads(response.text)
    assert responseText["updatedLocation"]["N"] == "40.446"
    assert responseText["updatedLocation"]["W"] == "79.982"
    assert responseText["createdAt"]

  @pytest.mark.location
  def test_rider_update_location(self):
    riderId = "8B0A79F0-8E4E-4523-A335-2EB98305354F"
    url = f"http://127.0.0.1:3000/riders/{riderId}/locations"
    payload = json.dumps({
      "currentLocation": {
        "N": "40.446",
        "W": "79.982"
      }
    })
    response = requests.put(url, data=payload)
    responseText = json.loads(response.text)
    assert responseText["currentLocation"]["N"] == "40.446"
    assert responseText["currentLocation"]["W"] == "79.982"
    assert responseText["lastActive"]