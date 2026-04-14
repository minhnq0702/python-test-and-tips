# QR Code Scanner Docker

A Dockerized QR code scanner using Python, OpenCV, and zbar with multi-architecture support (ARM/x86).

## Features

- Multi-architecture support (ARM64 and x86_64)
- Reads QR codes from images using zbar
- Containerized for consistent execution across platforms

## Prerequisites

- Docker
- Docker Compose (optional, for easier management)

## Project Structure

```
code-scanner/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── main.py
├── image.jpg
└── README.md
```

## Building the Docker Image

### Option 1: Using Docker directly

```bash
# Build for your current architecture
docker build -t qr-scanner .

# Build for specific architecture (multi-arch)
docker buildx build --platform linux/amd64,linux/arm64 -t qr-scanner .
```

### Option 2: Using Docker Compose

```bash
docker-compose build
```

## Running the Container

### Option 1: Using Docker directly

```bash
# Run with the default image.jpg
docker run --rm qr-scanner

# Run with a custom image (mount your image)
docker run --rm -v $(pwd)/your-image.jpg:/app/image.jpg qr-scanner
```

### Option 2: Using Docker Compose

```bash
docker-compose up
```

## Scanning Different Images

To scan a different image, you have several options:

### Method 1: Replace image.jpg
Simply replace `image.jpg` with your own image and rebuild:
```bash
docker-compose up --build
```

### Method 2: Mount a different image
```bash
docker run --rm -v $(pwd)/my-qr-code.jpg:/app/image.jpg qr-scanner
```

### Method 3: Modify main.py
Update the image path in `main.py` and rebuild the container.

## Architecture Support

This Docker image works on:
- **x86_64** (Intel/AMD processors)
- **ARM64** (Apple Silicon M1/M2/M3, Raspberry Pi 4+, AWS Graviton)

The base image `python:3.11-slim` automatically selects the correct architecture, and zbar is installed from Debian repositories which provide native builds for both architectures.

## Dependencies

- **Python 3.11**
- **opencv-python-headless**: For image processing
- **pyzbar**: Python wrapper for zbar
- **libzbar0**: Native zbar library for QR code detection

## Troubleshooting

### Image not found error
Ensure your image file exists and the path is correct in `main.py`.

### Permission denied
Make sure the mounted volume has proper read permissions.

### Architecture mismatch
If you built the image on one architecture and are trying to run on another, rebuild the image on the target platform or use `docker buildx` for multi-arch builds.

## Example Output

```
['https://example.com/qr-code-data']
```
