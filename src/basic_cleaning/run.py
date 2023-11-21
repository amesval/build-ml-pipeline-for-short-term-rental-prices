#!/usr/bin/env python
"""
 Download from W&B the raw dataset and apply some basic data cleaning, exporting the result to a new artifact
"""
import argparse
import logging
import wandb
import pandas as pd
import os


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    logger.info("Downloading artifact")
    artifact_path = run.use_artifact(args.input_artifact).file()
    logger.info("Reading artifact: input dataset")
    df = pd.read_csv(artifact_path)

    logger.info("Cleaning dataset")
    idx = df['price'].between(args.min_price, args.max_price)
    df = df[idx].copy()
    # Convert last_review to datetime
    df['last_review'] = pd.to_datetime(df['last_review'])

    idx = df['longitude'].between(-74.25, -73.50) & df['latitude'].between(40.5, 41.2)
    df = df[idx].copy()

    filename = "clean_sample.csv"
    df.to_csv(filename, index=False)

    logger.info("Creating output artifact: clean dataset")
    artifact = wandb.Artifact(
     name=args.output_artifact,
     type=args.output_type,
     description=args.output_description,
    )
    artifact.add_file(filename)
    logger.info("Logging output artifact")
    run.log_artifact(artifact)

    os.remove(filename)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="A very basic data cleaning")

    print(parser)

    parser.add_argument(
        "--input_artifact", 
        type=str,
        help="Name of the datataset artifact to clean",
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type=str,
        help="Name of the clean dataset",
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str,
        help="Type of the artifact to create",
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type=str,
        help="Dataset that drops outliers for price attribute.",
        required=True
    )

    parser.add_argument(
        "--min_price", 
        type=float,
        help="Min limit of the price value.",
        required=True
    )

    parser.add_argument(
        "--max_price", 
        type=float,
        help="Max limit of the price value.",
        required=True
    )


    args = parser.parse_args()

    go(args)
