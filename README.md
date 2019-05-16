This is a port of purdy/aws-transcribe-transcript intended to run as an AWS Lambda function

# aws-transcribe-transcript
This is a simple utility script to convert the Amazon Transcribe .json transcript into a more readable transcript.

Amazon has a neat Transcription service and you can have the service identify speakers. And in their web interface, they show you a neat play-by-play transcript, but it's limited to the first 5,000 characters. If you want the full transcript, you have to download their JSON file. However, the JSON file only has the transcript as a big block and then some structured data below for the various speakers, start times, and text fragments.

This script creates a transcript that's human-readable.

## Regular Directions

1. Download your Transcription from the Job Details page. The filename format is currently asrOutput.json.
2. Run the `transcript.py` program on the downloaded file, i.e. `python ./transcript.py asrOutput.json`
3. Results will be written in your current working directory as `[FILENAME]-transcript.txt`

## S3/Lambda Directions

1. Create an S3 bucket with two folders; input/ and output/
2. Create a Lambda function that triggers on CreateObject in input/ (Triggers section of the UI)
3. Give the function access to write to S3/output (Resources section of the UI)
4. Place json file in S3/input and wait a few seconds for your transcript to show up in output/
