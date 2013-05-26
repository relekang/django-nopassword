## Changelog
### 0.3.3
* Fix redirect bug in logout view.
* Add "http://" to link sent in token mail.
* Add NOPASSWORD prefix to all django-nopassword settings

### 0.3.2
* Remove migrations

### 0.3.1
* Remove long description with bad markup

### 0.3
* Support inactive users
* Set `supports_inactive_user` to avoid warnings on 1.4

### 0.2
* Support for custom user in Django 1.5
* Add `LOGIN_CODE_TIMEOUT` setting
* Add south support
* Fix bug in timout check

### 0.1.2
* Fix typo in LoginCode.max_length

### 0.1.1
* Add tests
* Add travis-ci settings

### 0.1.0
* First version, basic functionality added
