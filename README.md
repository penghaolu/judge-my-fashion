# judge-my-fashion

## Description
A program that uses deep neural networks to analyze and determine your primary fashion style and then insult it accordingly.

View the demo: https://www.youtube.com/watch?v=agqwDCULiO4

Built with: TensorFlow, YOLOv3, React, Flask

Winner of Bitcamp 2021 for Most Entertaining Hack: https://devpost.com/software/judge-my-fashion



# MacOS First Time Setup Instructions
These instructions assume you have cloned the codebase and have python3 and conda installed.

## Downloading the necessary files
We have not included the weights for YOLOv3 in our codebase due to their file size. You can download them at the following links:

  1. https://pjreddie.com/media/files/yolov3.weights
  2. https://github.com/pjreddie/darknet/blob/master/cfg/yolov3.cfg

Once downloaded, move these two files into `judge-my-fashion/server/configs/`.

## Creating the conda environment
A file containing the exported conda environment that includes all the necessary dependencies has been included in the codebase. To install the environment from this file, first navigate to the main `judge-my-fashion/` directory containing the `environment.yml` file. Now run:

    conda env create -f environment.yml

To activate the new environment:

    conda activate judgemyfashion
    
If properly installed, you should now see `(judgemyfashion)` in front of your shell prompt.



# Hosting Instructions


## Start Flask server
Open a new terminal and activate your conda environment with `conda activate judgemyfashion`. Navigate into `judge-my-fashion/server/`. From there, run:

    export FLASK_APP=server.py
    python -m flask run

If successful, you should see the following:

     * Serving Flask app "server.py"
     * Environment: production
       WARNING: This is a development server. Do not use it in a production deployment.
       Use a production WSGI server instead.
     * Debug mode: off
    INFO: Initialized TensorFlow Lite runtime.
     * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

## Start Frontend
Open a new terminal and activate your conda environment with `conda activate judgemyfashion`. Navigate into `judge-my-fashion/frontend/`. From there, run:

    npm install
    npm start
    
If successful, the working web app should automatically open in your default browser.


