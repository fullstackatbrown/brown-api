# Dining
The dining eatery essentially reformats forwards the request to the [http://legacy.cafebonappetit.com/api/2](http://legacy.cafebonappetit.com/api/2) endpoint and then appends info stored on the Brown API servers to the return values. If you have no need for these additional fields and would like to optimize your system for request speed, we recommend you access the bonappetit API directly.

Each dining hall has a unique ID that we take directly from the BA systems, thus, the mapping is

| Café      |  ID |
|-----------|-----------|
| Sharpe Refectory  | 1531       |
| Verney-Woolley  | 1532       |
| Andrews Commons  | 1533       |
| Blue Room  | 1534       |
| Josiah’s  | 1535       |
| Ivy Room  | 1536       |
| Campus Market  | 1537       |
| Café Carts  | 1538       |


## Request Dining Schedule
**Endpoint**: /dining/cafe/&lt;cafe_id&gt;

**Parameters**:
If data for many cafés are desired, separate many cafe_ids with ","

**Returns**: information for the cafe with the given cafe_id

Schedule information will be given under 'days' in the format:
```javascript
{
  'date': STRING,
  'dayparts': [
    {
      'starttime': STRING,
      'endtime': STRING,
      'hide': STRING,
      'id': STRING,
      'label': STRING,
      'message': STRING
    }
  ]
}
```

**Examples:**  

Get ratty data - `/dining/cafes/1531?client_id=<client_id>`

Get ratty and vdub data - `/dining/cafes/1531,1532?client_id=<client_id>`

## Request Dining Menu
**Endpoint**: /dining/cafe/&lt;cafe_id&gt;/menu/&lt;date&gt;

**Parameters**:
Dates are formated in YYYY-MM-DD form. Additionally, **date is an optional parameter** and you may query /dining/cafe/&lt;cafe_id&gt;/menu to find the menu for the current day


**Returns**: Menus for the selected dining halls on the selected days.

**Examples:**  

Get ratty menu today -
`/dining/cafes/1531/menu?client_id=<client_id>`

Get ratty and vdub menus on specific dates -
`/dining/cafes/1531,1532/menu/2018-2-4,2018-2-5?client_id=<client_id>`
