# 메시지 처리 앱
import boto3

import time
import random

def main():
    sqs = boto3.resource("sqs")

    queue = sqs.get_queue_by_name(QueueName="vote.fifo")

    while True:
        for message in queue.receive_messages():
            print(message.body)

            message.delete()

        time.sleep(random.randint(15, 30))


if __name__ == "__main__":
    main()