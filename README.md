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
>>> from facebook_snooper.dump import dump_search, dump_info
>>> fb = facebook_snooper.init_session()
>>> fb.log_in('user@account.com', 'user_password')
<facebook_snooper.core.session.Session object at 0x10ffc58d0>
>>> results = fb.search('frank new york')
>>> dump_search(results, pretty=True)
profile frankdecaro https://m.facebook.com/frankdecaro?refid=46
  Frank DeCaro
  Author at Rizzoli New York
  Freelance Writer at The New York Times
profile frankbruninyt https://m.facebook.com/frankbruninyt?refid=46
  Frank Bruni
  The New York Times
  New York, New York
>>> info = fb.profile_info('frankbruninyt')
>>> dump_info(info, pretty=True)
Frank Bruni
Image: https://scontent-fco1-1.xx.fbcdn.net/v/t1.0-1/cp0/e15/q65/p120x120/49...
  work The New York Times
  education Columbia University,
  education UNC Chapel Hill
  education Loomis Chaffee
  education Loomis Chaffee, Windsor, Conn.
  living New York
  living White Plains
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