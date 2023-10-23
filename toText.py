def detect_text_uri(uri):
    """Detects text in the file located in Google Cloud Storage or on the Web."""
    from google.cloud import vision

    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = "https://scontent-ord5-2.cdninstagram.com/v/t51.2885-15/370756379_1025149722260803_1282863242509454581_n.jpg?stp=dst-jpg_e35&_nc_ht=scontent-ord5-2.cdninstagram.com&_nc_cat=107&_nc_ohc=HNZeSQwbZvUAX_JCvIS&edm=ACWDqb8BAAAA&ccb=7-5&ig_cache_key=MzE3OTUyNTUyNzQ2MTY5NjIyNQ%3D%3D.2-ccb7-5&oh=00_AfAqX_6wJE00STZvZvM_sBIF40FhSxmmt6hGSbo_fYIaRQ&oe=651E833B&_nc_sid=ee9879"

    response = client.text_detection(image=image)
    texts = response.text_annotations
    print("Texts:")

    for text in texts:
        print(f'\n"{text.description}"')

        vertices = [
            f"({vertex.x},{vertex.y})" for vertex in text.bounding_poly.vertices
        ]

        print("bounds: {}".format(",".join(vertices)))

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )