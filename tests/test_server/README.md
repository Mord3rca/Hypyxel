# Test Server

This test server is used to send predictable DATA while testing the library.

## Register new endpoint

To register new DATA, put them in the *response* directory with the following scheme:

`<path>.<method>`

Where:
  * path is the endpoint method with / replaced by .
  * method is the method used in lowercase (get, post, head, put, ...)

Note: Only GET is supported for now.
