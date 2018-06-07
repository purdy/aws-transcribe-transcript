# aws-transcribe-transcript
This is a simple utility script to convert the Amazon Transcribe .json transcript into a more readable transcript.

Amazon has a neat Transcription service and you can have the service identify speakers. And in their web interface, they show you a neat play-by-play transcript, but it's limited to the first 5,000 characters. If you want the full transcript, you have to download their JSON file. However, the JSON file only has the transcript as a big block and then some structured data below for the various speakers, start times, and text fragments.

This script creates a transcript that's human-readable.

## Directions

1. Download your Transcription from the Job Details page. The filename format is currently asrOutput.json.
2. Run the `transcript.php` program on the downloaded file, i.e. `php ./transcript.php asrOutput.json`
3. Results will be written in your current working directory as `[FILENAME]-transcript.txt`
