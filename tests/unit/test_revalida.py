import requests
import json
import pytest
from geopy.distance import distance

class TestRevalida:

  @pytest.fixture(scope="class")
  def global_data(self):
    return {
      "acceptableRides": [],
      "riderLocation": {},
      "driverLocation": {},
      "timestamp": ""
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
  def test_book_new_ride_error(self):
    url = "http://127.0.0.1:3000/rides"
    payload = json.dumps({})
    response = requests.post(url, data=payload)
    assert response.status_code == 400

  @pytest.mark.flow
  def test_return_acceptable_rides(self, global_data):
    driverId = "dc90aeaf-db59-44c0-b4c0-19fe5dbe360d"
    url = f"http://127.0.0.1:3000/drivers/{driverId}/rides/acceptable"
    response = requests.get(url)
    global_data["acceptableRides"] = json.loads(response.text)
    assert response.status_code == 200

  @pytest.mark.flow
  def test_get_pending_ride_info(self, global_data):
    rideId = global_data["acceptableRides"][0]['rideId']
    url = f"http://127.0.0.1:3000/rides/{rideId}"
    response = requests.get(url)
    state = json.loads(response.text)["state"]
    assert state == "pending"

  @pytest.mark.flow
  def test_get_ride_info_error(self, global_data):
    url = f"http://127.0.0.1:3000/rides/error"
    response = requests.get(url)
    assert response.status_code == 400

  @pytest.mark.flow
  def test_driver_accept_ride(self, global_data):
    driverId = "dc90aeaf-db59-44c0-b4c0-19fe5dbe360d"
    rideId = global_data["acceptableRides"][0]['rideId']
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

  @pytest.mark.flow
  def test_get_accepted_ride_info(self, global_data):
    rideId = global_data["acceptableRides"][0]['rideId']
    url = f"http://127.0.0.1:3000/rides/{rideId}"
    response = requests.get(url)
    state = json.loads(response.text)["state"]
    assert state == "accepted"

  @pytest.mark.location
  def test_driver_update_location(self, global_data):
    driverId = "dc90aeaf-db59-44c0-b4c0-19fe5dbe360d"
    location = {
      "N": "14.505637",
      "W": "-121.289874"
    }
    global_data["driverLocation"] = location
    url = f"http://127.0.0.1:3000/drivers/{driverId}/locations"
    payload = json.dumps({
      "updatedLocation": {
        "N": location["N"],
        "W": location["W"]
      }
    })
    response = requests.put(url, data=payload)
    responseText = json.loads(response.text)
    assert responseText["updatedLocation"]["N"] == location["N"]
    assert responseText["updatedLocation"]["W"] == location["W"]
    assert responseText["createdAt"]
    global_data["timestamp"] = responseText["createdAt"]

  @pytest.mark.location
  def test_driver_get_location(self, global_data):
    driverId = "dc90aeaf-db59-44c0-b4c0-19fe5dbe360d"
    location = global_data["driverLocation"]
    url = f"http://127.0.0.1:3000/drivers/{driverId}"
    response = requests.get(url)
    responseText = json.loads(response.text)
    assert responseText["updatedLocation"]["N"] == location["N"]
    assert responseText["updatedLocation"]["W"] == location["W"]
    assert responseText["createdAt"] == global_data["timestamp"]

  @pytest.mark.location
  def test_rider_update_location(self, global_data):
    riderId = "8B0A79F0-8E4E-4523-A335-2EB98305354F"
    location = {
      "N": "14.503529",
      "W": "-121.288397"
    }
    global_data["riderLocation"] = location
    url = f"http://127.0.0.1:3000/riders/{riderId}/locations"
    payload = json.dumps({
      "currentLocation": {
        "N": location["N"],
        "W": location["W"]
      }
    })
    response = requests.put(url, data=payload)
    responseText = json.loads(response.text)
    assert responseText["currentLocation"]["N"] == location["N"]
    assert responseText["currentLocation"]["W"] == location["W"]
    assert responseText["lastActive"]
    global_data["timestamp"] = responseText["lastActive"]

  @pytest.mark.location
  def test_rider_get_location(self, global_data):
    riderId = "8B0A79F0-8E4E-4523-A335-2EB98305354F"
    location = global_data["riderLocation"]
    url = f"http://127.0.0.1:3000/riders/{riderId}"
    response = requests.get(url)
    responseText = json.loads(response.text)
    assert responseText["currentLocation"]["N"] == location["N"]
    assert responseText["currentLocation"]["W"] == location["W"]
    assert responseText["lastActive"] == global_data["timestamp"]

  @pytest.mark.location
  def test_get_distance(self, global_data):
    riderId = "8B0A79F0-8E4E-4523-A335-2EB98305354F"
    driverId = "dc90aeaf-db59-44c0-b4c0-19fe5dbe360d"
    driverLocation = global_data["driverLocation"]
    riderLocation = global_data["riderLocation"]
    payload = json.dumps({
      "riderId": riderId
    })
    url = f"http://127.0.0.1:3000/drivers/{driverId}/distance"
    response = requests.put(url, payload)
    responseText = json.loads(response.text)
    dist = distance((driverLocation["N"], driverLocation["W"]),(riderLocation["N"], riderLocation["W"])).m
    print(responseText["distance"])
    assert responseText["distance"] == dist