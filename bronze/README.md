To build:

```
docker build -t bronze-etl-app .
```

To run:

```
docker run -p 8080:8080 bronze-etl-app
```

To execute:

```
curl -X POST http://localhost:8080/process-zip
```

To deploy:

```
gcloud run deploy your-service-name --image gcr.io/your-project/your-image-name --platform managed --region your-region --allow-unauthenticated
```