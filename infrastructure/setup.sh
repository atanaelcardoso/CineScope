echo "=========== INICIALIZANDO RECURSOS AWS VIA LOCALSTACK ==========="

awslocal s3 mb s3://cinescope-media-bucket

awslocal sns create-topic --name cinescope-movie-events

cd /etc/localstack/init/ready.d/../.. || exit
zip -j lambda.zip /etc/localstack/init/ready.d/../../infrastructure/lambda/index.py

awslocal lambda create-function \
    --function-name cinescope-movie-processor \
    --runtime python3.10 \
    --role arn:aws:iam::000000000000:role/lambda-role \
    --handler index.handler \
    --zip-file fileb://lambda.zip

echo "=========== RECURSOS AWS CRIADOS COM SUCESSO ==========="
