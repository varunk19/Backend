
# Advanced Flight Navigation System (AFNS) BACKEND

It is a navigation system to identify optimal flight paths considering factors like duration and weather and average altitude in the route. Additionally, it provides real-time risk assessment and suggests alternative routes to pilots, airlines, and airport authorities for safe and efficient navigation.

`This is the BACKEND part of the app`
## Tech Stack

**Server:** Flask, pytest

**Database:** SQLAlchemy

**ML Libraries:** Pandas, Numpy, networkx

## Algorithm

To find the best route between two airports we have used Depth First Search Algorithn.

## Deployment

To deploy this project run

```bash
  pip install -r requirements.txt
```
```bash
  python -m app
```


## API Reference

#### login

```http
  /login
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `user_id,password` | `string,string` | **Required**. user_id, password |

#### Create flight_plan

```http
  /flight_plan
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `flight_plan`      | `json file` | **Required**. flight_plan |


#### Edit_flight_plan

```http
  /edit_flight_plan
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `plan_id`      | `integer` | **Required**. plan_id |


#### Fetch_flight_plan

```http
  /fetch_flight_plan
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `flight_id`      | `integer` | **Required**. flight_id |


#### Find_best_route

```http
  /find_best_route
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `source, destination, excluded_airport, included_airport`      | `list` | **Required**. flight_data |


#### Flight_plan_alert

```http
  /flight_plan/status
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `plan_id`      | `integer` | **Required**. plan_id |





