# Facebook Snooper

Scrapes Facebook profile pages and searches profiles using a normal log in (without an API key). Inspired by [facebook-scraper](https://github.com/kevinzg/facebook-scraper).
Built with [MechanicalSoup](https://github.com/MechanicalSoup/MechanicalSoup) and [lxml](https://github.com/lxml/lxml).

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
>>> fb = facebook_snooper.default_session()
>>> fb
<facebook_snooper.core.session.FacebookSession object at 0x106f64590>
>>> fb.log_in('user@email.com', 'user_password')
<facebook_snooper.core.session.FacebookSession object at 0x106f64590>
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
'https://scontent-fco1-1.xx.fbcdn.net/v/t1.0-1/cp0/e15/q65/p74x74/49342020_10157005134417363_1173260116078624768_o.jpg?_nc_cat=101&efg=eyJpIjoiYiJ9&_nc_ohc=ePuavjZLTc8AQls2sbe1iRxIb0rjQZhCDHdeGew-nC-OLozFtw768yIAg&_nc_ht=scontent-fco1-1.xx&oh=14a30cde6126c807eba801a07cfbf316&oe=5E7B9A5F'
>>> info
['The New York Times', 'Columbia University', 'UNC Chapel Hill', 'Loomis Chaffee',
 'Loomis Chaffee, Windsor, Conn.', 'New York', 'White Plains']
```

## Test
Create test directory and data:
```sh
$ cd facebook-snooper
$ mkdir tests/pages
```
```python
>>> import facebook_snooper 
>>> from tests import persist
>>> fb = facebook_snooper.default_session()
>>> fb.log_in('user@email.com', 'user_password')
True
>>> utils.save_page('login', fb.current_html
>>> fb.search('frank new york')
...
>>> utils.save_page('search', fb.current_html)
>>> fb.profile_info('frankbruninyt')
...
>>> utils.save_page('profile', fb.current_html)

```
Execute tests:
```sh
$ python3 tests/core.py
```

### Disclaimer
- This package cannot gather nothing more that is publicly visible.
- Please respect people's privacy and use it ethically.

### Notes
- This is a pre-release, since it's under development API can change until stable version.
- There is no guarantee that will work if scraped pages change too much.