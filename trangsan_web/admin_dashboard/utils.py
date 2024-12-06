from groq import Groq
from decouple import config
import re

def generate_prioritas_catatan(aduan):
    """
    Fungsi untuk menghasilkan prioritas dan catatan dari aduan masyarakat menggunakan Groq API.

    Args:
        aduan (str): Aduan masyarakat.

    Returns:
        tuple: Prioritas (str) dan catatan (str) yang dihasilkan.
    """
    # Baca API key dari .env
    api_key = config("GROQ_API_KEY")

    client = Groq(
        api_key=api_key,
    )

    # Permintaan ke model
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"""
                    Berikut adalah sebuah aduan masyarakat:
                    "{aduan}"
                    
                    Tolong tentukan:
                    1. Prioritas aduan (tinggi, sedang, rendah).
                    2. Catatan singkat yang relevan.
                    
                    Format output:
                    Prioritas: [Tinggi/Sedang/Rendah]
                    Catatan: [Catatan singkat]
                """,
            }
        ],
        model="llama3-70b-8192",
    )

    # Parsing hasil
    result = chat_completion.choices[0].message.content

    # Regular expression untuk mengekstrak Prioritas dan Catatan
    prioritas_match = re.search(r"Prioritas:\s*(Tinggi|Sedang|Rendah)", result)
    catatan_match = re.search(r"Catatan:\s*(.*)", result)

    prioritas = prioritas_match.group(1) if prioritas_match else None
    catatan = catatan_match.group(1).strip() if catatan_match else None

    return prioritas, catatan