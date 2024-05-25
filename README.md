# serverless-e5-misw-4204

## Description
This is the 5th project for MISW 4204 Uniandes - 2024-02

## Deploy a gateway
Create an API specification file in Swagger Open API 2.0 syntax and deploy it.

## Deploy functions

**Important**: To deploy any function, you must copy the library_serverless_core library folder inside the
folder of the function you want to deploy. This since GCF will not try to link dependencies, it expects all the
code to be utilized to be inside the cloud function folder.

### Create User
```shell
gcloud functions deploy create-user \
  --region=us-central1 \
  --trigger-http \
  --entry-point create_user \
  --runtime python312 \
  --no-allow-unauthenticated \
  --gen2 \
  --service-account ? \
  --set-secrets="DATABASE_URL=?:?"
```

### Login User
```shell
gcloud functions deploy login-user \
  --region=us-central1 \
  --trigger-http \
  --entry-point login_user \
  --runtime python312 \
  --no-allow-unauthenticated \
  --gen2 \
  --service-account ? \
  --set-secrets="JWT_KEY=?:?,DATABASE_URL=?:?"
```

### Upload Video
```shell
gcloud functions deploy upload-video \
  --region=us-central1 \
  --trigger-http \
  --entry-point upload_video \
  --runtime python312 \
  --no-allow-unauthenticated \
  --gen2 \
  --service-account ? \
  --set-secrets="JWT_KEY=?:?,DATABASE_URL=?:?,DRONE_BUCKET=?:?,DRONE_PATH_TO_VIDEOS=?:?,PROJECT_ID=?:?,VIDEO_PROCESS_TOPIC_ID=?:?"
```

### Process Video
```shell
gcloud functions deploy process-video \
  --region us-central1 \
  --trigger-topic process-video-request \
  --runtime python312 \
  --entry-point process_video \
  --service-account ? \
  --gen2 \
  --set-secrets="JWT_KEY=?:?,DATABASE_URL=?:?"
```

### Get one Video
```shell
gcloud functions deploy get-one-video \
  --region=us-central1 \
  --trigger-http \
  --entry-point get_one_video \
  --runtime python312 \
  --no-allow-unauthenticated \
  --gen2 \
  --service-account ? \
  --set-secrets="JWT_KEY=?:?,DATABASE_URL=?:?"
```

### Get all Videos
```shell
gcloud functions deploy get-all-videos \
  --region=us-central1 \
  --trigger-http \
  --entry-point get_all_videos \
  --runtime python312 \
  --no-allow-unauthenticated \
  --gen2 \
  --service-account ? \
  --set-secrets="JWT_KEY=?:?,DATABASE_URL=?:?"
```

### Delete one Video
```shell
gcloud functions deploy delete-one-video \
  --region=us-central1 \
  --trigger-http \
  --entry-point delete_one_video \
  --runtime python312 \
  --no-allow-unauthenticated \
  --gen2 \
  --service-account ? \
  --set-secrets="JWT_KEY=?:?,DATABASE_URL=?:?,DRONE_BUCKET=?:?,DRONE_PATH_TO_VIDEOS=?:?"
```
