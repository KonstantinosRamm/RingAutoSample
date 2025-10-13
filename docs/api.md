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

**GET api/machines/<machine_id>**
>Server Response
```json
{
    "active": true,
    "id": 1,
    "last date": "Sat, 11 Oct 2025 00:00:00 GMT",
    "last number": "",
    "machine_name": "G38",
    "nec": "3022_CO"
}
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
```json
>Client json
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





