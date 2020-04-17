Laundry
=====================

Laundry rooms are identified in the laundry model by a unique ID. To view all ID mappings,
please request [/laundry/rooms](/laundry/rooms) with your client_id. All laundry data is scraped from [https://www.laundryview.com/brownu](https://www.laundryview.com/brownu) and stored in our database. When get_status is passed in as an argument, we scrape the latest information on demand directly from the laudryview json and deliver it to your system. 

## Request Rooms
**Endpoint**: /laundry/rooms

**Returns**: The mapping of all known wash rooms and their IDs:

```javascript
{
	'num_results': INTEGER,
	'results': [
		{
			'id': INTEGER,
			'name': STRING
		},
		...
	]
 }
```

**Example:**  

`/dining/schedule?client_id=<client_id>`

## Request Specific Room
**Endpoint**: /laundry/rooms/&lt;room_id&gt;

**Parameters**:

| Parameter |  Required | Value                               | Type                 |
|-----------|-----------|-------------------------------------|----------------------|
| `get_status`  | no       | true if retrieving machine statuses, default false | bool               |


**Returns**: Machines in the room with the specified ID

```javascript
{
	'result': {
		'id': INTEGER,
		'machines': [
			{
				'id': INTEGER,
				'room_id': INTEGER,
				'avail': BOOLEAN, // if get_status is true
				'average_run_time': INTEGER, // if get_status is true
				'time_remaining': INTEGER, // if get_status is true
				'type': STRING
			},
			...
		]
	}
 }
```

**Example:**  

Get with statuses - `/laundry/rooms/<room_id>?get_status=true&client_id=<client_id>`

Get without statuses - `/laundry/rooms/<room_id>?get_status=true&client_id=<client_id>`


## Request Specific Machine
**Endpoint**: /laundry/rooms/&lt;room_id&gt;/machines/&lt;machine_id&gt;

**Parameters**:

| Parameter |  Required | Value                               | Type                 |
|-----------|-----------|-------------------------------------|----------------------|
| `get_status`  | no       | true if retrieving machine statuses, default false | bool               |


**Returns**: The machine with the given ID in the room with the given ID

```javascript
{
	'result': {
		'id': INTEGER,
		'room_id': INTEGER,
		'type': STRING
	}
}
```

**Example:**  

Get with statuses - `/laundry/rooms/<room_id>/machines/<machine_id>?get_status=true&client_id=<client_id>`

Get without statuses - `/laundry/rooms/<room_id>/machines/<machine_id>?get_status=true&client_id=<client_id>`
