# Sweager 
https://api.eloverblik.dk/CustomerApi/swagger/index.html

# Step 1: 
Use token in Eloverblik in Bearer Tokan
call API:  https://api.eloverblik.dk/CustomerApi/api/Token
Get a temporarily token: 

# Step 2: (optional)
use API: /api/MeteringPoints/MeteringPoints  to get the meteringPoint. 
But only need this api once, then we can use the metering point as a static data. 
Helsebakken: 571313174114453369
Vangedevej: 571313174113992944


# Step 3: 
Now ready to use the temporarily token to call other apis.

Get last 7 days
https://api.eloverblik.dk/CustomerApi/api/MeterData/GetTimeSeries/2020-03-01/2020-03-05/Day

Get last 7 month
https://api.eloverblik.dk/CustomerApi/api/MeterData/GetTimeSeries/2020-03-01/2020-03-05/Month

Get last 7 hours
https://api.eloverblik.dk/CustomerApi/api/MeterData/GetTimeSeries/2020-03-01/2020-03-05/Hours

Get reading
/api/MeterData/GetMeterReadings/{dateFrom}/{dateTo}
have start reading
and end reading