import argparse
try:
    import boto3
    from botocore.exceptions import ClientError
except ImportError:
    raise SystemExit("[-] Missing dependency! Please install boto3: pip install boto3")

def audit_s3_bucket(bucket_name: str) -> None:
    """Inspect an S3 bucket's Public Access Block configuration."""
    s3_client = boto3.client("s3")

    print(f"\n[+] Auditing S3 Bucket: {bucket_name}")
    try:
        response = s3_client.get_public_access_block(Bucket=bucket_name)
        config = response.get("PublicAccessBlockConfiguration", {})

        block_public_acls = config.get("BlockPublicAcls", False)
        ignore_public_acls = config.get("IgnorePublicAcls", False)
        block_public_policy = config.get("BlockPublicPolicy", False)
        restrict_public_buckets = config.get("RestrictPublicBuckets", False)

        all_blocked = all([block_public_acls, ignore_public_acls, block_public_policy, restrict_public_buckets])

        print(f"  - Block Public ACLs:       {block_public_acls}")
        print(f"  - Ignore Public ACLs:      {ignore_public_acls}")
        print(f"  - Block Public Policy:    {block_public_policy}")
        print(f"  - Restrict Public Buckets: {restrict_public_buckets}")

        if all_blocked:
            print("  [+] STATUS: Fully Secured against public access.")
        else:
            print("  [!] WARNING: Bucket has missing public access block restrictions!")

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "NoSuchPublicAccessBlockConfiguration":
            print("  [!] CRITICAL: No Public Access Block configured! Bucket settings may allow exposure.")
        elif error_code == "NoSuchBucket":
            print("  [-] Error: Target bucket does not exist.")
        else:
            print(f"  [-] AWS Error: {e.response['Error']['Message']}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit AWS S3 Bucket Public Settings")
    parser.add_argument("-b", "--bucket", required=True, help="Target AWS S3 Bucket Name")
    
    args = parser.parse_args()
    audit_s3_bucket(args.bucket)