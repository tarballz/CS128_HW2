# CS128_HW2
Distributed single-site key-value store with forwarding

This assignment consists of two parts. In the first part, you will build a REST-accessible single-site key-value store. In the second part, you will create a service that consist of several instances. One instance is a single site key-value store. All other instance process requests by forwarding them to the main instance.

 

You will use Docker to create an image which must expose a web server at port 8080 that implements the REST interface below.

#### Functional guarantees for a single site key-value store:

* service runs on port 8080 and is available as a resource named kv-store. i.e. service listens at http://server-hostname:8080/kv-store

* service listens to requests on a network

* get on a key that does not exist returns an error message

* get on a key that exists returns the last value successfully written (via put) to that key

* del on a key that does not exist returns an error message

* put on a key that does not exist (say key=foo, val=bar) creates a resource at kv-store/foo. Subsequent gets return 'bar' until the next put at kv-store/foo

* del on a key that exists (say foo) deletes the resource kv-store/foo and returns success. Subsequent gets return a 404 until the next put at kv-store/foo

* put on a key that exists (say key=foo) replaces the existing val with the new val (say baz), and acknowledges a replacement in the response by setting the 'replaced' field to ‘True’ (see examples below) . Subsequent gets return 'baz' until the next put at kvs/foo.

 

#### Part 2: Network of instances with request forwarding

Once you have a single site key-value store working, you will create a network of instances. One instance is the key-value store, which we call the main one. All other instances process request by forwarding them to the main instance.

We are going to create several instances of your container. However, you are just submitting one container, so your service will need to know how to play either role. The role of a container is specified via environment variables.
