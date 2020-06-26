import requests
import json
import pytest
from geopy.distance import distance

class TestRevalida:

  @pytest.fixture(scope="class")
  def global_data(self):
    return {
      "url": "https://dfwfckxo51.execute-api.ap-southeast-1.amazonaws.com/Prod",
      # "url": "http://127.0.0.1:3000",
      "acceptableRides": [],
      "acceptedRideId": "",
      "riderLocation": {},
      "driverLocation": {},
      "timestamp": ""
    }

  def test_rider_update_location(self, global_data):
    riderId = "8B0A79F0-8E4E-4523-A335-2EB98305354F"
    location = {
      "N": "14.503529",
      "W": "-121.288397"
    }
    global_data["riderLocation"] = location
    url = global_data["url"]+f"/riders/{riderId}/locations"
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

  def test_rider_get_location(self, global_data):
    riderId = "8B0A79F0-8E4E-4523-A335-2EB98305354F"
    location = global_data["riderLocation"]
    url = global_data["url"]+f"/riders/{riderId}"
    response = requests.get(url)
    responseText = json.loads(response.text)
    assert responseText["currentLocation"]["N"] == location["N"]
    assert responseText["currentLocation"]["W"] == location["W"]
    assert responseText["lastActive"] == global_data["timestamp"]

  def test_book_new_ride(self, global_data):
    url = global_data["url"]+"/rides"
    payload = json.dumps({
      "riderId": "8B0A79F0-8E4E-4523-A335-2EB98305354F",
      "bookingLocation": {
        "N": "14.503529",
        "W": "-121.288397"
      },
      "targetLocation": {
        "N": "14.505637",
        "W": "-121.289874"
      }
    })
    response = requests.post(url, data=payload)
    global_data["acceptedRideId"] = json.loads(response.text)["rideId"]
    assert response.status_code == 200

  def test_book_new_ride_error(self, global_data):
    url = global_data["url"]+"/rides"
    payload = json.dumps({})
    response = requests.post(url, data=payload)
    assert response.status_code == 400

  def test_return_acceptable_rides(self, global_data):
    driverId = "dc90aeaf-db59-44c0-b4c0-19fe5dbe360d"
    url = global_data["url"]+f"/drivers/{driverId}/rides/acceptable"
    response = requests.get(url)
    global_data["acceptableRides"] = json.loads(response.text)
    assert response.status_code == 200

  def test_get_pending_ride_info(self, global_data):
    rideId = global_data["acceptableRides"][0]['rideId']
    url = global_data["url"]+f"/rides/{rideId}"
    response = requests.get(url)
    state = json.loads(response.text)["state"]
    assert state == "pending"

  def test_get_ride_info_error(self, global_data):
    url = global_data["url"]+f"/rides/error"
    response = requests.get(url)
    assert response.status_code == 400

  def test_driver_accept_ride(self, global_data):
    driverId = "dc90aeaf-db59-44c0-b4c0-19fe5dbe360d"
    rideId = global_data["acceptableRides"][0]['rideId']
    url = global_data["url"]+f"/drivers/{driverId}/rides/{rideId}/accept"
    location = {
      "N": "14.505637",
      "W": "-121.289874"
    }
    payload = json.dumps({
      "acceptLocation": location
    })
    response = requests.put(url, data=payload)
    responseText = json.loads(response.text)
    assert responseText["rideId"] == rideId
    assert responseText["acceptLocation"]["N"] == location["N"]
    assert responseText["acceptLocation"]["W"] == location["W"]
    assert responseText["createdAt"]

  def test_get_accepted_ride_info(self, global_data):
    rideId = global_data["acceptableRides"][0]['rideId']
    url = global_data["url"]+f"/rides/{rideId}"
    response = requests.get(url)
    state = json.loads(response.text)["state"]
    assert state == "accepted"

  def test_driver_update_location(self, global_data):
    driverId = "dc90aeaf-db59-44c0-b4c0-19fe5dbe360d"
    location = {
      "N": "14.505637",
      "W": "-121.289874"
    }
    global_data["driverLocation"] = location
    url = global_data["url"]+f"/drivers/{driverId}/locations"
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

  def test_driver_get_location(self, global_data):
    driverId = "dc90aeaf-db59-44c0-b4c0-19fe5dbe360d"
    location = global_data["driverLocation"]
    url = global_data["url"]+f"/drivers/{driverId}"
    response = requests.get(url)
    responseText = json.loads(response.text)
    assert responseText["updatedLocation"]["N"] == location["N"]
    assert responseText["updatedLocation"]["W"] == location["W"]
    assert responseText["createdAt"] == global_data["timestamp"]
  
  def test_get_distance(self, global_data):
    riderId = "8B0A79F0-8E4E-4523-A335-2EB98305354F"
    driverId = "dc90aeaf-db59-44c0-b4c0-19fe5dbe360d"
    driverLocation = global_data["driverLocation"]
    riderLocation = global_data["riderLocation"]
    payload = json.dumps({
      "riderId": riderId
    })
    url = global_data["url"]+f"/drivers/{driverId}/distance"
    response = requests.put(url, payload)
    responseText = json.loads(response.text)
    dist = distance((driverLocation["N"], driverLocation["W"]),(riderLocation["N"], riderLocation["W"])).m
    assert responseText["distance"] == dist

  def test_driver_update_location_near_passenger(self, global_data):
    driverId = "dc90aeaf-db59-44c0-b4c0-19fe5dbe360d"
    location = {
      "N": "14.503483",
      "W": "-121.288362"
    }
    global_data["driverLocation"] = location
    url = global_data["url"]+f"/drivers/{driverId}/locations"
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

  def test_get_in_progress_ride_info(self, global_data):
    rideId = global_data["acceptedRideId"]
    url = global_data["url"]+f"/rides/{rideId}"
    response = requests.get(url)
    state = json.loads(response.text)["state"]
    assert state == "in_progress"

  def test_driver_update_location_near_target(self, global_data):
    driverId = "dc90aeaf-db59-44c0-b4c0-19fe5dbe360d"
    location = {
      "N": "14.505612",
      "W": "-121.289897"
    }
    global_data["driverLocation"] = location
    url = global_data["url"]+f"/drivers/{driverId}/locations"
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

  def test_get_complete_success_ride_info(self, global_data):
    rideId = global_data["acceptedRideId"]
    url = global_data["url"]+f"/rides/{rideId}"
    response = requests.get(url)
    state = json.loads(response.text)["state"]
    assert state == "complete_success"