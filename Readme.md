# Resty and Healthy Microservices

before using the api please update the config file with your own token to the npm site <br>
To get a token for accessing the npm API, you need to sign up for an npm account. <br>
Once you have an account, you can create a token by logging into your npm account and navigating to your profile settings. 
<br> 
From there, you can select the “Tokens” section and create a new token.

you can customize the config file with your own host and port for each service defaults are localhost and port 5050 and 5051
<br>

the expected input is a json object with the following structure:
<br>
```json
{ "data": ["package1", "package2", ...., "package10"] }
```
the json payload can be 10 packages or fewer
<br>

the output is a json object with the following structure:
```json
{
    "adea": "Package not found",
    "adeamdify": "package unhealthy due to -Last version is more than 30 days old and Number of maintainers is less than 2 and Latest commit is more than 14 days old",
    "buffer": "package unhealthy due to -Last version is more than 30 days old and Number of maintainers is less than 2 and Latest commit is more than 14 days old",
    "csv": "package unhealthy due to -Last version is more than 30 days old and Number of maintainers is less than 2 and Latest commit is more than 14 days old",
    "htmlparser2": "package unhealthy due to -Last version is more than 30 days old and Number of maintainers is less than 2 and Latest commit is more than 14 days old",
    "json5": "Package is healthy",
    "matchabot": "package unhealthy due to -Last version is more than 30 days old and Number of maintainers is less than 2 and Latest commit is more than 14 days old",
    "table": "package unhealthy due to -Last version is more than 30 days old and Latest commit is more than 14 days old"
}
```
the name of the package is the key and the value is the status of the package which could be healthy, package not found or unhealthy.<br>
if it is unhealthy the reason(s) is also provided.