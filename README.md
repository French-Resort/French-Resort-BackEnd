# French Resort BackEnd

The Backend component of the French Resort, facilitating administrators to manage bookings and rooms using CRUD operations.

## How to Use:

### Requirements
- Python 3.11
- Conda or Python virtual environment

### Install Libraries
Execute the following commands to set up the required environment:
```bash
conda create -n frenchResortBackEnd python=3.11
conda activate frenchResortBackEnd
pip install -r requirements.txt
```

### Run the Server
Navigate to the `src` directory and execute the following command:
```bash
python app.py
```

Open your web browser and go to [http://localhost:5001](http://localhost:5001) to interact with the French Resort BackEnd.

**Note:** Ensure that the Backend server is running to enable complete functionality. Adjust the server configuration in the backend if necessary.

Feel free to explore the interface, log in as an administrator, and manage bookings and rooms through the user-friendly BackEnd of the French Resort.

To initialize the database, you can use the following command:
```bash
python -c "from bdd_requests import bdd_init; bdd_init()"
```

This will set up the necessary database structure for the French Resort BackEnd.
