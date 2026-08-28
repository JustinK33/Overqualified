# General flow
user enters user/pass to frontend
fronted forwards that to backend where auth service lives
the backend hashes the password and checks: is this hash the same as the hashed password saved from registering?
possibility 1: if it is then we return cookies to the user directly from the backend (not through front end. there is a secruity gap)
possibility 2: if it isnt just return an error message

## things to look into
JWT instead of cookies
bycrpt (hashing) vs encrpyting (reversible with secret key)

## things to think about
ask yourself: what would go wrong if for our users if the database ever got leaked? once with encrpytion and other with hashing.
(this should show the gap between what different parts of our systems are supporting)

initial sketch
![Auth Flow 1](services/auth-service/docs/auth-design1.png)

## things i learned
- for password hashing we used bcrpyt and salting which just results in different hashes for the same passwords.
- use with block to not have to close() each time
- we can use pydantic validation models not just for incoming data but also outgoing
bcrpyt docs - https://github.com/pyca/bcrypt
- for auto incrementing sql columns "GENERATED ALWAYS AS IDENTITY"
- use pydantic model as type for input values
- (5) is an int but (5,) is a tuple

## unrelated learning
normally we do this for version before 18
volumes:
      - postgres_data:/var/lib/postgresql/data
but starting version 18+ its stores data in /var/lib/postgresql/$PG_MAJOR/docker
so it should be 
volumes:
      - postgres_data:/var/lib/postgresql