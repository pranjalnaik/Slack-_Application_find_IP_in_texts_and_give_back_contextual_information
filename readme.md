# IP Address Information using VirusTotal API

## Introduction

The slack bot monitors all messages passing through any channel of a workspace and gives out contextual information if the message contains an IP address. For this application, information such as Network subnet, IP origin Country, Owner and Harmlessness factors are considered. 

This application uses VirusTotal API to pass this contextual information back to the user. The VirusTotal API lets you upload and scan files or URLs, access finished scan reports and make automatic comments without the need of using the website interface.
Please find more information about VirusTotal here: https://developers.virustotal.com/reference/overview

## Requirements

Please find the system requirements in requirements.txt

## Installation

1. Create a Workspace on slack using the link - https://slack.com/help/articles/206845317-Create-a-Slack-workspace
2. Create a slack application in the Workspace using the link - https://api.slack.com/apps 
3. Add OAuth Scopes for the bot and make a note of bot token
4. Copy the zip file of the application and run it on any IDE which supports python.

## Configuration

This application makes use of free version of ngrok(3.0.6). Ngrok is a cross-platform application that exposes local server ports to the Internet. This free version comes with a 2 hour limit per session, with each session having a unique *Request URL*. This Request URL needs to be updated on the slack workspace as well for the application to function. This issue can be eliminated by getting a paid version of ngrok.

## Mainainers

Pranjal Naik - pnaik13@hawk.iit.edu