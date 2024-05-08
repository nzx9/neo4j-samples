import google.generativeai as genai
import re
from neo4j import GraphDatabase


GEMINI_API_KEY = "" # Fill this

class CypherGemini:
    def __init__(self, username, password, host="bolt://localhost:7687") -> None:
        self.host = host
        self.username = username
        self.password = password
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')


    def generate(self, prompt):
        prompt_template_cypher = f"You are a cypher code generating tool. Create cypher code to create nodes for the following data with appropriate labels and relationships: {prompt}. just return the cyper code only. Don't include code comments. Give code as list of commands as plain text."
        print("(cypher) prompt template")
        print("------------------------------------")
        response = self.model.generate_content(prompt_template_cypher)
        print(response)
        result = response.text
        pr, cypher = self.extract_cypher(result)

        if pr:
            print("(cypher) generated:")
            print("------------------------------------")
            print(cypher)

            # cypher = cypher.split("\n")
            
            return cypher
        else:
            return "Failed to generate Cypher query."
        
    def execute(self, cypher):
        try:
            driver = GraphDatabase.driver(self.host, auth=(self.username, self.password))
            with driver.session() as session:
                statements = cypher.split("\n")
                # print(statements)
                for statement in statements:
                    if statement.strip():
                        try:
                            result = session.run(statement)
                            print(f"Cypher statement executed successfully.")
                        except Exception as e:
                            # print(f"Cypher statement failed: {statement}\nError: {e}")
                            pass
                print("Cypher query executed successfully.")
        except Exception as e:
            print("Cypher query failed: " + str(e))

    def extract_cypher(self, text):
        pattern = r'```(.*?)```'
        matches = re.search(pattern, text, re.DOTALL)

        if matches:
            print(matches)
            code = matches.group(1)
            return True, code.strip()
        else:
            return True, text