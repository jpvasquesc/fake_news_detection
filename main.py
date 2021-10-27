import argparse
from pathlib import Path
import glob
import pandas as pd
import pickle


def main():
    """
    Classify input text as 'fake' or 'real' using the pre-trained machine learning model.
    """
    # Get command-line arguemnts
    args = parse_arguments()
    
    # Create a dataframe with the input texts
    if args.file:
        pattern_path = args.file
        files = glob.glob(pattern_path)
        texts = get_text_from_file(files)

    else:
        texts = pd.DataFrame(data={"text": [args.text]})
        
    # Predict text classification with ML model
    predictions = classsify_input_text(texts)
    
    # Print predictions to user
    predictions = predictions.drop(columns="text")
    predictions = predictions.sort_values("prediction")
    print(predictions)
    
    
def parse_arguments() -> argparse.Namespace:
    """
    Create a command-line menu for this script using 'argparse'.
    """
    parser = argparse.ArgumentParser(prog="Fake news detection ML model",
                                     description="Predict if input text is 'fake' or 'real'")
    
    input_methods = parser.add_mutually_exclusive_group(required=True)
    input_methods.add_argument('-t', '--text', dest='text', type=str, help="Input text from the command line")
    input_methods.add_argument('-f','--file', dest='file', type=str, help="Input text from one or more .txt files")

    return parser.parse_args()


def get_text_from_file(files: list) -> pd.DataFrame:
    """
    Check if input is files are correct.
    Get the text inside each .txt file in 'files'.

    Args:
        files (list): List of .txt files
        
    Returns:
        pd.Dataframe: DataFrame of texts, with filename as index
    """
    df = pd.DataFrame(columns={"file": [], "text": []})
    
    for file in files:

        file_path = Path(file)
        file_name = file_path.stem
        file_extension = file_path.name[-4:]
        
        # 'file' has .txt extension
        if file_extension != ".txt":
            raise IOError("Input file '{0}' has an extension different from .txt".format(file_path))
    
        with open(file_path, "r", encoding="UTF-8") as f:
            text = f.read()
            row = {"file": file_name, "text": text}
            df = df.append(row, ignore_index = True)
            
    return df.set_index("file")
    
    
def classsify_input_text(text_df: pd.DataFrame) -> pd.DataFrame:
    """
    Utilize the ML model to predict if the text is 'fake' or 'real'.

    Args:
        text_df (pd.Dataframe): DataFrame with input texts
    
    Returns:
        pd.Dataframe: DataFrame with the prediction for each text
    """
    # Load ML model
    model_path = Path("./model.sav")
    model = pickle.load(open(model_path, "rb"))

    # Pass input through model
    prediction = model.predict(text_df.text)
    text_df["prediction"] = prediction     
    
    return text_df
     
     
if __name__ == "__main__":
    main()