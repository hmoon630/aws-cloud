# 메시지 전송 앱
import boto3

import time
import random


def main():
    sqs = boto3.resource("sqs")

    queue = sqs.get_queue_by_name(QueueName="vote.fifo")

    print(f"Sending Messages To {queue.url}")
    while True:
        time.sleep(random.randint(1, 15))

        vote = random.randint(1, 5)
        response = queue.send_message(
            MessageBody=str(vote),
            MessageDeduplicationId=str(int(time.time())),
            MessageGroupId="main",
        )
        print(f"Sent! MessageBody={vote}")


if __name__ == "__main__":
    main()