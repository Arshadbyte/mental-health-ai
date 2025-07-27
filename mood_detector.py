
import cv2
from deepface import DeepFace

def detect_mood_from_image(image_path):
    """
    Detects mood from an image using DeepFace.
    Args:
        image_path (str): Path to the image file.
    Returns:
        dict: A dictionary containing detected emotions and their scores.
    """
    try:
        # DeepFace.analyze returns a list of dictionaries, one for each face found.
        # We'll take the first face found.
        analysis = DeepFace.analyze(img_path=image_path, actions=["emotion"], enforce_detection=False)
        if analysis:
            return analysis[0]["emotion"]
        else:
            return {"error": "No face detected in the image."}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # Example usage (requires an image file)
    # You can replace 'test_image.jpg' with a path to your own image
    # For testing, you might need to provide a dummy image or skip this block
    print("To test mood detection, provide an image path to detect_mood_from_image function.")
    print("Example: detect_mood_from_image(\"path/to/your/image.jpg\")")



