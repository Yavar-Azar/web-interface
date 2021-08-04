# JSON format

- JSON stands for JavaScript Object Notation
- JSON is a lightweight data-interchange format
- JSON is plain text written in JavaScript object notation
- JSON is used to send data between computers
- JSON is language independent 



### **Functions Used:**  

- json.loads():  This function is used to parse the JSON string.
- json.dumps(): This function is used to convert Python object into JSON string.



Converting a json to dict object and using dict.update() function one can update an object and make a new json

**example**

```python
import json
  
# JSON data:
x =  '{ "organization":"GeeksForGeeks",
        "city":"Noida",
        "country":"India"}'
 
# python object to be appended
y = {"pin":110096}
 
# parsing JSON string:
z = json.loads(x)
  
# appending the data
z.update(y)
 
# the result is a JSON string:
print(json.dumps(z))
```

