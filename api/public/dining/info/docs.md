# Dining
The eatery names are 'ratty' or 'vdub'. Currently, only the Ratty and VDub are supported.

## Request Dining Menu
**Endpoint**: /dining/schedule

**Parameters**:

| Parameter |  Required | Value                               | Type                 |
|-----------|-----------|-------------------------------------|----------------------|
| `eatery`  | yes       | either 'ratty' or 'vdub'            | string               |
| `year`    | no        | the current year will be inferred   | integer              |
| `month`   | no        | the current month will be inferred  | integer between 0-12 |
| `day`     | no        | the current day will be inferred    | integer between 0-31 |
| `hour`    | no        | the current hour will be inferred   | integer between 0-23 |

**Returns**: The number of menus found and a list of those menus in the form:

```javascript
{'num_results': INTEGER,
 'results': [
   {
     'dining_hall': STRING,
     'daily_schedule': [...],
     'weekly_schedule': [...],
     'special_data': [...],
   }
 }
```

**daily_schedule** will appear in the form
```javascript
{
    "meal_title": STRING,
    "timespan": {
      "start_time": STRING, // Isoformat
      "end_time": STRING // Isoformat
    }
    "menu": [
      {
        "dish_name": STRING,
        "dish_description": STRING,
        "station": STRING,
        "vegetarian": BOOLEAN,
        "timespan": {
          "start_time": STRING, // Isoformat
          "end_time": STRING // Isoformat
        }
      },
      ...
    ]
}
```
**Examples:**  
How to get the current menu at the Ratty...
`https://api.students.brown.edu/dining/menu?client_id=your-client-id&eatery=ratty`

How to get the menu at the Ratty on the 16th of this month at 5PM (that's 17:00!)...
`https://api.students.brown.edu/dining/menu?client_id=your-client-id&eatery=ratty&day=16&hour=17`

How to get all menus at the Ratty on the 16th of this month...
`https://api.students.brown.edu/dining/menu?client_id=your-client-id&eatery=ratty&day=16`

## Request Dining Hours
**Endpoint**: /dining/schedule

**Parameters**:

| Parameter |  Required | Value                    | Type                 |Default              |
|-----------|-----------|--------------------------|----------------------|---------------------|
| `eatery`  | no        | either 'ratty' or 'vdub' | string               |all dining halls     |
| `year`    | no        | the year desired         | integer              |current year         |
| `month`   | no        | the month desired        | integer between 0-12 |current month        |
| `day`     | no        | the day desired          | integer between 0-31 |current day          |

**Returns**: The number of menus found and a list of those menus in the form:

```javascript
{'num_results': INTEGER,
   [{'eatery': STRING,
     'year': INTEGER,
     'month': INTEGER,
     'day': INTEGER,
     'open_hour': INTEGER,
     'open_minute': INTEGER,
     'close_hour': INTEGER,
     'close_minute': INTEGER},
     ...
   ]
}
```

NOTE: Each eatery has different menu sections (e.g. "Bistro", "Main Menu", etc).
NOTE: If the eatery is closed, num_results will equal zero.

**Examples:**  
How to get today's hours for the Ratty...
`https://api.students.brown.edu/dining/hours?client_id=your-client-id&eatery=ratty`

How to get the hours for the VDub on the 18th of this month...
`https://api.students.brown.edu/dining/hours?client_id=your-client-id&eatery=vdub&day=18`

## Find Open Eateries  
**Endpoint**: /dining/open

**Parameters**:

| Parameter |  Required | Value                               | Type                 |Default              |
|-----------|-----------|-------------------------------------|----------------------|---------------------|
| `year`    | no        | the current year will be inferred   | integer              |Type                 |
| `month`   | no        | the current month will be inferred  | integer between 0-12 |Type                 |
| `day`     | no        | the current day will be inferred    | integer between 0-31 |Type                 |
| `hour`    | no        | the current hour will be inferred   | integer between 0-23 |Type                 |
| `minute`  | no        | the current minute will be inferred | integer between 0-59 |Type                 |

**Returns**:
```javascript
{'open_eateries': [hours_1, hours_2, ...]}
```
NOTE: is an hours object just like in the response from dining/hours.

**Examples:**  
Find out what eateries are currently open...
`https://api.students.brown.edu/dining/find?client_id=your-client-id`

Find out what eateries are open on the 12th of April...
`https://api.students.brown.edu/dining/find?client_id=your-client-id&day=12&month=4`
