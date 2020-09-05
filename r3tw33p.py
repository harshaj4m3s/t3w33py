import tweepy
import json
import argparse


def get_access_token(file_name):
    '''Accepts json file name and returns the data from it
    This program expects the json file to be in this format:
    {
        "api":"CONSUMER_API",
        "api-key":"CONSUMER_API_KEY",
        "access-token":"ACCESS_TOKEN",
        "access-token-secret:"ACCESS_TOKEN_SECRET"
    }'''
    with open(file_name, 'r') as js:
        data = json.load(js)
    return data


def parse_arguments():
    '''Parse the command-line arguments'''
    parser = argparse.ArgumentParser(
        description='retweet the tweets based on keyword')
    parser.add_argument('--file', dest='file_name',
                        help='twitter api keys file', required=True)
    parser.add_argument('--keyword', dest='key', required=True,
                        help='keyword to be searched for retweet')
    parser.add_argument('--limit', dest='limit', required=False,
                        default=10, help='number of tweets to be retweeted')
    return parser.parse_args()


def main():
    ''' Main program which connects to the Twitter API and retweets based on some conditions'''
    args = parse_arguments()
    data = get_access_token(args.file_name)
    auth = tweepy.OAuthHandler(data['api'], data['api-key'])
    auth.set_access_token(data['access-token'], data['access-token-secret'])
    api = tweepy.API(auth)
    try:
        api.verify_credentials()
        print('Credentials verification  : success')
    except Exception as e:
        print(e)
    for tweet in tweepy.Cursor(api.search, args.key).items(int(args.limit)):
        try:
            tweet.retweet()
        except tweepy.TweepError as te:
            print(te.reason)
        except StopIteration:
            break


if __name__ == '__main__':
    main()
