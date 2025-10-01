# Final Report

## Design Choices

The REST API was built using Python's built-in `http.server` module. This choice was made for its simplicity and to avoid external dependencies, making the project lightweight and easy to run.

The data is parsed from an XML file and stored in memory in two data structures: a list and a dictionary. The list of transactions allows for easy iteration, while the dictionary provides fast lookups by transaction ID (O(1) average time complexity).

## Security Considerations

### Basic Authentication

Basic Authentication was implemented to protect all API endpoints. While easy to implement, it is not recommended for production environments because it sends credentials in plain text (Base64 encoded, which is easily reversible).

### Weaknesses of Basic Authentication

- **Plain Text Credentials:** Credentials are not encrypted, making them vulnerable to interception.
- **No Session Management:** Each request requires authentication, which can be inefficient.
- **Vulnerable to Brute-Force Attacks:** Without proper rate limiting, the server is susceptible to brute-force attacks.

### Recommended Alternatives

For a production environment, more secure authentication mechanisms should be used, such as:

- **JWT (JSON Web Tokens):** Tokens are signed and can contain user roles and permissions. They are stateless and scalable.
- **OAuth2:** An authorization framework that allows third-party applications to obtain limited access to an HTTP service.

## Data Structures and Algorithms (DSA) Reflections

The project demonstrates the performance difference between two search algorithms:

- **Linear Search:** Implemented in the `linear_search` function, it iterates through the list of transactions to find a match. The time complexity is O(n), where n is the number of transactions.
- **Dictionary Lookup:** Implemented in the `dictionary_lookup` function, it uses a hash map (dictionary) to find a transaction by its ID. The time complexity is O(1) on average.

The `/search-comparison` endpoint clearly shows that dictionary lookup is significantly faster than linear search, especially as the number of transactions grows. This highlights the importance of choosing the right data structure for the task at hand.
