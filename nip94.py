from nostrpublish import nostrpost
import os
import blurhash
import requests
from PIL import Image
from io import BytesIO
import hashlib

private_key = os.environ["nostrdvmprivatekey"]

def compute_sha256(data):
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def gifmetadata(gifUrl, gifSize, gifDims, thumb, preview, alt, searchTerm):
    # Blurhash
    response = requests.get(preview)
    response.raise_for_status()
    image = Image.open(BytesIO(response.content))
    blur_hash = blurhash.encode(image, x_components=4, y_components=3)

    # Post 1063 File Metadata Event
    kind = 1063
    content = searchTerm
    hash = str(compute_sha256(gifUrl))
    if hash is not None:
        tags = [["url", gifUrl],
                ["m", "image/gif"],
                ["x", hash],
                ["ox", hash],
                ["size", str(gifSize)],
                ["dim", str(gifDims)],
                ["blurhash", blur_hash],
                ["thumb", thumb],
                ["image", preview],
                ["summary", searchTerm],
                ["alt", alt]
                ]
        
        event_id = nostrpost(private_key,kind,content,tags)

    return event_id

if __name__ == "__main__":
    gifUrl = "https://media.tenor.com/tIPGwbBysUoAAAAC/ruh-roh.gif"
    gifSize = "869458"
    gifDims = "[498, 329]"
    thumb = "https://media.tenor.com/tIPGwbBysUoAAAAT/ruh-roh.png"
    preview = "https://media.tenor.com/tIPGwbBysUoAAAAN/ruh-roh.png"
    alt = "ruh-roh"
    searchTerm = "ruh roh"

    gifmetadata(gifUrl, gifSize, gifDims, thumb, preview, alt, searchTerm)
# {
#   "kind": 1063,
#   "tags": [
#     ["url","https://media.tenor.com/6TcA9vRym4MAAAAC/laugh-mock.gif"],
#     ["m", "image/gif"],
#     ["x",<Hash SHA-256>],
#     ["ox",<Hash SHA-256>],
#     ["size", 28257],
#     ["dim", "203x200"],
#     ["magnet",<magnet URI> ],
#     ["i",<torrent infohash>],
#     ["blurhash", <value>],
#     ["thumb", "https://media.tenor.com/6TcA9vRym4MAAAAT/laugh-mock.png"],
#     ["image", "https://media.tenor.com/6TcA9vRym4MAAAAe/laugh-mock.png"],
#     ["summary", liotta mock laugh],
#     ["alt", ["laugh", "mock", "lol", "hysterical", "rofl"]]
#   ],
#   "content": "liotta mock laugh",
#   ...
# }


            # ['EVENT', 
            #  {'id': 'd35bc3f318f1c0dc3884371ed7d928e401e003a3c7b110c66a4354de8b8e106d', 
            #   'pubkey': '18059c49c526b873d59e0798b0c892d9171114927dfccdc9b4aa7d45e8c2c314', 
            #   'created_at': 1720584193, 
            #   'kind': 1063, 
            #   'tags': [['url', 'https://image.nostr.build/a9b70576d8cc1e778e4d58b3b46942fff30fd611454ad57a1a08f044126da9b4.jpg'], 
            #            ['m', 'image/jpeg'], 
            #            ['alt', 'Verifiable file url'], 
            #            ['x', 'b083689218db941e132c5094e23e45640e937b9122dced6c6860ceccd0785d59'], 
            #            ['size', '53027'], 
            #            ['dim', '828x746'], 
            #            ['blurhash', ';tODd^~qIUae%MRjtRaeofx]D%t7xuWCRjt8f6WBtRaet7Rjf6ozRjayj[xuWBWVj[jZa}aekCae%MRjj[ofWBj[j]WBj[xuWBofWBazofWBaeofV@a}ofWBj[ofR*t6ayWBt7WBayayofWBs:WV'], 
            #            ['ox', 'a9b70576d8cc1e778e4d58b3b46942fff30fd611454ad57a1a08f044126da9b4']], 
            #            'content': '', 
            #            'sig': '42c7c139429a829498f5c158972d0d39aa3a4bc32e351f5404a060b3990b24108f5fd2bb449abc9a623c7db165b52b88470feaef04cb176043a71f23c73cd1eb'}]
