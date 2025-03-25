import cv2
import pytesseract
from tqdm import tqdm

def extract_text_from_video(video_path, output_text_file, frame_interval=1, unique_only=False):
    """
    Extract text from a video file and save it to a text file.
    
    This function can:
      - Process every nth frame, reducing processing load if desired.
      - Optionally compare OCR results with the previous frame's text and
        only save unique results.
    
    Parameters:
    - video_path: Path to the input video file.
    - output_text_file: Path to the output text file.
    - frame_interval: Process every nth frame (default=1 processes every frame).
    - unique_only: If True, only save text if it is non-empty and differs from the previous frame.
    """
    # Optionally, set the tesseract_cmd if it's not in your PATH:
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    # Open the video file
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error opening video file.")
        return

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    extracted_text = []
    prev_text = None
    frame_count = 0

    # Initialize progress bar
    pbar = tqdm(total=total_frames, desc="Processing Frames")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Process only every nth frame
        if frame_count % frame_interval == 0:
            # Convert frame to grayscale for better OCR performance
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            current_text = pytesseract.image_to_string(gray).strip()

            if unique_only:
                # Append only if text is non-empty and different from the previous frame
                if current_text and current_text != prev_text:
                    extracted_text.append(f"Frame {frame_count}:\n{current_text}\n{'-'*40}\n")
                    prev_text = current_text
            else:
                extracted_text.append(f"Frame {frame_count}:\n{current_text}\n{'-'*40}\n")
        
        frame_count += 1
        pbar.update(1)

    pbar.close()
    cap.release()

    # Save the extracted text to the output file
    with open(output_text_file, 'w', encoding='utf-8') as f:
        f.writelines(extracted_text)

    print(f"\nText extraction complete. Output saved to {output_text_file}")

if name == "main":
    # If needed, set the tesseract_cmd to the path where Tesseract is installed:
    # pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    # Path to your video file (use a raw string to handle backslashes on Windows)
    video_path = r"C:\Users\syeda\Videos\Event Chat Log.mp4"
    # Path to the output text file where extracted text will be saved
    output_text_file = "extracted_text.txt"

    # Adjust parameters as needed:
    #   frame_interval=30: processes every 30th frame for performance.
    #   frame_interval=1: processes every frame for more accuracy.
    #   unique_only=True: saves text only when it's different from the previous frame.
    extract_text_from_video(video_path, output_text_file, frame_interval=30, unique_only=True)
