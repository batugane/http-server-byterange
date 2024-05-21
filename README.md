
# HTTP Server for Cloud Optimized GeoTIFFs

This project provides a simple HTTP server to serve Cloud Optimized GeoTIFF (COG) files. The server supports HTTP byte range requests, allowing efficient access to large geospatial datasets.

## Features

- Serves Cloud Optimized GeoTIFF (COG) files
- Supports HTTP byte range requests
- Handles CORS for cross-origin resource sharing
- Simple to set up and run

## Requirements

- Python 3.x

## Setup and Usage

1. **Clone the Repository:**
    ```sh
    git clone https://github.com/batugane/http-server-byterange.git
    ```

2. **Install Dependencies:**
    Ensure you have Python 3.x installed. You can create a virtual environment and install any necessary packages if required:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Place Your COG Files:**
    Place your Cloud Optimized GeoTIFF files in the `your_cog_files` directory.

4. **Run the Server:**
    ```sh
    python simple_http_server.py
    ```

5. **Access the Files:**
    Open your web browser or use a tool like `curl` to access your COG files. For example:
    ```sh
    curl -H "Range: bytes=0-16000" http://127.0.0.1:8000/your_cog_files/your_cog_file.tif -o partial_output.tif
    ```

## Directory Structure

```
your_project/
├── .gitignore
├── simple_http_server.py
├── README.md
└── your_cog_files/
    └── your_cog_file.tif
```
