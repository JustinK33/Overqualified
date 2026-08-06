### before starting ...
1. create ur venv
2. pip install -r -requirements.txt
3. review any of our changes

### concepts
The gateway usually handles things like:

  - Public HTTP routes
  - Authentication
  - Request validation
  - Calling internal services
  - Normalizing errors
  - Logging and tracing
  - Rate limiting
  - Hiding internal service addresses from the frontend

  Your gateway should not contain all business logic.
  It should coordinate calls and enforce cross-cutting rules.

  The Mental Model

  When an endpoint in the gateway calls another service, the flow is:

  Client sends request
          |
          v
  Gateway route receives it
          |
          v
  Gateway builds a request to the internal service
          |
          v
  Internal service responds
          |
          v
  Gateway maps that response back to the client

### problems i came across
1. when creating a venv to install my dependencies, it didnt automatically select the right one. do cmd+shift+p to find the right one

# Basic start
1. fastapi app running
2. one dumb endpoint (it should call another service and return whatever that service says. even a fake one b/c it should say "i can talk to another service" not just "i can respond")
3. once we have 2/3 internal services add routing request like /search to the search-service and /postings to the ingestion-service. (start thinking about how the gateway knows addresses of other services not just hardcoded urls or env vars)
4. once the auth service exists, add token verification (the gateway should check if the user is logged in once instead of checking every other service individually)