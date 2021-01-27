import boto3
from botocore.config import Config

import argparse


def main():
    instance_id = parse_arg()
    ec2 = boto3.resource("ec2")

    # instance = get_instance(ec2, instance_id)
    # volume = get_volume_from_instance(instance)
    # snapshot = create_snapshot(volume)

    # encrypted_snapshot = copy_and_encrypt_snapshot(ec2, snapshot)

    encrypted_snapshot = ec2.Snapshot("snap-0d776d128b0ed90ac")
    encrypted_volume = create_volume_with_snapshot(ec2, encrypted_snapshot)
    print(encrypted_volume)

    pass


# Get instance id from args
def parse_arg():
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument("--instance-id")
    args = args_parser.parse_args()
    instance_id = args.instance_id

    return instance_id


# Get instance by id
def get_instance(ec2, instance_id):
    return ec2.Instance(instance_id)


# Get root volume
def get_volume_from_instance(instance):
    return list(instance.volumes.all())[0]


# Create snapshot
def create_snapshot(volume):
    snapshot = volume.create_snapshot()
    snapshot.wait_until_completed()

    return snapshot


# Copy snapshot & encrypt
def copy_and_encrypt_snapshot(ec2, snapshot):
    copied_snapshot = snapshot.copy(
        Encrypted=True, KmsKeyId="alias/aws/ebs", SourceRegion="ap-northeast-2"
    )
    new_snapshot = ec2.Snapshot(copied_snapshot["SnapshotId"])
    new_snapshot.wait_until_completed()


# Create volume
def create_volume_with_snapshot(ec2, snapshot):
    volume = ec2.create_volume(
        AvailabilityZone="ap-northeast-2a", SnapshotId=snapshot.id
    )

    return volume


# Create new instance
def create_new_instance(ec2, name, snapshot):
    new_instance = ec2.create_instance(
        BlockDeviceMappings=[{"VirtualName": name, "Ebs": {"SnapshotId": snapshot.id}}]
    )

    return new_instance


# Attach EIP to new instance

if __name__ == "__main__":
    main()