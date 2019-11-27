![fb-snooper logo](https://user-images.githubusercontent.com/1194228/69556500-1ab03f00-0fa5-11ea-867a-c4c897ea17ff.png)

# Facebook Snooper

Scrapes Facebook profile pages and searches profiles using a normal log in (without an API key). Inspired by [facebook-scraper](https://github.com/kevinzg/facebook-scraper). Built with [MechanicalSoup](https://github.com/MechanicalSoup/MechanicalSoup).

## Install
**NOTE**: Python 3.7 or higher is required.
```sh
# clone the repository
$ git clone https://github.com/gsscoder/facebook-snooper.git

# change the working directory
$ cd facebook-snooper

# install the package
$ python3 -m pip install .
```

## Usage
```python
>>> import facebook_snooper
>>> fb = facebook_snooper.init_session()
>>> fb
<facebook_snooper.core.session.Session object at 0x1075898d0>
>>> fb.log_in('user@email.com', 'user_password')
<facebook_snooper.core.session.Session object at 0x1075898d0>
>>> fb.search('frank new york')
('frankdecaro',
  ['Frank DeCaro', 'Author at Rizzoli New York',
   'Freelance Writer at The New York Times'],
  'https://m.facebook.com/frankdecaro?refid=46')
('frankbruninyt',
  ['Frank Bruni', 'The New York Times', 'New York, New York'],
  'https://m.facebook.com/frankbruninyt?refid=46')
>>> name, image_link, info = fb.profile_info('frankbruninyt')
>>> name
'Frank Bruni'
>>> image_link
'https://scontent-fco1-1.xx.fbcdn.net/...0cde6126c807eba801a07cfbf316&oe=5E7B9A5F'
>>> info
[('work', 'The New York Times'), ('education', 'Columbia University'),
 ('education', 'UNC Chapel Hill'), ('education', 'Loomis Chaffee'), ('education',
 'Loomis Chaffee, Windsor, Conn.'), ('living', 'New York'), ('living', 'White Plains')]
```

## Test
Create test directory and data:
```sh
$ cd facebook-snooper
$ mkdir tests/pages
```
```python
>>> import facebook_snooper 
>>> from tests.persistence import save_login, save_current_page
>>> fb = facebook_snooper.init_session()
>>> save_login(fb)
>>> fb.log_in('user@email.com', 'user_password')
...
>>> save_current_page(fb, 'logged')
>>> fb.search('frank new york')
...
>>> save_current_page(fb, 'search')
>>> fb.profile_info('frankbruninyt')
...
>>> save_current_page(fb, 'profile')

```
Execute tests:
```sh
$ python3 tests/session.py
```

### Disclaimer
- This package cannot gather nothing more that is publicly visible.
- Please respect people's privacy and use it ethically.

### Notes
- This is a pre-release, since it's under development API can change until stable version.
- There is no guarantee that will work if scraped pages change too much.