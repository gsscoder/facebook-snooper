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
<facebook_snooper.core.session.FacebookSession object at 0x10cf22290>
>>> fb.log_in('user@email.com', 'user_password')
True
>>> fb.search('frank new york')
[('frank.cisneros.56', 'hubs', 'https://www.facebook.com/frank.cisneros.56'),
 ('frankbruninyt', 'Frank Cisneros', 'https://www.facebook.com/frankbruninyt')]
>>> name, image_link, followers, intro = fb.profile_info('frankbruninyt')
>>> name
'Frank Bruni'
>>> image_link
'https://scontent-fco1-1.xx.fbcdn.net/v/t1.0-1/p160x160/49342020_10157005134417363_1173260116078624768_o.jpg?_nc_cat=101&_nc_oc=AQliVuLJdFWX1at-6TPqNRWj3_T6I-cJvESxIfPvcFD1NNjRMGaDr0m8XUKZOwY3_kA&_nc_ht=scontent-fco1-1.xx&oh=c658885ef831fdcd1a7f7b6f3faa958d&oe=5E559A48'
>>> followers
'234994'
>>> intro
['Works at The New York Times', 'Studied at Columbia University', 'Studied at UNC Chapel Hill', 'Went to Loomis Chaffee', 'Went to Loomis Chaffee, Windsor, Conn.', 'Lives in New York, New York', 'From White Plains, New York', 'Followed by 234,994 people']
```

## Test
Create test directory and data:
```sh
$ cd facebook-snooper
$ mkdir tests/pages
```
```python
>>> import facebook_snooper 
>>> from tests import utils
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
- Please respect people's privacy and use it ethically.

### Notes
- This is a pre-release, since it's under development API can change until stable version.
- There is no guarantee that will work if scraped pages change too much.