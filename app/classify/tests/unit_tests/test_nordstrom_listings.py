import sys, os
sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/../../../.."))

from fastapi.testclient import TestClient
from app.schemas import *
from app.main import *
import json

client = TestClient(app)

def test_nordstrom_listings_successful_response():
  targets = [
    "app/classify/tests/data/targets/nordstrom-listings-successful.json"
  ]

  for target_filename in targets:
    with open(target_filename) as json_file:
      target = json.load(json_file)
    r = client.post("/classify", json=target)

    result_filename = target['mock_name'].replace('.json','-result.json')
    result_filename = result_filename.replace('/targets/', '/results/')
    print(json_file)

    with open(result_filename) as json_file:
      result = json.load(json_file)

    assert r.status_code == 200
    assert r.json() == result
    assert len(r.json()['results']) > 0
    assert ("message" not in r.json()['results'][0])