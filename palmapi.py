import pprint
import google.generativeai as palm
def extractDate(text_entry):
    palm.configure(api_key='AIzaSyAc-sjC_3QK02mlhoU5ygWiYkYUOG5ixvU')

    prompt = """
    list any event related to a certain time in the following text in the format 08/28/2023$3:00PM to 5:00PM$Mckelvey Fair by Washu Robotics without adding anything not provided, if there is not any event related to a time, simply return "no event" 
    """
    reply = palm.chat(context=prompt, messages=text_entry)
    
    return (reply.last)
# completion = palm.generate_text(
#     model="models/text-bison-001",
#     prompt= """
#     summarize any event related to a certain time in the following text in the format: 08/28/2023: Mckelvey Fair by Washu Robotics
#     """+"""Mckelvey Fair on Aug 28 @5-6:30pm at Lopata Gallery, WashU activities fair on Sep 1 @3-5pm at Mudd Field"""
#     temperature=0,
#     # The maximum length of the response
#     max_output_tokens=800,
# )

# print(completion.result)
print(extractDate("Mckelvey Fair on Aug 28 @5-6:30pm at Lopata Gallery, WashU activities fair on Sep 1 @3-5pm at Mudd Field"))