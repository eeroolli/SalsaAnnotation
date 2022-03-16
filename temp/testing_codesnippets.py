

from datetime import datetime


def clean(string):
    import re
    clean_string = string.replace("/", "-").replace(" ", "_") 
    clean_string = re.sub("""[/{/}!();:'/" \,<>?@#$%^&*~]""", "", clean_string)
    clean_string = clean_string.strip()
    clean_string = clean_string.lstrip("_") #starting a name with _ leads to funny names in Markdown
    return clean_string

coreo = "_First"
video_background = "Black"
dance_role = "Leader/Male"
salsa_style = "NY/On2"
uploaded_filename = "Testing_Up }load_to_s3.mp4"

from datetime import datetime
now = datetime.now().strftime("%Y%m%d%H%M")
print(now)

success_text = f"You have just successfully uploaded {uploaded_filename}, which will be renamed to:" 
print(success_text)

changing_video_name = clean(f"{coreo}_{video_background}_{dance_role}_{salsa_style}_{uploaded_filename}")
print(changing_video_name)