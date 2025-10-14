>⚠️ Note
>
>The REST API is designed to **validate all incoming JSON data**. 
>If a request contains invalid fields, missing required values, or wrong types, 
>the server will respond with an **error in JSON format**, explaining what went wrong. 
>This ensures that clients always receive structured feedback for corrections.
>
>Currently, the **PATCH `/machines` endpoint** is the only endpoint that accepts **multiple machines at once** (an array of objects). 
>All other endpoints (`POST`, `DELETE`, etc.) currently accept **only a single object** per request. 
>This may change in future updates to support bulk operations.


**GET api/machines**
>Server Response
```json
[
    {
        "active": true,
        "id": 1,
        "last date": "Sat, 11 Oct 2025 00:00:00 GMT",
        "last number": "",
        "machine_name": "G38",
        "nec": "3022_CO"
    },
    {
        "active": true,
        "id": 2,
        "last date": "Thu, 09 Oct 2025 00:00:00 GMT",
        "last number": "",
        "machine_name": "G38",
        "nec": ""
    }
    
]
```
**DELETE api/machines/<machine_id>**
>Server Response
```json
{
    "status": "Machine <machine_id> deleted"
}
```
**POST api/machines**
>Client json
```json
{   
    "id" : 100,
    "machine_name" : "G30"
}
```
>Server Response
```json
{
    "success": "machine G30-100 added"
}
```

**PATCH api/machines**
>Client json
```json
[
    {"machine_id": 21,
     "is_active": false
    },
    {
     "machine_id": 11,
     "is_active": false
    }
]
```

>Server response
```json
[
    {
        "success": "field 'is_active' updated in machine 21"
    },
    {
        "error": "machine_id 11 not found"
    }
]
```





