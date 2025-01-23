import requests
import json

url = "https://app.toplogger.nu/graphql"

headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:134.0) Gecko/20100101 Firefox/134.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Referer": "https://app.toplogger.nu/en-us/boulder-brighton/boulders",
    "x-app-locale": "en-us",
    "Origin": "https://app.toplogger.nu",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Priority": "u=4",
    "TE": "trailers",
}


full_payload = [
    {
        "operationName": "climbs",
        "variables": {"gymId": "hf64ufvvw8s60c3scpqcj", "climbType": "boulder"},
        "query": "query climbs($gymId: ID!, $climbType: ClimbType!, $isReported: Boolean, $userId: ID, $compRoundId: ID) {\n  climbs(\n    gymId: $gymId\n    climbType: $climbType\n    isReported: $isReported\n    compRoundId: $compRoundId\n  ) {\n    data {\n      ...climb\n      ...climbWithClimbUser\n      ...climbWithCompRoundClimb\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment climbGroupClimb on ClimbGroupClimb {\n  id\n  climbGroupId\n  order\n  __typename\n}\n\nfragment climbUser on ClimbUser {\n  id\n  climbId\n  grade\n  rating\n  project\n  votedRenew\n  tickType\n  totalTries\n  triedFirstAtDate\n  tickedFirstAtDate\n  updatedAt\n  compClimbUser(compRoundId: $compRoundId) {\n    id\n    points\n    pointsJson\n    tickType\n    __typename\n  }\n  __typename\n}\n\nfragment compRoundClimb on CompRoundClimb {\n  id\n  points\n  pointsJson\n  leadRequired\n  __typename\n}\n\nfragment climb on Climb {\n  id\n  climbType\n  positionX\n  positionY\n  gradeAuto\n  grade\n  gradeVotesCount\n  gradeUsersVsAdmin\n  picPath\n  label\n  name\n  zones\n  remarksLoc\n  suitableForKids\n  clips\n  holds\n  height\n  overhang\n  autobelay\n  leadEnabled\n  leadRequired\n  ratingsAverage\n  ticksCount\n  inAt\n  outAt\n  outPlannedAt\n  order\n  setterName\n  climbSetters {\n    id\n    gymAdmin {\n      id\n      name\n      picPath\n      __typename\n    }\n    __typename\n  }\n  wallId\n  wall {\n    id\n    nameLoc\n    labelX\n    labelY\n    __typename\n  }\n  wallSectionId\n  wallSection {\n    id\n    name\n    routesEnabled\n    positionX\n    positionY\n    __typename\n  }\n  holdColorId\n  holdColor {\n    id\n    color\n    colorSecondary\n    nameLoc\n    order\n    __typename\n  }\n  climbGroupClimbs {\n    ...climbGroupClimb\n    __typename\n  }\n  climbTagClimbs {\n    id\n    climbTagId\n    order\n    climbTag {\n      id\n      type\n      nameLoc\n      icon\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment climbWithClimbUser on Climb {\n  id\n  climbUser(userId: $userId) {\n    ...climbUser\n    __typename\n  }\n  __typename\n}\n\nfragment climbWithCompRoundClimb on Climb {\n  id\n  compRoundClimb(compRoundId: $compRoundId) {\n    ...compRoundClimb\n    __typename\n  }\n  __typename\n}",
    },
    {
        "operationName": "gymForClimbs",
        "variables": {"gymId": "hf64ufvvw8s60c3scpqcj"},
        "query": "query gymForClimbs($gymId: ID) {\n  gym(gymId: $gymId) {\n    ...gymForClimbs\n    __typename\n  }\n}\n\nfragment holdColor on HoldColor {\n  id\n  nameLoc\n  color\n  colorSecondary\n  __typename\n}\n\nfragment wall on Wall {\n  id\n  nameLoc\n  idOnFloorplan\n  height\n  overhang\n  bouldersEnabled\n  routesEnabled\n  climbTypeDefault\n  labelX\n  labelY\n  order\n  __typename\n}\n\nfragment wallSection on WallSection {\n  id\n  name\n  clips\n  height\n  overhang\n  bouldersEnabled\n  routesEnabled\n  climbTypeDefault\n  leadEnabled\n  leadRequired\n  autobelay\n  positionX\n  positionY\n  wallId\n  wall {\n    id\n    nameLoc\n    labelX\n    labelY\n    __typename\n  }\n  __typename\n}\n\nfragment setter on GymAdmin {\n  id\n  name\n  picPath\n  __typename\n}\n\nfragment climbGroupForIcon on ClimbGroup {\n  id\n  color\n  climbGroupBy\n  holdColor {\n    id\n    color\n    colorSecondary\n    __typename\n  }\n  __typename\n}\n\nfragment climbGroup on ClimbGroup {\n  id\n  nameLoc\n  descriptionLoc\n  color\n  climbGroupBy\n  climbType\n  holdColorId\n  holdColor {\n    id\n    color\n    colorSecondary\n    __typename\n  }\n  ...climbGroupForIcon\n  visible\n  order\n  __typename\n}\n\nfragment climbTag on ClimbTag {\n  id\n  type\n  nameLoc\n  icon\n  __typename\n}\n\nfragment gymForClimbs on Gym {\n  id\n  markBoulderNewDays\n  markRouteNewDays\n  markBoulderOutSoonDays\n  markRouteOutSoonDays\n  settingsLogBoulders\n  settingsLogRoutes\n  holdColors {\n    ...holdColor\n    __typename\n  }\n  walls {\n    ...wall\n    __typename\n  }\n  wallSections {\n    ...wallSection\n    __typename\n  }\n  setters {\n    ...setter\n    __typename\n  }\n  climbGroups {\n    ...climbGroup\n    __typename\n  }\n  climbTags {\n    ...climbTag\n    __typename\n  }\n  __typename\n}",
    },
]

optimised_payload = [
    {
        "operationName": "climbs",
        "variables": {"gymId": "hf64ufvvw8s60c3scpqcj", "climbType": "boulder"},
        "query": "query climbs($gymId: ID!, $climbType: ClimbType!) {\n  climbs(\n    gymId: $gymId\n    climbType: $climbType\n  ) {\n    data {\n      grade\n      gradeVotesCount\n      ratingsAverage\n      holdColor {\n        nameLoc\n      }\n      wall {\n        nameLoc} ticksCount\n  inAt\n  outPlannedAt\n \n }\n  }\n}",
    }
]


# Sending the POST request
response = requests.post(url, headers=headers, json=optimised_payload)

# Check if the request was successful (HTTP status code 200 means success)
if response.status_code == 200:
    data = response.json()
    print(json.dumps(data, indent=4))

    with open("data/boulders.json", "w") as file:
        json.dump(data, file, indent=4)
else:
    print(f"Request failed with status code: {response.status_code}")
    print(response.text)
