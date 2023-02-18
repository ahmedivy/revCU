import requests

cookie = "1vlaqiupbae3h5h0jhvhky30"


response = requests.get(
    "https://cuonline.cuilahore.edu.pk:8091/ResultCard", 
    cookies={
        "ASP.Net_SessionId": cookie,
        "__RequestVerificationToken" : "1GeFgAeL24uuidfTPlK6y_E3LqWBn0Qr8_lKSke6V7ErrYdOZk2wPPphSKeYRH4bpZXq-3sB2P_xRQkpG0ouc7e6NFecGy0j4QTiccmZFPJz0AsVaMp1xHOFsGV0WCXqPZ4T_JruJCZLQAt-o-weNQ2"
    }
)

print(response.text)