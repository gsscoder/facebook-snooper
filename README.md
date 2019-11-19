# Facebook Snooper

Scrapes Facebook profile pages and searches profiles using a normal log in (without an API key). Inspired by [facebook-scraper](https://github.com/kevinzg/facebook-scraper).
Built with [MechanicalSoup](https://github.com/MechanicalSoup/MechanicalSoup) and [lxml](https://github.com/lxml/lxml).

## Install
**NOTE**: Python 3.7.5 or higher is required.
```sh
# clone the repository
$ git clone https://github.com/gsscoder/facebook-snooper.git

# change the working directory
$ cd facebook-snooper

# install the requirements
$ python3 -m pip install -r requirements.txt

# copy to your project directory
$ cp -r facebook_snooper $HOME/your/project/dir
```

## Usage
```python
>>> from facebook_snooper import Session
>>> fb = Session.Default()
>>> fb
<facebook_snooper.core._FacebookSession object at 0x10ff45f50>
>>> fb.log_in('user@email.com', 'user_password')
True
>>> fb.search_profiles('johnny new york')
[('johnny.profile.id', 'https://www.facebook.com/johnny.profile.id'), ('mark.profile.id', 'https://www.facebook.com/mark.profile.id')]
>>> fb.get_intro('johnny.profile.id')
['Works at ...', 'Former consultant at ...', 'Studies at Columbia University', 'Went to UNC Chapel Hill', 'Lives in White Plains, New York', 'Joined August 2015', 'Followed by 1,068 people']
```

## Test
Create test directory and data:
```sh
$ cd facebook_snooper
$ mkdir tests/pages
```
```python
>>> from facebook_snooper import Session
>>> from tests import utils
>>> fb = Session.Default()
>>> fb.log_in('user@email.com', 'user_password')
True
>>> utils.save_page('login', fb.current_html
>>> fb.search_profiles('johnny new york')
...
>>> utils.save_page('search', fb.current_html)
>>> fb.get_intro('johnny.profile.id')
...
>>> utils.save_page('profile', fb.current_html)

```
Execute tests:
```sh
$ python3 tests/core.py
```

### Disclaimer
- Please respect people's privacy and use it ethically.

### Notes
- There is no guarantee that will work if scraped pages change too much.