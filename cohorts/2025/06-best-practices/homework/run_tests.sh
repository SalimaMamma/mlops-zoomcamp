echo "Starting localstack..."
docker-compose up -d localstack

echo "Waiting for localstack to be ready..."
#sleep 10

echo "Setting dummy AWS credentials, because otherwise it will fail"
export AWS_ACCESS_KEY_ID="test"
export AWS_SECRET_ACCESS_KEY="test"
export AWS_DEFAULT_REGION="us-east-1"

echo "Creating S3 bucket"
export S3_ENDPOINT_URL="http://localhost:4566"
aws --endpoint-url=${S3_ENDPOINT_URL} s3 mb s3://nyc-duration

echo "Verifying bucket creation..."
aws --endpoint-url=http://localhost:4566 s3 ls

echo "Running unit tests..."
export INPUT_FILE_PATTERN="s3://nyc-duration/in/{year:04d}-{month:02d}.parquet"
export OUTPUT_FILE_PATTERN="s3://nyc-duration/out/{year:04d}-{month:02d}.parquet"
python -m pytest tests/test_batch.py -v

echo "Running integration tests..."
python -m pytest -s tests/integration_test.py -v


echo "Verifying test data file size..."
aws --endpoint-url=http://localhost:4566 s3 ls s3://nyc-duration/in/ --recursive --human-readable