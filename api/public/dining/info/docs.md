# Dining
The eatery names are 'ratty' or 'vdub'. Currently, only the Ratty and VDub are supported.

## Request Dining Menu
**Endpoint**: /dining/menu

**Parameters**:

| Parameter |  Required | Value                               | Type                 |
|-----------|-----------|-------------------------------------|----------------------|
| `eatery`  | yes       | either 'ratty' or 'vdub'            | string               |
| `year`    | no        | the current year will be inferred   | integer              |
| `month`   | no        | the current month will be inferred  | integer between 0-12 |
| `day`     | no        | the current day will be inferred    | integer between 0-31 |
| `hour`    | no        | the current hour will be inferred   | integer between 0-23 |
| `minute`  | no        | the current minute will be inferred | integer between 0-59 |

**Returns**: The number of menus found and a list of those menus in the form:

~~~~.json
{'num_results': INTEGER,
 'menus':
    {'eatery': STRING,
     'year': INTEGER,
     'month': INTEGER,
     'day': INTEGER,
     'start_hour': INTEGER,
     'start_minute': INTEGER,
     'end_hour': INTEGER,
     'end_minute': INTEGER,
     <menu_section1>: [STRING, STRING, ...],
     <menu_section2>: [STRING, STRING, ...],
     ...
   }
 }
 ~~~~
