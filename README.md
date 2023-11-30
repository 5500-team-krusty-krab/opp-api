# Project File

## Deployment

### Docker

#### Install Docker Desktop
Visit Docker’s official website and download and install Docker Mac Intel Chip version
Attention: Docker can only run on macOS system above 12.0, no matter Apple silicon or Intel chip 

#### Build Docker image
Run in the project root directory backend
```bash
docker build -t myimage .
```

#### Run Docker container
```bash
docker run -d --name mycontainer -p 8000:8000 myimage
```

#### Test Docker container status
```bash
 run http://localhost:8000 at local engine
```