<h1 align="center" style="font-size: 50px;">Welcome to Cloudflare Firewall Rules library 👋</h1>

[![Website](https://quentium.fr/+img/github/website_cloudflare.svg)](https://quentiumyt.github.io/Cloudflare-Firewall-Rules/)&nbsp;
[![Donate](https://quentium.fr/+img/github/donate.svg)](https://www.paypal.me/QuentiumYT/1)&nbsp;
[![Contributions](https://quentium.fr/+img/github/contributions.svg)](https://github.com/QuentiumYT/Cloudflare-Firewall-Rules/pulls)&nbsp;
[![Tested on Python 3.10](https://quentium.fr/+img/github/python310.svg)](https://www.python.org/downloads)&nbsp;
[![License](https://quentium.fr/+img/github/apache2.svg)](https://github.com/QuentiumYT/Cloudflare-Firewall-Rules/blob/master/LICENSE)&nbsp;
[![Size](https://img.shields.io/github/repo-size/QuentiumYT/Cloudflare-Firewall-Rules?label=Repo%20Size&color=4391BD&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFAAAABQCAYAAACOEfKtAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAUCSURBVHhe7ZzdbhtFFMfPru3ECSFtYlqhVKK9IQ0Iil0JAilIhSTQPgHPwVWBB2hRVcFzcAG3CNIIJIgrxEeqctPSXvWioh/5aBJok6Zr5r/rTdeb2fjs7tjZmfXvZsdeS9H8dM6cc9aKqUePHjpjNa+5YPbiQtV27Evbjv3x/OeTS823U2E3r8bTlHdZLKeLduPy9PlfK96ddORC4NkL9ZqQNy+WFdvGlhvVou3MffRlfdT9QAqMF4jIcyxrTixHX3zhAM1OvU7PDw3gVo227Pm0kWj0GRhI2wrkTZ54mRCBj7ee0C9/Xqf1jUfilnV127Fmkp6JxgqMkuejSqKRKTx9sX5GyFsQS6k8UO4r0bsnJ5rpjDMxWWExTiAir+RY34rlYLFYoOorx3bJ81Eh0SiBfto2iAYgb3v7KdUXb9KmSNco0ko0RmD4zJt55zUaHhqktY3/6MrVm96HIkgj0QiBsoIx0N8vpByng8PPiRRuXyuTStS+CrertnGJW521jsCgvFKbgsElbiRqKzAs7wmjYHCJI1FLgbsKxtvPCsbPf1ynx5vdk6idQNmZVy57BQMS1/995J5h3ZKolcAPv7hy1nLsulhWxg6N0OQb4ztnXr+72WcSFxZvKEvnU9VxKrh/BxKdr707HtoIdCOP6BvRNrhN8omJl8i2WpuIoERO/8fBaTTo2o3b9NRxxCtr1bHsT707HoXmNdME0nbYnzDuLa/TkcMjVCy0bgGv8f79lXU3ao6OHWreiQ/k/XbtFt25vyJeQZ41O3du8nfvrkfm+8DwmYdWBdUWETYyPESn33rV+6BiOPJAplNYVjDiThhJ4MoDmY1Amby0TTKHOPJAJiMwKE/VhMEhrjyQuSISlocJI6pgqCSJPJApgeG0Rf8FeSgY/zx4SGOHRwlVWDVJ5YHMCJSdeaVSyY28u0trbnN8d0m9xDTyQCYE4juMgmN/L5YHwgXD7+t8ifeW15Slc1p5YN8FIvKKjv2DWLrfYUzVxqlPRF6QoESk84OVDTp2JHmDDFTIA/sqMJC2mZswuOxbHxg+87I2YXDZlz5QVjCyNmFw6XoEyuRltUnm0NUIDMrL+oTBpWtFJCwv6xMGl64IDKetDhMGl44LlJ15OkwYXDoqUOcJg0vHBCLydJ4wuHREYCBttZ0wuCjvA8Nnnq4TBhelTZisYOg6YXBRtiOZPN2bZA5KdhiUZ8qEwSV1EQnLM2XC4JJqh+G0NWnC4JJ4d7Izz6QJg0uineVhwuASe1eIvDxMGFxiCQykrfETBhd2Hxg+80yfMLiwmjVZwTB9wuDSducyeXlpkjnsaSIoL28TBpfIIhKWl7cJg4vURDht8zhhcNllQXbm5XHC4NJiYK+CEWyOVUvUVR7Y2f1e8nzCEpdWzZ0wuOwYEvIuiUsFU0N1Irra+v/MoqL/a5VHy3bD+UAneWDHwOmvfjzYv1nGjPvm0GCZ3js5QeVyn3ezA+geeT4tIdQtiabIA7tysNMSTZIHpIdYpySaJg9EVgHVEk2UByIFAlUSTZUH9hQI0ko0WR5oKxAklWi6PMASCOJKzIM8wBYIuBLzIg/EEgjaScyTPBBbIIiSmDd5IJFAEJZ4qnac/vr7dq7kgcQCgfsruFsWHoHV8PTGcX8aBE9VGjPffTa1iBemk0ogCEZiniLPJ/VXbD998v4q9TXOiOW8js/zevTQGaL/Af3ei59A3O7oAAAAAElFTkSuQmCC)](../../)&nbsp;

# ✨ Cloudflare Firewall Rules

> #### A Cloudflare wrapper to bulk add / edit your firewall rules using Cloudflare's API.

Cloudflare Firewall Rules is a wrapper module that aims to easily create, modify, delete rules. It also provides a way to import & export new rules in your domain's firewall.

If you have some rules that you want to duplicate among your domains, this module is made for you!

### A complete documentation can be found at: https://quentiumyt.github.io/Cloudflare-Firewall-Rules/

## 📥 Installation

```bash
pip install cf_rules

# OR

git clone https://github.com/QuentiumYT/Cloudflare-Firewall-Rules.git
cd Cloudflare-Firewall-Rules/
pip install .
```

## 🚀 Usage

You have 2 auth methods available:

A Global API Key or a specific API Token generated from here: https://dash.cloudflare.com/profile/api-tokens

### Cloudflare Global API Key

![Cloudflare Key](/images/cloudflare_key.png)

Using a Global API Key, you will have access to everything allowed by a Cloudflare account. It can access all domains from every account you have, this might be overpowered...

### Cloudflare API Token

An API token is recommended to keep control of specific domains only. You will need to give the correct permissions for Cloudflare's firewall rules to work.

The required permissions are "Zone.Zone, Zone.Firewall Services"

![Cloudflare Token](/images/cloudflare_tokens.png)

Here is a token creation example:

![Cloudflare Token](/images/cloudflare_token.png)

## 💨 Quickstart

You can use any example scripts in the examples folder, just create a .env file

I might add more examples in the future, but everything is in the docs :)

---

Create any Python file in the cloned directory and paste these lines

```python
from cf_rules import Cloudflare

cf = Cloudflare()
cf.auth("cloudflare@example.com", "your-global-api-key")
# OR
cf.auth_bearer("your-specific-bearer-token")

domains = cf.domains["domains"]

print(domains)
# >>> ['example.com']

cf.export_rules("example.com")
# Creates a text file for every rule you have on your domain

cf.create_rule("example.com", "My Bad Bots FW rule", "Bad Bots", "challenge")
# Create a new rule with the content of the "Bad bots.txt" file with the challenge action

cf.update_rule("example.com", "My Bad Bots FW rule", "Bad Bots lib")
# Change the rule's expression to the content of the "Bad bots lib.txt" file
```

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change and join your fork with the modifications.\
Please make sure to test your suggestions before committing.

If you don't feel comfortable coding, you can submit your idea about what you would like to see implemented.

Any PR with small code examples or better documentation changes is appreciated :)

## 👤 Author

**Quentin L.**

-   Website: [quentium.fr](https://quentium.fr/)
-   Twitter: [@QuentiumYT](https://twitter.com/QuentiumYT)
-   Contact: [Mail](mailto:pro@quentium.fr?subject=[Cloudflare]%20Contact%20for%20...)

Please ✰ this repository if this project helped you!

## 📖 License

[Apache 2.0](https://choosealicense.com/licenses/apache-2.0/)

---

_Made with_ ❤ _by QuentiumYT_
