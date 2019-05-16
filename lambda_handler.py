import json
import os
import sys
import boto3
import uuid
import datetime
s3_client=boto3.client('s3')

def convert_transcript(infile,outfile):
    print ("Filename: ", infile)
    with open(outfile,'w+') as w:
            with open(infile) as f:
                    data=json.loads(f.read())
                    labels = data['results']['speaker_labels']['segments']
                    speaker_start_times={}
                    for label in labels:
                            for item in label['items']:
                                    speaker_start_times[item['start_time']] =item['speaker_label']
                    items = data['results']['items']
                    lines=[]
                    line=''
                    time=0
                    speaker='null'
                    i=0
                    for item in items:
                            i=i+1
                            content = item['alternatives'][0]['content']
                            if item.get('start_time'):
                                    current_speaker=speaker_start_times[item['start_time']]
                            elif item['type'] == 'punctuation':
                                    line = line+content
                            if current_speaker != speaker:
                                    if speaker:
                                            lines.append({'speaker':speaker, 'line':line, 'time':time})
                                    line=content
                                    speaker=current_speaker
                                    time=item['start_time']
                            elif item['type'] != 'punctuation':
                                    line = line + ' ' + content
                    lines.append({'speaker':speaker, 'line':line,'time':time})
                    sorted_lines = sorted(lines,key=lambda k: float(k['time']))
                    for line_data in sorted_lines:
                            line='[' + str(datetime.timedelta(seconds=int(round(float(line_data['time']))))) + '] ' + line_data.get('speaker') + ': ' + line_data.get('line')
                            w.write(line + '\n\n')

def lambda_handler(event, context):
    for record in event['Records']:
        bucket=record['s3']['bucket']['name']
        key=record['s3']['object']['key']
        localkey=os.path.basename(key)
        txtfile='output/'+localkey+'.txt'
        download_path = '/tmp/{}'.format(localkey)
        upload_path = '/tmp/{}.txt'.format(localkey)
        s3_client.download_file(bucket,key,download_path)
        convert_transcript(download_path,upload_path)
        s3_client.upload_file(upload_path, '{}'.format(bucket), txtfile)

    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
