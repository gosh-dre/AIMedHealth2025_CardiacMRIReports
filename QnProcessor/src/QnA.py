from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline
import json
import re
import fnmatch
import os
import time
# Configs.

SourceJsonFiles   = r'./json_interim/'
OutputFolderPath  = r'./output/' 
PromptfilePath    = r'./prompts/prompt.json'





class QnA():

    def __init__(self,processconfig):
        
        self.pipeline_config = processconfig
        self.nlp_pipeline = pipeline(processconfig['PipelineName'], model=processconfig['ModelPath'], tokenizer=processconfig['ModelPath'])


    def Run_QnAOnJson(self,report):
        """
        Perform Question and Answer (QnA) on a JSON report.

        Parameters:
        - report (str): The unstructured text from a patient report.

        Returns:
        - Tuple[Dict[str, Dict], Dict[str, Dict]]: A tuple containing two dictionaries - log_dict and insight_dict.
        - log_dict: Contains detailed logging information for each QnA prompt.
        - insight_dict: Contains insights extracted from the QnA process.
        """



        promptfile      = json.load(open(self.pipeline_config['PromptfilePath']))
        NumberofPrompts = len(promptfile)


        context         = "Following is an extracted unstructured text from a report of a patient in the GOSH NHS Hospital,"
        questionPretext = "From the given unstructured text,"
        questionPretext = ""

        log_dict      = {}
        insight_dict  = {}

        
        log_dict['context'] = context+report
        start_QnAmoduletime = time.time()

        
        for index in promptfile:

            prompt          = promptfile[str(index)]
            question        = questionPretext + prompt['Prompt']
            label           = prompt['label']

            start_qna_instant = time.time()
            # question      = "From the given unstructured text,What is the "+label+" ?"
            QA_input      = {
                                'question': question,
                                'context': context+report 
                            }

            res = self.nlp_pipeline(QA_input)

            
            insight_dict[label]                = {}
            insight_dict[label]['text']        = str(res['answer'])
            # insight_dict[label]['score']       = str(res['score'])
            end_QnAInstant = time.time()

            log_dict[label] = {
                                    'score': str(res['score']),
                                    'start': str(res['start']),
                                    'end': str(res['end']),
                                    'question': question,
                                    'answer': str(res['answer']),
                                    'time_for_processing': time.time() - start_qna_instant
                                }

        
        end_QnAmoduletime = time.time()
        elapsed_time = end_QnAmoduletime - start_QnAmoduletime    
        log_dict['Totaltimeforprocessing']  = elapsed_time
            
        return log_dict,insight_dict


    def split_and_merge(self,text: str, line_number: int) -> str:
        """
        Split the input text into sentences using '\n' as the delimiter,
        then merge sentences up to the specified line_number using '[SEP]' as a separator.

        Parameters:
        - text (str): The input text to be split and merged.
        - line_number (int): The line number up to which sentences should be merged.

        Returns:
        - str: The merged text up to the specified line_number, separated by '[SEP]'.
        If the line_number is invalid, returns "Invalid line number."
        """
        # Split the text into sentences using '\n' as the delimiter
        sentences = text.split('\n')

        # Ensure the line_number is within a valid range
        if line_number < 1 or line_number > len(sentences):
            return "Invalid line number"

        # Merge sentences up to the specified line_number using '[SEP]' as a separator
        merged_text = '[SEP]'.join(sentences[:line_number])

        return merged_text


    def write_tojson(self,file_path, dict_data):
        """
        Write a dictionary to a JSON file with the specified file path and indentation.

        Parameters:
        - file_path (str): The path to the JSON file to be written.
        - dict_data (dict): The dictionary data to be written to the JSON file.

        Returns:
        - bool: True if the writing process is successful, False otherwise.
        """
        try:
            # Save the dictionary to a JSON file using json.dump() with specified indentation
            with open(file_path, 'w') as json_file:
                json.dump(dict_data, json_file, indent=4)
            return True  # Return True if writing is successful

        except Exception as e:
            
            # Print an error message if an exception occurs
            print(f"Error writing to JSON file '{file_path}': {e}")
            
            return False  # Return False if writing fails

    def getjsonfilelist(self,folder_path) -> list[str]:
        """
        Get a list of paths to JSON files in the specified folder and its subdirectories.

        Parameters:
        - folder_path (str): The path to the folder to search for JSON files.

        Returns:
        - list: A list of paths to JSON files in the specified folder and its subdirectories.
        """

        json_files = []
        for root, dirnames, filenames in os.walk(folder_path):
            for filename in fnmatch.filter(filenames, '*.json'):
                json_files.append(os.path.join(root, filename))
        return json_files


    def parsejsonforreport(self,filename):

        """
        Parse a JSON file containing information about a report.

        Parameters:
        - filename (str): The path to the JSON file.

        Returns:
        - Tuple[str, str]: A tuple containing the parsed report text and PDF filename.
        """

        PAGENO       = 1
        NoLines      = 12

        jsonstore    = json.load(open(filename))
        PDF_filename = jsonstore['file_name']
        No_pages     = jsonstore['number_of_pages']
        No_tables    = jsonstore['number_of_tables']
        text_pages   = jsonstore['raw_text_per_page']
        table_pages  = jsonstore['tables_extracted']
        reporttext   = self.split_and_merge(text_pages['1'],NoLines)   
        return reporttext,PDF_filename


    def StoreInsightsAndLogs(self,Insight,Logs,PDF_filename):
        """
        Store insights and logs in JSON files.

        Parameters:
        - insight (dict): Dictionary containing insights.
        - logs (dict): Dictionary containing logs.
        - pdf_filename (str): Name of the PDF file.

        Returns:
        - None
        """
        json_ofreport               = {}
        log_ofreport                = {}
        json_ofreport['file name']  = PDF_filename
        json_ofreport['Insights']   = Insight
        
        log_ofreport['file name']   = PDF_filename
        log_ofreport['Logs']        = Logs
    
        Insights_file_path                    = self.pipeline_config['OutputFolderPath'] +"/Insights/"+ PDF_filename.replace(".pdf", "") +"_Insights.json"
        self.write_tojson(Insights_file_path,json_ofreport)
        logfile_path                          = self.pipeline_config['OutputFolderPath'] +"/Logs/"+ PDF_filename.replace(".pdf", "") +"_log.json"
        self.write_tojson(logfile_path,log_ofreport)
