# Dataset Service

This service provides functionality for working with a dataset in CSV format.

## Usage

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/dataset-service.git
    ```

2. Navigate to the project directory:

    ```bash
    cd dataset-service
    ```

3. Build the Docker image:

    ```bash
    docker build -t dataset-service .
    ```

4. Run the Docker container:

    ```bash
    docker run -p 5000:5000 dataset-service
    ```

5. Access the API documentation:

    Open your web browser and go to [http://localhost:5000/swagger](http://localhost:5000/swagger)

6. Interact with the API endpoints to filter data and export to CSV.

## API Endpoints

- `/filter`: Filter data based on specified parameters.
- `/export`: Export filtered data to CSV.

## Example Requests

- Filter data:

    ```http
    GET /filter?category=example&gender=male&dob=1990-01-01&age_range=25-30
    ```

- Export filtered data to CSV:

    ```http
    GET /export?category=example&gender=male&dob=1990-01-01&age_range=25-30
    ```

## Notes

- The dataset is expected to be in CSV format and located at `app/dataset.csv`.
- The SQLite database file will be created at `app/dataset.db`.

