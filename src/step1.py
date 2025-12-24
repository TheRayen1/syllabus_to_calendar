import pypdf
import google.generativeai as genai


genai.configure(api_key="xx")

def main():
    pdf_path = input("Enter syllabus file name: ")
    pdf_path += ".pdf"
    course = input("Enter course name: ")
    text= extract_text_pypdf(pdf_path)
    response = api(text)
    print(response.text)

def extract_text_pypdf(pdf_path):
    """Extract text from PDF using pypdf"""
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = pypdf.PdfReader(file)
        
        print(f"Number of pages: {len(reader.pages)}")
        
        for page_num, page in enumerate(reader.pages, 1):
            page_text = page.extract_text()
            #text += f"\n--- Page {page_num} ---\n"
            text += page_text + "\n"
    
    return text
def api(text): 
    prompt= "find all my assignments + dates for this class. Only return Assignment name + dates in MM/DD/2025 format. Do not output anything else. IF DOCUMENT DOES NOT EXPLICITY STATE THE DATE, DO NOT RETURN ANYTHING"
    model = genai.GenerativeModel("gemini-2.5-flash-lite")
    text += prompt
    response = model.generate_content(text)
    return response

if __name__ == "__main__":
    main()
