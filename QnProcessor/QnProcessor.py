from src.QnA import QnA
import logging
import time
import sys
import datetime

logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s',  handlers=[
        logging.FileHandler('./logreports/processing.log'),
        logging.StreamHandler(sys.stdout)
    ])


process_config = {
                    'ModelName'        : r'roberta-large-squad2-hp',
                    'PipelineName'     : r'question-answering',
                    'ModelPath'        : r'./Models/roberta-large-squad2-hp',
                    'SourceJsonFiles'  : r'./JSONInput/',
                    'OutputFolderPath' : r'./JSONOutput/',
                    'PromptfilePath'   : r'./prompts/prompt.json'
                 }

# Create an instance of the QnA class
qna_instance = QnA(process_config)
logging.info(f"NLP Pipeline Initialised: {datetime.datetime.now()}")

# Invoke the test() function
# result = qna_instance.QnAprocess()

def QnAprocess():
        
        # Get the JSON file list in the specified folder and its subdirectories.
        jsonfilelist     = qna_instance.getjsonfilelist(process_config['SourceJsonFiles'])
        succesfullfiles  = 0
        Totaltimeforprocessing = 0
        for jsonfile in jsonfilelist:
            
            try:
                logging.info(f"Processing started on : {jsonfile} -> :{datetime.datetime.now()}")
                reportext,PDF_filename     =  qna_instance.parsejsonforreport(jsonfile)
                logging.info(f"Parsed report text from JSON report : {datetime.datetime.now()}")
                start_time = time.time()
                log_dict,insight_dict      = qna_instance.Run_QnAOnJson(reportext)
                logging.info(f"Processed JSON using NLP Transformer : {datetime.datetime.now()}")
                qna_instance.StoreInsightsAndLogs(insight_dict,log_dict,PDF_filename)
                logging.info(f"Stored Insights and Logs succesfully : {datetime.datetime.now()}")
                end_time  = time.time()
                logging.info(f"Processing completed succesfully for : {PDF_filename} Time taken for the process to complete :{end_time-start_time}")
                succesfullfiles = succesfullfiles + 1
                Totaltimeforprocessing = Totaltimeforprocessing + (end_time-start_time)

            except Exception as e:
                
                logging.error(f"Error processing file: {jsonfile} - Error: {str(e)}")


        logging.info(f"Summary: No of files processed succesfully: {succesfullfiles}")
        logging.info(f"Summary: No of files failed to process: {len(jsonfilelist)-succesfullfiles}")
        logging.info(f"Summary: Total time taken for  processed (sec): {Totaltimeforprocessing}")

# Print the result
QnAprocess()