FILE_TYPES = [
    "txt",
    "jpg",
    "jpeg",
    "png",
]


def create_input_image(data_uri):
    return {
        "role": "user",
        "content": [
            {
                "type": "input_image",
                "detail": "auto",
                "image_url": data_uri,
            }
        ],
    }


# end
